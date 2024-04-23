from importlib import resources

from mkdocs_thebe import assets

from mkdocs.plugins import BasePlugin
from mkdocs.config.base import Config
from mkdocs.config import config_options


class MkDocsThebeConfig(Config):
    baseUrl = config_options.Type(str)


class MkDocsThebe(BasePlugin[MkDocsThebeConfig]):
    def on_config(self, config, **kwargs):
        # extra_javascript
        # extra_css
        # extra_templates

        path_to_assets = resources.files(assets)
        config["theme"].dirs.insert(0, path_to_assets)

        config["extra_javascript"].append("mkdocs-thebe.js")
        config["extra_css"].append("mkdocs-thebe.css")

        print("site dir", config["site_dir"])

        return config
