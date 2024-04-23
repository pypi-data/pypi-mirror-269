import logging

import rich_click as click
from cli_base.cli_tools.verbosity import OPTION_KWARGS_VERBOSE, setup_logging
from cli_base.systemd.api import ServiceControl
from rich import print  # noqa

from ha_services.cli_app import cli
from ha_services.cli_app.settings import get_user_settings
from ha_services.example import DemoSettings, SystemdServiceInfo


logger = logging.getLogger(__name__)


@cli.command()
@click.option('-v', '--verbosity', **OPTION_KWARGS_VERBOSE)
def systemd_debug(verbosity: int):
    """
    Print Systemd service template + context + rendered file content.
    """
    setup_logging(verbosity=verbosity)
    user_settings: DemoSettings = get_user_settings(debug=True)
    systemd_settings: SystemdServiceInfo = user_settings.systemd

    ServiceControl(info=systemd_settings).debug_systemd_config()


@cli.command()
@click.option('-v', '--verbosity', **OPTION_KWARGS_VERBOSE)
def systemd_setup(verbosity: int):
    """
    Write Systemd service file, enable it and (re-)start the service. (May need sudo)
    """
    setup_logging(verbosity=verbosity)
    user_settings: DemoSettings = get_user_settings(debug=True)
    systemd_settings: SystemdServiceInfo = user_settings.systemd

    ServiceControl(info=systemd_settings).setup_and_restart_systemd_service()


@cli.command()
@click.option('-v', '--verbosity', **OPTION_KWARGS_VERBOSE)
def systemd_remove(verbosity: int):
    """
    Write Systemd service file, enable it and (re-)start the service. (May need sudo)
    """
    setup_logging(verbosity=verbosity)
    user_settings: DemoSettings = get_user_settings(debug=True)
    systemd_settings: SystemdServiceInfo = user_settings.systemd

    ServiceControl(info=systemd_settings).remove_systemd_service()


@cli.command()
@click.option('-v', '--verbosity', **OPTION_KWARGS_VERBOSE)
def systemd_status(verbosity: int):
    """
    Display status of systemd service. (May need sudo)
    """
    setup_logging(verbosity=verbosity)
    user_settings: DemoSettings = get_user_settings(debug=True)
    systemd_settings: SystemdServiceInfo = user_settings.systemd

    ServiceControl(info=systemd_settings).status()


@cli.command()
@click.option('-v', '--verbosity', **OPTION_KWARGS_VERBOSE)
def systemd_stop(verbosity: int):
    """
    Stops the systemd service. (May need sudo)
    """
    setup_logging(verbosity=verbosity)
    user_settings: DemoSettings = get_user_settings(debug=True)
    systemd_settings: SystemdServiceInfo = user_settings.systemd

    ServiceControl(info=systemd_settings).stop()
