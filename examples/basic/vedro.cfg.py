import vedro
import vedro_dependency_finder as df


class Config(vedro.Config):

    class Plugins(vedro.Config.Plugins):

        class DependencyFinder(df.DependencyFinder):
            enabled = True
