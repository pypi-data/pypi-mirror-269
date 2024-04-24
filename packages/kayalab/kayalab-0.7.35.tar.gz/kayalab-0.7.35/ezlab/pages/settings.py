# Config show dialog
import json
import logging
from nicegui import app, ui
from ezlab.parameters import DF, UA
from ezlab.pages import ezmeral

from ezlab.pages.sshkeys import ssh_keys_ui
from ezlab.pages import targets
from ezlab.pages import settings
from ezlab.utils import CONFIG_DL_PATH

logger = logging.getLogger("ezlab.ui.settings")


def save_config(val: str, dialog):
    try:
        for key, value in json.loads(val.replace("\n", "")).items():
            app.storage.general[key] = value
        for m in (ezmeral.menu, targets.menu, settings.menu):
            m.refresh()
        dialog.close()
        ui.notify("Settings loaded", type="positive")
    except (TypeError, json.decoder.JSONDecodeError, ValueError) as error:
        ui.notify("Not a valid json", type="negative")
        logger.warning(error)


def config_show():
    with ui.dialog() as config_show, ui.card().classes("grow"):
        ui.code(json.dumps(app.storage.general, indent=2), language="json").classes("w-full text-wrap")
        with ui.row().classes("w-full"):
            ui.button(
                "Save",
                icon="save",
                on_click=lambda: ui.download(CONFIG_DL_PATH),
            )
            ui.space()
            ui.button(
                "Close",
                icon="cancel",
                on_click=config_show.close,
            )
    return config_show


# Config load dialog
def config_load():
    with ui.dialog() as config_load, ui.card().classes("grow"):
        ui.upload(label="Config JSON", auto_upload=True, on_upload=lambda e: save_config(e.content.read().decode("utf-8"), config_load)).classes(
            "max-w-full"
        )
        # jsontext = ui.textarea().props("stack-label=json autogrow filled").classes("h-dvh w-full text-wrap")
        # with ui.row():
        #     ui.button(
        #         "Save",
        #         on_click=lambda _: save_config(
        #             jsontext.value,
        #             config_load,
        #         ),
        #         icon="save",
        #     )
        #     ui.button(
        #         "Close",
        #         icon="cancel",
        #         on_click=config_load.close,
        #     )

    return config_load


@ui.refreshable
def menu():
    with (
        ui.expansion(
            "Settings",
            icon="settings",
            caption="for your environment",
        )
        .classes("w-full")
        .classes("text-bold") as settings
    ):
        with ui.row().classes("w-full place-items-end"):
            ui.input("Datacenter").bind_value(app.storage.general, "datacenter").classes("grow")
            # ui.space()
            ui.checkbox("Dry Run", value=False).bind_value(app.storage.general["config"], "dryrun")
        ui.label("Network Settings").classes("text-bold")
        with ui.row().classes("w-full"):
            ui.input("VM Network", placeholder="10.1.1.0/24").bind_value(app.storage.general["config"], "cidr").classes("grow")
            ui.input("Gateway", placeholder="10.1.1.1").bind_value(app.storage.general["config"], "gateway").classes("grow")
            ui.input("HTTP Proxy", placeholder="").bind_value(app.storage.general["config"], "proxy").classes("grow")
        with ui.row().classes("w-full"):
            ui.input("Name Server", placeholder="10.1.1.1").bind_value(app.storage.general["config"], "nameserver").classes("grow")
            ui.space()
            ui.input("Domain", placeholder="ez.lab").bind_value(app.storage.general["config"], "domain").classes("grow")

        ui.label("Repositories").classes("text-bold")
        with ui.row().classes("w-full place-items-end"):
            # YUM Repo
            ui.input("YUM Repo", placeholder="").bind_value(app.storage.general["config"], "yumrepo").classes("grow")
            ui.input("EPEL Repo", placeholder="").bind_value(app.storage.general["config"], "epelrepo").classes("grow")
            # Airgap registry settings
            ui.input("Registry URL", placeholder="").bind_value(app.storage.general[UA], "registryUrl").classes("grow")
        # with ui.row().classes("w-full"):
        # ui.checkbox("Registry Insecure").bind_value(app.storage.general[UA], "registryInsecure")
        # ui.input("Registry User", placeholder="").bind_value(app.storage.general[UA], "registryUsername")
        # ui.input("Registry Password", placeholder="").bind_value(app.storage.general[UA], "registryPassword")
        # ui.input("Registry CA File (base64)", placeholder="").bind_value(app.storage.general[UA], "registryCaFile")

        # MapR Repository Configuration
        with ui.row().classes("w-full place-items-end"):
            ui.label("MapR Repo").classes("self-center")
            switch = ui.switch("Use local", value=False).props("left-label").bind_value(app.storage.general[DF], "maprrepoislocal")

            # Using default HPE repository
            with ui.row().bind_visibility_from(switch, "value", lambda x: not x).classes("w-full"):
                ui.input("HPE Passport e-mail").bind_value(app.storage.general[DF], "maprrepouser").classes("grow")
                ui.input("HPE Passport token", password=True, password_toggle_button=True).bind_value(
                    app.storage.general[DF], "maprrepotoken"
                ).classes("grow")

            # Using local repository
            with ui.row().classes("w-full place-items-end").bind_visibility_from(switch, "value"):
                ui.input(
                    "MapR Repo",
                    placeholder="https://repo.ez.lab/mapr/",
                ).bind_value(
                    app.storage.general[DF], "maprlocalrepo"
                ).classes("grow")
                authlocal = ui.switch("Authenticate", value=True).bind_value(app.storage.general[DF], "maprlocalrepoauth")
                with ui.row().classes("w-full place-items-end"):
                    ui.input("Username", password=True).bind_value(app.storage.general[DF], "maprlocalrepousername").bind_visibility(
                        authlocal, "value"
                    ).classes("grow")
                    ui.input("Password", password=True).bind_value(app.storage.general[DF], "maprlocalrepopassword").bind_visibility(
                        authlocal, "value"
                    ).classes("grow")

        ui.label("Cloudinit Settings").classes("text-bold")
        with ui.row().classes("w-full place-items-end"):
            ui.input("username", placeholder="ezmeral").bind_value(app.storage.general["config"], "username").classes("grow")
            ui.input("password", password=True, password_toggle_button=True).bind_value(app.storage.general["config"], "password").classes("grow")

        ui.label("SSH Key").classes("text-bold")
        ssh_keys_ui()

    settings.bind_value(app.storage.general["ui"], "settings")
