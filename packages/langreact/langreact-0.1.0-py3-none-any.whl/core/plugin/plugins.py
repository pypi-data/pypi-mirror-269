import abc
from dataclasses import dataclass, field
from conf.default import Configure
from core.application import Application
from core.common.chunk import Chunk
from typing import List, Optional
from core.observer.observer import Observer
from core.modifier.context_modifier import GlobalContextModifier, LocalContextModifier
from core.modifier.chunk_modifier import ChunkModifier
from core.params import InvokeParams
from core.planning.agent import PlanningAgent
from core.builder.output_builder import DefaultOutputBuilder, OutputBuilder
from core.plugin.base import Plugin


class GlobalContextPlugin(Plugin):
    """init global context at flow's beginning"""

    @abc.abstractmethod
    def create_global_context_modifier(self) -> GlobalContextModifier:
        """create GlobalContextModifier"""


class ObserverPlugin(Plugin):
    """add observers to watch some event and react it"""

    @abc.abstractmethod
    def create_observers(self, global_context) -> List[Observer]:
        """create Observers"""


class PlanningAgentPlugin(Plugin):
    """create EventMappings for detecting intent of chunk"""

    @abc.abstractmethod
    def create_planning_agents(self, global_context) -> List[PlanningAgent]:
        """create EventMappings"""


class ApplicationPlugin(Plugin):
    """interact between LangReact and user through output_builder and input_chunk_modifier"""

    def create_local_context_modifier(
        self, params: InvokeParams
    ) -> LocalContextModifier:
        """create LocalContextModifiers"""
        return LocalContextModifier()

    def create_input_chunk_modifier(self, local_context, chunk: Chunk) -> ChunkModifier:
        """create ChunkModifier for parse original input"""
        return ChunkModifier()

    def create_output_builder(self, local_context) -> OutputBuilder:
        """create ChunkModifier for parse original input"""
        return DefaultOutputBuilder("LLM")

    @abc.abstractmethod
    def create_new_application(
        self, local_context, configure: Configure, reflection=False
    ) -> Application:
        """create EventMappings of final return event"""
