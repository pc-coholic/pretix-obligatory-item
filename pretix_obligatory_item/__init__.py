from django.utils.translation import gettext_lazy

try:
    from pretix.base.plugins import PluginConfig
except ImportError:
    raise RuntimeError("Please use pretix 2.7 or above to run this plugin!")

__version__ = "1.0.0"


class PluginApp(PluginConfig):
    name = "pretix_obligatory_item"
    verbose_name = "Obligatory Item Purchase"

    class PretixPluginMeta:
        name = gettext_lazy("Obligatory Item Purchase")
        author = "Martin Gross"
        description = gettext_lazy("This plugin enforces the purchase of a specific item")
        visible = True
        version = __version__
        category = "FEATURE"
        compatibility = "pretix>=2.7.0"

    def ready(self):
        from . import signals  # NOQA


default_app_config = "pretix_obligatory_item.PluginApp"
