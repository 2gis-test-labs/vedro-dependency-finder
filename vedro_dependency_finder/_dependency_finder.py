from vedro.core import Dispatcher, Plugin, PluginConfig, ScenarioOrderer, VirtualScenario, ConfigType
from vedro.events import ArgParsedEvent, ArgParseEvent, ConfigLoadedEvent
from ._dependency_orderer import DependencyOrderer
from ._dependency_scheduler import DependencyScheduler


class DependencyFinderPlugin(Plugin):
    def subscribe(self, dispatcher: Dispatcher) -> None:
        dispatcher.listen(ConfigLoadedEvent, self.on_config_loaded) \
            .listen(ArgParseEvent, self.on_arg_parse) \
            .listen(ArgParsedEvent, self.on_arg_parsed)

    def on_config_loaded(self, event: ConfigLoadedEvent) -> None:
        self._global_config: ConfigType = event.config

    def on_arg_parse(self, event: ArgParseEvent) -> None:
        group = event.arg_parser.add_argument_group("DependencyFinder")

        group.add_argument("--dependency-finder", nargs="+", default=list(),
                           help="Generates a sequence of tests at startup to detect unstable tests")

    def on_arg_parsed(self, event: ArgParsedEvent) -> None:
        scenarios_paths = event.args.dependency_finder

        if scenarios_paths:
            self._global_config.Registry.ScenarioOrderer.register(
                lambda: DependencyOrderer(scenarios_paths), self
            )
            self._global_config.Registry.ScenarioScheduler.register(DependencyScheduler, self)


class DependencyFinder(PluginConfig):
    plugin = DependencyFinderPlugin
