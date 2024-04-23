# Copyright 2024 The Orbax Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A class providing emergency checkpoint management.


This class is experimental; do not use without specific approval.
"""

import collections
import dataclasses
from typing import Any, Optional, Sequence, Set
from etils import epath
import jax
from jax.experimental import multihost_utils
import jax.numpy as jnp
import numpy as np
from orbax.checkpoint import abstract_checkpoint_manager
from orbax.checkpoint import args as args_lib
from orbax.checkpoint import checkpoint_manager
from orbax.checkpoint import multihost
from orbax.checkpoint import utils
from orbax.checkpoint.path import step as step_lib


PyTree = checkpoint_manager.PyTree
CheckpointHandler = checkpoint_manager.CheckpointHandler
P = jax.sharding.PartitionSpec


@dataclasses.dataclass
class LocalCheckpointOptions:
  """Optional CheckpointManager arguments for saving local checkpoints.

  save_interval_steps:
    The interval at which checkpoints should be saved to local storage.
    Ensures checkpoints will only be saved every m steps. Defaults to 10.
  max_to_keep:
    If provided, specifies the maximum number of local checkpoints to
    keep. Older checkpoints are removed. When set, no more than `max_to_keep`
    checkpoints will be present at any one time. This option has a slightly
    different meaning than it normally does in Orbax: this should be treated
    as a hard cap on the number of checkpoints concurrently present, rather
    than a threshold beyond which checkpoints start to be deleted.
  """

  save_interval_steps: int = 10
  max_to_keep: Optional[int] = 2


@dataclasses.dataclass
class PersistentCheckpointOptions:
  """Optional CheckpointManager arguments for saving persistent checkpoints.

  save_interval_steps:
    The interval at which checkpoints should be saved to persistent storage.
    Ensures checkpoints will only be saved every n steps. Defaults to 1000.
  max_to_keep:
    If provided, specifies the maximum number of persistent checkpoints to
    keep. Older checkpoints are removed. By default, does not remove any old
    checkpoints. Must be None or non-negative. When set, checkpoints
    may be considered for deletion when there are more than `max_to_keep`
    checkpoints present.
  """

  save_interval_steps: int = 1000
  max_to_keep: Optional[int] = None


@dataclasses.dataclass
class CheckpointManagerOptions:
  """Optional arguments for CheckpointManager.

  local:
    Options relevant to the local checkpoints.
    See `LocalCheckpointOptions`.
  persistent:
    Options relevant to the persistent checkpoints. See
    `PersistentCheckpointOptions`.
  step_name_format:
    NameFormat to build or find steps under input root directory. If provided,
    `step_prefix`, `step_format_fixed_length` are ignored.
  create:
    If True, creates the top-level directory if it does not already exist.
  cleanup_tmp_directories:
    If True, cleans up any existing temporary directories
    on CheckpointManager creation.
  async_options: Used to configure properties of async behavior. See above.
  """

  local: LocalCheckpointOptions = dataclasses.field(
      default_factory=LocalCheckpointOptions
  )
  persistent: PersistentCheckpointOptions = dataclasses.field(
      default_factory=PersistentCheckpointOptions
  )

  step_name_format: Optional[step_lib.NameFormat] = None
  create: bool = True
  cleanup_tmp_directories: bool = False
  async_options: Optional[checkpoint_manager.AsyncOptions] = None


def _in_slice(process_index: int, device_slice: np.ndarray) -> bool:
  pid = np.vectorize(lambda d: d.process_index)
  return process_index in pid(device_slice)


def _in_primary_slice(
    process_index: int, global_mesh: jax.sharding.Mesh
) -> bool:
  """Returns true if host is in primary slice (the first slice)."""
  primary_slice = global_mesh.devices[0]

  return _in_slice(process_index, primary_slice)


def _unique_processes_from_devices(device_array: np.ndarray) -> Set[int]:
  pid = np.vectorize(lambda d: d.process_index)
  return set(pid(device_array).flat)


def _local_slice_devices(devices_array: np.ndarray) -> np.ndarray:
  for device_slice in devices_array:
    if _in_slice(jax.process_index(), device_slice):
      return device_slice
  raise ValueError(
      f'process_index {jax.process_index()} does not exist in provided'
      ' `global_mesh`'
  )


def _pad_steps(steps, target):
  return steps + [-1] * (target - len(steps))


class _LocalCheckpointManager(checkpoint_manager.CheckpointManager):
  """A checkpoint manager that checkpoints to local storage.

  Attributes:
    device_array: an ndarray representing all the devices running
      LocalCheckpointManager in the same global jax Mesh, importantly the first
      axis of the device_array is assumed to be the direction of device slices
      across which the Data Parallelism is happening.
  """

  # TODO: b/330585086 - Allow configuration of global mesh describing slices.
  # Validate against global meshes used for arrays in state.
  def __init__(
      self,
      directory: epath.PathLike,
      # TODO: b/330585086 - Support arbitrary items beyond state. We will have
      # to evaluate whether arbitrary items can be a good fit for local
      # checkpointing, given restore+broadcast requirements.
      state_handler: CheckpointHandler,
      device_array: np.ndarray,
      *,
      options: Optional[CheckpointManagerOptions] = None,
      metadata: Optional[dict[str, Any]] = None,
  ):
    # TODO: b/330585086 - Fully support options.
    options = options or CheckpointManagerOptions()
    local_options = checkpoint_manager.CheckpointManagerOptions(
        save_interval_steps=options.local.save_interval_steps,
        max_to_keep=options.local.max_to_keep,
        step_name_format=options.step_name_format,
        create=options.create,
        cleanup_tmp_directories=options.cleanup_tmp_directories,
        async_options=options.async_options,
        multiprocessing_options=checkpoint_manager.MultiprocessingOptions(
            primary_host=None,
            active_processes=_unique_processes_from_devices(device_array),
        ),
        # TODO: b/331426277 - remove async false after barrier is done.
        enable_async_checkpointing=False,
    )
    self._options = local_options
    self._device_array = device_array

    super().__init__(
        directory,
        options=local_options,
        metadata=metadata,
        item_handlers=state_handler,
    )

  def _global_list_union(
      self, steps: Sequence[int], devices: np.ndarray
  ) -> np.ndarray:
    slice_mesh = jax.sharding.Mesh(
        devices.reshape(
            devices.size // jax.local_device_count(), jax.local_device_count()
        ),
        ['host', 'dev'],
    )

    g_arr = multihost_utils.host_local_array_to_global_array(
        np.asarray(steps), slice_mesh, P('host')
    )

    result_arr = jax.jit(
        lambda x: x,
        out_shardings=jax.sharding.NamedSharding(slice_mesh, P()),
    )(g_arr)

    return np.asarray(result_arr.addressable_data(0))

  def _common_steps_global(self, steps: Sequence[int]) -> np.ndarray:
    """Returns common steps across all slices.

    A step is considered as "common step" if it is known to any slice.

    The slice is assumed to be diveded along the first axis, i.e. slice0 =
    global_mesh.devices[0]

    Args:
      steps: a list of steps known to all hosts on a slice
    """
    unioned_steps = self._global_list_union(steps, self._device_array)

    return np.asarray(list(set(unioned_steps)))

  def _common_steps_within_slice(self, steps: Sequence[int]) -> np.ndarray:
    """Returns common steps within one slices.

    A step is considered "common step" if it is known to every host in the slice

    The slice is assumed to be diveded along the first axis, i.e. slice0 =
    global_mesh.devices[0]

    This function will pad return array to len(steps) with -1's indicating no
    step.

    Args:
      steps: a list of known steps on host
    """

    devices = _local_slice_devices(self._device_array)
    slice_process_count = devices.size // jax.local_device_count()
    unioned_steps = self._global_list_union(steps, devices)

    def count_and_filter(steps, num_process):
      count = collections.Counter(steps)
      return np.asarray([k for k in count if count[k] == num_process])

    result = count_and_filter(unioned_steps, slice_process_count)

    # here len(result) will be <= len(steps) because there are at most
    # len(steps) unique step number that appeared `slice_process_count` times in
    # an array with size [len(steps), slice_process_count]
    if len(result) > len(steps):
      raise AssertionError(
          f' len(result steps) {result} exceeded length of input steps {steps}'
      )

    return np.asarray(_pad_steps(list(result), len(steps)))

  def all_steps(self, read: bool = False) -> Sequence[int]:
    """Returns all steps tracked by the manager.

    Includes steps located in local as well as persistent storage.

    Args:
      read: If True, forces a read directly from the storage location.
        Otherwise, a cached result can be returned.

    Returns:
      A sequence of steps (integers)
    """
    # List of steps present in individual host storage.
    local_steps = list(super().all_steps(read))

    if len(local_steps) > self._options.max_to_keep:
      raise AssertionError(
          f' local_step on host {jax.process_index()} exceeded `max_to_keep`'
          f' {self._options.max_to_keep}'
      )

    local_steps = _pad_steps(local_steps, self._options.max_to_keep)

    common_steps_on_slice = self._common_steps_within_slice(local_steps)

    steps = self._common_steps_global(common_steps_on_slice)

    return [x for x in steps if x != -1]

  def latest_step(self) -> Optional[int]:
    """Returns the latest step saved in the local storage.

    Returns None if no steps have been saved.

    Returns:
      A step (int) or None if no steps are present.
    """
    local_all_steps = self.all_steps()
    return max(local_all_steps) if local_all_steps else None


class CheckpointManager(abstract_checkpoint_manager.AbstractCheckpointManager):
  """A checkpoint manager that stores checkpoint to local storage."""

  # TODO: b/330585086 - Allow configuration of global mesh describing slices.
  # Validate against global meshes used for arrays in state.
  def __init__(
      self,
      local_directory: epath.PathLike,
      persistent_directory: epath.PathLike,
      global_mesh: jax.sharding.Mesh,
      # TODO: b/330585086 - Support arbitrary items beyond state. We will have
      # to evaluate whether arbitrary items can be a good fit for local
      # checkpointing, given restore+broadcast requirements.
      local_state_handler: CheckpointHandler,
      persistent_state_handler: CheckpointHandler,
      *,
      options: Optional[CheckpointManagerOptions] = None,
      metadata: Optional[dict[str, Any]] = None,
  ):
    # TODO: b/330585086 - Fully support options.
    options = options or CheckpointManagerOptions()
    self._device_array = global_mesh.devices

    self._persistent_primary_host = global_mesh.devices[0].flat[0].process_index
    self._local_primary_host = (
        global_mesh.devices[1].flat[0].process_index
        if global_mesh.devices.shape[0] > 1
        else None
    )
    if self._local_primary_host is None:
      raise AssertionError(
          'to use this CheckpointManager, at least 3 data-parallel slices are'
          ' needed.'
      )

    self._in_primary_slice = _in_primary_slice(jax.process_index(), global_mesh)
    self._persistent_max_to_keep = options.persistent.max_to_keep
    self._local_max_to_keep = options.local.max_to_keep

    if self._in_primary_slice:
      # TODO: b/330585086 - Build options for persistent CheckpointManager.
      persistent_options = checkpoint_manager.CheckpointManagerOptions(
          save_interval_steps=options.persistent.save_interval_steps,
          max_to_keep=self._persistent_max_to_keep,
          step_name_format=options.step_name_format,
          create=options.create,
          cleanup_tmp_directories=options.cleanup_tmp_directories,
          async_options=options.async_options,
          multiprocessing_options=checkpoint_manager.MultiprocessingOptions(
              primary_host=self._persistent_primary_host,
              active_processes=_unique_processes_from_devices(
                  global_mesh.devices[0]
              ),
          ),
          # TODO: b/331426277 - remove async false after barrier is done.
          enable_async_checkpointing=False,
      )
      self._persistent_checkpoint_manager = (
          checkpoint_manager.CheckpointManager(
              persistent_directory,
              options=persistent_options,
              metadata=metadata,
              item_handlers=persistent_state_handler,
          )
      )
    else:
      self._local_checkpoint_manager = _LocalCheckpointManager(
          local_directory,
          local_state_handler,
          device_array=global_mesh.devices[1:],
          options=options,
          metadata=metadata,
      )

  @property
  def directory(self) -> epath.Path:
    raise NotImplementedError()

  def all_steps(self, read: bool = False) -> Sequence[int]:
    """Returns all steps tracked by the manager.

    Includes steps located in local as well as persistent storage.

    Args:
      read: If True, forces a read directly from the storage location.
        Otherwise, a cached result can be returned.

    Returns:
      A sequence of steps (integers)
    """
    local_steps = [-1] * self._local_max_to_keep
    persistent_steps = [-1] * self._persistent_max_to_keep
    if self._in_primary_slice:
      persistent_steps = list(
          self._persistent_checkpoint_manager.all_steps(read)
      )
      if len(persistent_steps) > self._persistent_max_to_keep:
        # TODO: b/330585086 - for now we assume that
        # persistent_checkpoint_manager.all_steps returns an array with length
        # smaller than max_to_keep
        raise AssertionError(
            f'persistent_step on host {jax.process_index()} exceeded'
            f' `max_to_keep` {self._persistent_max_to_keep}'
        )
      persistent_steps = _pad_steps(
          persistent_steps, self._persistent_max_to_keep
      )
    else:
      local_steps = _pad_steps(
          list(self._local_checkpoint_manager.all_steps(read)),
          self._local_max_to_keep,
      )

    local_steps = np.asarray(
        multihost.broadcast_one_to_all(
            local_steps,
            is_source=jax.process_index() == self._local_primary_host,
        )
    )

    persistent_steps = np.asarray(
        multihost.broadcast_one_to_all(
            persistent_steps,
            is_source=jax.process_index() == self._persistent_primary_host,
        )
    )

    return [
        x
        for x in set(np.concatenate((local_steps, persistent_steps)))
        if x != -1
    ]

  def latest_step(self) -> Optional[int]:
    """Returns the latest step saved.

    Includes steps located in local as well as persistent storage.

    Returns None if no steps have been saved.

    Returns:
      A step (int) or None if no steps are present.
    """
    if self._in_primary_slice:
      latest_step = self._persistent_checkpoint_manager.latest_step()
    else:
      latest_step = self._local_checkpoint_manager.latest_step()

    if latest_step is None:
      latest_step = -1

    latest_step = self._global_max(latest_step)
    return latest_step if latest_step != -1 else None

  def best_step(self) -> Optional[int]:
    """Returns the best step saved, as defined by `options.best_fn`.

    Includes steps located in local as well as persistent storage.

    Returns None if no steps have been saved.

    Returns:
      A step (int) or None if no steps are present.
    """
    raise NotImplementedError(
        'Metrics tracking not yet implemented for emergency.CheckpointManager.'
    )

  def reload(self):
    """Performs disk reads to ensure internal properties are up to date."""
    if self._local_primary_host:
      self._persistent_checkpoint_manager.reload()
    else:
      self._local_checkpoint_manager.reload()

  def reached_preemption(self, step: int) -> bool:
    """Returns True if a preemption sync point has been reached."""
    return utils.reached_preemption(step)

  def _global_max(self, value: Any) -> Any:
    """Returns the global max of a local value across all devices as a scalar."""
    slice_mesh = jax.sharding.Mesh(
        self._device_array.reshape(
            self._device_array.size // jax.local_device_count(),
            jax.local_device_count(),
        ),
        ['host', 'dev'],
    )

    g_arr = multihost_utils.host_local_array_to_global_array(
        np.asarray([value]), slice_mesh, P('host')
    )

    result_arr = jax.jit(
        jnp.max,
        out_shardings=jax.sharding.NamedSharding(slice_mesh, P()),
    )(g_arr)

    return result_arr.addressable_data(0)

  def should_save(self, step: int) -> bool:
    """Returns True if a checkpoint should be saved for the current step.

    This depends the previous step and save interval.

    Args:
      step: int

    Returns:
      True if the checkpoint should be saved.
    """
    if self._in_primary_slice:
      should_save = self._persistent_checkpoint_manager.should_save(step)
    else:
      should_save = self._local_checkpoint_manager.should_save(step)
    return self._global_max(should_save)

  def delete(self, step: int):
    """Deletes a step checkpoint."""
    raise NotImplementedError(
        'Delete not yet implemented for emergency.CheckpointManager.'
    )

  def save(
      self,
      step: int,
      args: Optional[args_lib.CheckpointArgs] = None,
      metrics: Optional[PyTree] = None,
      force: Optional[bool] = False,
  ) -> bool:
    # TODO: b/330608746 - implement save op on different slices

    # this code is only for testing purpose for all_steps funcion.
    if self._in_primary_slice:
      saved = self._persistent_checkpoint_manager.save(
          step, args=args, metrics=metrics, force=force
      )
    else:
      saved = self._local_checkpoint_manager.save(
          step, args=args, metrics=metrics, force=force
      )

    return self._global_max(saved)

  def restore(
      self,
      step: int,
      args: Optional[args_lib.CheckpointArgs] = None,
      directory: Optional[epath.PathLike] = None,
  ) -> Any:
    return self._local_checkpoint_manager.restore(
        step, args=args, directory=directory
    )

  def item_metadata(self, step: int) -> Any:
    raise NotImplementedError(
        'Item metadata not yet implemented for emergency.CheckpointManager.'
    )

  def metadata(self) -> dict[str, Any]:
    """Returns CheckpointManager level metadata if present, empty otherwise."""
    raise NotImplementedError(
        'Metadata not yet implemented for emergency.CheckpointManager.'
    )

  def metrics(self, step: int) -> Optional[PyTree]:
    """Returns metrics for step, if present."""
    raise NotImplementedError(
        'Metrics not yet implemented for emergency.CheckpointManager.'
    )

  def wait_until_finished(self):
    """Blocks until any incomplete save operations are completed.

    Note that this method will typically be a no-op if all checkpointers are
    synchronous, since old checkpoints are already cleaned up immediately after
    completing `save`, and there is no background thread to wait for.

    If some checkpointers are of type AsyncCheckpointer, however, this method
    will wait until each of these checkpointers is finished.
    """
    if self._in_primary_slice:
      self._persistent_checkpoint_manager.wait_until_finished()
    else:
      self._local_checkpoint_manager.wait_until_finished()

  def check_for_errors(self):
    """Checks for any outstanding errors in completed asynchronous save operations.

    Delegates to underlying Checkpointer.
    """
    if self._in_primary_slice:
      self._local_checkpoint_manager.check_for_errors()
    else:
      self._persistent_checkpoint_manager.check_for_errors()

  def close(self):
    """Waits for outstanding operations to finish and closes Checkpointers."""
    if self._in_primary_slice:
      self._local_checkpoint_manager.close()
    else:
      self._persistent_checkpoint_manager.close()
