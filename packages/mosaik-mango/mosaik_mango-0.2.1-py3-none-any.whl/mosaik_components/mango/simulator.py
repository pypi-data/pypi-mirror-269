from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, TypeAlias

import mosaik_api_v3
from typing_extensions import override

from mango import Agent, create_container
from mango.util.clock import ExternalClock

if TYPE_CHECKING:
    from collections.abc import Coroutine, Generator

    from mosaik_api_v3.types import (
        CreateResult,
        InputData,
        OutputData,
        OutputRequest,
        Time,
    )

    from mango.container.core import Container
    from mango.messages.codecs import Codec


class MosaikAgent(Agent, ABC):
    @abstractmethod
    def start_mosaik_step(self, inputs: dict[str, dict[str, Any]]) -> None:
        ...

    @abstractmethod
    def get_mosaik_output(self, request: list[str]) -> dict[str, Any]:
        ...

    def setup_done(self) -> None:
        pass

    @property
    def time(self):
        return int(self._context.current_timestamp)


@dataclass(frozen=True)
class AgentSpec:
    agent_class: type[MosaikAgent]
    params: list[str] = field(default_factory=list)
    connection_params: dict[str, str] = field(default_factory=dict)
    inputs: list[str] = field(default_factory=list)
    measurements: list[str] = field(default_factory=list)
    outputs: list[str] = field(default_factory=list)


AgentSetup: TypeAlias = dict[str, AgentSpec]


@dataclass(frozen=True)
class AgentAddress:
    container_addr: tuple[str, int]
    aid: str


class MangoSimulator(mosaik_api_v3.Simulator):
    _sid: str
    """This simulator's ID."""
    _step_size: int
    """The step size for this simulator. If ``None``, the simulator
    is running in event-based mode, instead.
    """

    _agent_setup: AgentSetup
    _mango_codec: Codec | None

    _mango_container: Container
    _agent_addresses: dict[str, dict[str, AgentAddress]]
    _agents: dict[str, MosaikAgent]

    def __init__(self, agent_setup: AgentSetup, codec: Codec | None = None):
        self._agent_setup = agent_setup
        self._mango_codec = codec
        self._agents = {}
        self._agent_addresses = defaultdict(dict)
        super().__init__(
            {
                "api_version": "3.0",
                "type": "hybrid",
                "models": {
                    model: {
                        "public": True,
                        "params": [
                            "id",
                            *agent_spec.params,
                            *agent_spec.connection_params.keys(),
                        ],
                        "attrs": [
                            *agent_spec.inputs,
                            *agent_spec.measurements,
                            *agent_spec.outputs,
                        ],
                        "non-trigger": agent_spec.measurements,
                        "persistent": [],
                    }
                    for model, agent_spec in agent_setup.items()
                },
            }
        )

    @override
    def init(
        self, sid: str, time_resolution: float, addr: tuple[str, int], step_size: int
    ):
        self._sid = sid
        self._step_size = step_size
        self._mango_container = yield create_container(
            addr=addr,
            codec=self._mango_codec,
            clock=ExternalClock(start_time=-step_size),
        )
        return self.meta

    @override
    def create(self, num: int, model: str, **params: Any) -> list[CreateResult]:
        agent_spec = self._agent_setup[model]
        container = self._mango_container

        # For each param name listed in agent_params, the value should
        # be the ID of an already-created agent. Replace this ID by the
        # agent's address, so that the new agent can send messages to
        # it.
        for name, value in params.items():
            param_model = agent_spec.connection_params.get(name)
            if not param_model:
                continue
            addr = self._agent_addresses[param_model][value]
            params[name] = addr

        new_entities: list[CreateResult] = []
        for _ in range(num):
            eid = params.pop("id", f"{model}-{len(self._agent_addresses[model])}")
            agent = agent_spec.agent_class(
                suggested_aid=eid,
                container=container,
                **params,
            )
            self._agents[eid] = agent
            self._agent_addresses[model][eid] = AgentAddress(
                tuple(container.addr), agent.aid
            )
            new_entities.append({"eid": eid, "type": model})
        return new_entities

    async def _wait_for_termination(self):
        await asyncio.gather(
            *(
                agent._scheduler.tasks_complete_or_sleeping()  # noqa: SLF001
                for agent in self._agents.values()
            )
        )

    @override
    def setup_done(self) -> Generator[Coroutine[Any, Any, None], None, None]:
        for agent in self._agents.values():
            agent.setup_done()
        yield self._wait_for_termination()

    @override
    def step(
        self, time: Time, inputs: InputData, max_advance: Time
    ) -> Generator[Coroutine[Any, Any, None], None, Time]:
        self._mango_container.clock.set_time(time)
        for eid, agent in self._agents.items():
            agent.start_mosaik_step(inputs.get(eid, {}))
        yield self._wait_for_termination()

        return time + self._step_size

    @override
    def get_data(self, outputs: OutputRequest) -> OutputData:
        return {
            eid: self._agents[eid].get_mosaik_output(attrs)
            for eid, attrs in outputs.items()
        }

    @override
    def finalize(self):
        yield self._mango_container.shutdown()
