from __future__ import annotations

import json
from typing import Any, Dict, Optional, Union

import strangeworks as sw
from braket.annealing.problem import Problem
from braket.aws.aws_device import Device
from braket.circuits import Circuit
from braket.device_schema import DeviceCapabilities
from braket.ir.openqasm import Program as OpenQasmProgram
from braket.tasks.quantum_task import QuantumTask
from braket.tasks.quantum_task_batch import QuantumTaskBatch
from strangeworks_core.errors.error import StrangeworksError

from strangeworks_braket.job import StrangeworksQuantumJob
from strangeworks_braket.task import StrangeworksQuantumTask
from strangeworks_braket.utils.serializer import pickle_deserializer


class StrangeworksDevice(Device):
    def __init__(
        self,
        arn: str,
        name: Optional[str] = None,
        status: Optional[str] = None,
        slug: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(name, status)
        self.arn = arn
        self.slug = slug
        self._status = status
        self._properties: DeviceCapabilities = None
        self._certificate = None
        self._layout = None
        self._target = None
        self._modes = None

    def run(
        self,
        task_specification: Union[Circuit, Problem, OpenQasmProgram],
        shots: Optional[int],
        *args,
        **kwargs,
    ) -> QuantumTask:
        """Run a task on the device.
        Parameters
        ----------
        task_specification: Union[Circuit, Problem, OpenQasmProgram]
            The task specification.
        shots: Optional[int]
            The number of shots to run the task for. Defaults to 1000.
        Returns
        -------
        task: QuantumTask (StrangeworksQuantumTask)
            The task that was run.
        """

        return StrangeworksQuantumTask.create(
            self.arn, task_specification, shots or 1000, *args, **kwargs
        )

    def run_hybrid(
        self,
        filepath: str,
        hyperparameters: Dict[str, Any],
        *args,
        **kwargs,
    ) -> QuantumTask:
        """Run a task on the device.
        Parameters
        ----------
        filepath: str
            Path to the python file that will be run.
        hyperparameters: Dict[str, Any]
            Dictionary of hyperparameters to pass to the task.
            Must be json serializable.
        Returns
        -------
        Job: QuantumJob (StrangeworksQuantumJob)
            The job that was run.
        """
        return StrangeworksQuantumJob.create_hybrid(
            self.arn, filepath, hyperparameters, *args, **kwargs
        )

    @property
    def status(self) -> str:
        if self._status is None:
            dev = self.get_devices(arns=[self.arn])[0]
            self._status = dev.status

        return self._status

    @staticmethod
    def get_devices(
        arns: Optional[list[str]] = None,
        names: Optional[list[str]] = None,
        statuses: Optional[list[str]] = None,
    ) -> list[StrangeworksDevice]:
        """Get a list of devices.
        Parameters
        ----------
        arns: Optional[list[str]
            Filter by list of device ARNs. Defaults to None.
        names: Optional[list[str]]
            Filter by list of device names. Defaults to None.
        statuses: Optional[list[str]]
            Filter by list of device statuses. Defaults to None.
        Returns
        -------
        devices: list[SwDevice]
            List of devices that match the provided filters.
        """
        backends = sw.backends(product_slugs=["amazon-braket"])
        devices = []
        for backend in backends:
            if arns and backend.remote_backend_id not in arns:
                continue
            if names and backend.name not in names:
                continue
            if statuses and backend.remote_status not in statuses:
                continue

            devices.append(
                StrangeworksDevice(
                    backend.remote_backend_id,
                    backend.name,
                    backend.remote_status,
                    backend.slug,
                )
            )

        return devices

    def run_batch(
        self,
        task_specifications: Circuit | Problem | list[Circuit | Problem],
        shots: int | None,
        max_parallel: int | None,
        inputs: Dict[str, float] | list[Dict[str, float]] | None,
        *args,
        **kwargs,
    ) -> QuantumTaskBatch:
        raise StrangeworksError("currently not implemented/supported")

    @property
    def properties(self) -> DeviceCapabilities:
        if self._properties is None:
            payload = {
                "aws_device_arn": self.arn,
            }

            res = sw.execute_post(
                StrangeworksQuantumTask._product_slug, payload, endpoint="properties"
            )
            self._properties = pickle_deserializer(json.loads(res), "json")

        return self._properties

    def get_properties(self) -> DeviceCapabilities:

        payload = {
            "aws_device_arn": self.arn,
        }

        res = sw.execute_post(
            StrangeworksQuantumTask._product_slug, payload, endpoint="properties"
        )
        self._properties = pickle_deserializer(json.loads(res), "json")
