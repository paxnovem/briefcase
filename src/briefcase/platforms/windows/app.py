from pathlib import Path

from briefcase.commands import BuildCommand, PublishCommand, UpdateCommand
from briefcase.config import BaseConfig
from briefcase.integrations.rcedit import RCEdit
from briefcase.platforms.windows import (
    WindowsCreateCommand,
    WindowsMixin,
    WindowsPackageCommand,
    WindowsRunCommand,
)


class WindowsAppMixin(WindowsMixin):
    output_format = "app"
    packaging_root = Path("src")


class WindowsAppCreateCommand(WindowsAppMixin, WindowsCreateCommand):
    description = "Create and populate a Windows app."


class WindowsAppUpdateCommand(WindowsAppMixin, UpdateCommand):
    description = "Update an existing Windows app."


class WindowsAppBuildCommand(WindowsAppMixin, BuildCommand):
    description = "Build a Windows app."

    def verify_tools(self):
        super().verify_tools()
        self.rcedit = RCEdit.verify(self)

    def build_app(self, app: BaseConfig, **kwargs):
        """Build the application.

        :param app: The config object for the app
        """
        self.logger.info("Building App...", prefix=app.app_name)

        with self.input.wait_bar("Setting stub app details..."):
            self.subprocess.run(
                [
                    self.rcedit.rcedit_path,
                    self.binary_path(app).relative_to(self.bundle_path(app)),
                    "--set-version-string",
                    "CompanyName",
                    app.author,
                    "--set-version-string",
                    "FileDescription",
                    app.description,
                    "--set-version-string",
                    "FileVersion",
                    app.version,
                    "--set-version-string",
                    "InternalName",
                    app.module_name,
                    "--set-version-string",
                    "OriginalFilename",
                    self.binary_path(app).name,
                    "--set-version-string",
                    "ProductName",
                    app.formal_name,
                    "--set-version-string",
                    "productVersion",
                    app.version,
                    "--set-icon",
                    "icon.ico",
                ],
                check=True,
                cwd=self.bundle_path(app),
            )


class WindowsAppRunCommand(WindowsAppMixin, WindowsRunCommand):
    description = "Run a Windows app."


class WindowsAppPackageCommand(WindowsAppMixin, WindowsPackageCommand):
    description = "Package a Windows App as an MSI."


class WindowsAppPublishCommand(WindowsAppMixin, PublishCommand):
    description = "Publish a Windows App."


# Declare the briefcase command bindings
create = WindowsAppCreateCommand  # noqa
update = WindowsAppUpdateCommand  # noqa
build = WindowsAppBuildCommand  # noqa
run = WindowsAppRunCommand  # noqa
package = WindowsAppPackageCommand  # noqa
publish = WindowsAppPublishCommand  # noqa
