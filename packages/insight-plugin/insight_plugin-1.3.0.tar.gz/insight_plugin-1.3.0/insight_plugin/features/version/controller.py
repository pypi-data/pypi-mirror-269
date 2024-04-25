from insight_plugin.features.common.common_feature import CommonFeature
from insight_plugin.constants import SubcommandDescriptions
from insight_plugin.features.version.util.version_util import VersionUtil


class VersionController(CommonFeature):
    """
    Controls the subcommand to modify the plugin version & write to help.md
    Must be used within the directory that contains the plugin.spec.yaml
    """

    HELP_MSG = SubcommandDescriptions.VERSION_DESCRIPTION

    def __init__(
        self,
        version_num: str,
        changelog_desc: str,
        verbose: bool,
        target_dir: str,
    ):
        super().__init__(verbose, target_dir)
        self._version_num = version_num
        self.changelog_desc = changelog_desc
        self._verbose = verbose

    @classmethod
    def new_from_cli(cls, **kwargs):
        super().new_from_cli(
            **{
                "verbose": kwargs.get("verbose"),
                "target_dir": kwargs.get("target_dir"),
                "version_num": kwargs.get("version_num"),
                "changelog_desc": kwargs.get("changelog_desc"),
            }
        )
        return cls(
            kwargs.get("version_num"),
            kwargs.get("changelog_desc", ""),
            kwargs.get("verbose"),
            kwargs.get("target_dir"),
        )

    def semver(self):
        """
        Setup the VersionUtil class and perform the run function.
        :return:
        """
        version_util = VersionUtil(
            version_num=self._version_num,
            changelog_desc=self.changelog_desc,
            verbose=self._verbose,
            target_dir=self.target_dir,
        )
        version_util.run()
