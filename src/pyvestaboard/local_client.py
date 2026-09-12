import click
import requests
import json
import os
import enum
import sys

from blessings import Terminal

from pyvestaboard import VestaBoard, CommunicationException


class CommandType(enum.StrEnum):
    GET = enum.auto()
    SEND = enum.auto()


class VerticalAlignmentChoices(enum.Enum):
    VestaBoard.VERTICAL_ALIGN_TOP = enum.auto()
    VestaBoard.VERTICAL_ALIGN_MIDDLE = enum.auto()
    VestaBoard.VERTICAL_ALIGN_BOTTOM = enum.auto()
    VestaBoard.VERTICAL_ALIGN_JUSTIFIED = enum.auto()


def load_stored_preferences():
    prefs = {}
    preference_file_path = os.path.expanduser('~/.pyvestaboard')
    try:
        with open(preference_file_path) as pref_file:
            prefs = json.load(pref_file)
    except FileNotFoundError:
        pass
    
    if "VESTABOARD_IP" not in prefs.keys():
        prefs["VESTABOARD_IP"] = click.prompt("Vestaboard IP", type=str)
    if "VESTABOARD_PORT" not in prefs.keys():
        prefs["VESTABOARD_PORT"] = click.prompt("Port", type=int)
    if "API_TOKEN" not in prefs.keys():
        prefs["API_TOKEN"] = click.prompt("API Token", type=str)
    
    try:
        with open(preference_file_path, 'w') as pref_file:
            json.dump(prefs, pref_file)
    except Exception as ex:
        raise ex
    
    return prefs

def get_piped_input() -> str | None:
    piped_message = None
    if not os.isatty(sys.stdin.fileno()):
        piped_message = sys.stdin.read()
    return piped_message

@click.command(help="Get or Send command to VestaBoard")
@click.option(
    "-c",
    "--command",
    "command",
    type=click.Choice(CommandType, case_sensitive=False),
    default="send",
    help="Get or Send message"
)
@click.argument("message", required=False)
def cli(command, message) -> int:
    term = Terminal()
    
    piped_message = get_piped_input()
    # FIXME: We're just going to ignore the message argument if there's piped input is
    # that the right thing to do? Combine them somehow? Or add a flag to combine them?
    message = message if not piped_message else piped_message

    # FIXME: add option to ignore preferences
    prefs = load_stored_preferences()
    ip = prefs["VESTABOARD_IP"]
    port = prefs["VESTABOARD_PORT"]
    api_token = prefs["API_TOKEN"]

    vb = VestaBoard(ip, port, api_token)
    try:
        match command:
            case CommandType.GET:
                message = vb.get_current_message(multiline=True)\
                # Swap Emoji with (hopefully) monospaced characters to preserve alignment
                message = message.replace('🟩', term.green('■'))
                message = message.replace('⬜️', term.white('■'))
                message = message.replace('🟦', term.blue('■'))
                message = message.replace('🟪', term.magenta('■'))
                message = message.replace('🟥', term.red('■'))
                message = message.replace('🟧', term.bright_red('■'))
                message = message.replace('🟨', term.bright_yellow('■'))
                click.echo(message, nl=False)
            case CommandType.SEND:
                # No-op if no message has been passed (POSIX compliance)
                if message is not None:
                    vb.send_message(message)
            case _:
                raise Exception("Command not recognized")
    except CommunicationException as ex:
        click.echo(str(ex), err=True)
        return 1
    return 0

if __name__ == "__main__":
    exit(cli())