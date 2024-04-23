from everai.commands.command import ClientCommand
from argparse import _SubParsersAction

from .create import CreateCommand
from .get import GetCommand
from .deploy import DeployCommand
from .pause import PauseCommand
from .upgrade import UpgradeCommand
from .prepare import PrepareCommand
from .list import ListCommand
from everai.commands.command import setup_subcommands


class AppCommand(ClientCommand):
    parser: _SubParsersAction = None

    def __init__(self, args):
        self.args = args

    @staticmethod
    def setup(parser: _SubParsersAction):
        app_parser = parser.add_parser('app', help='Manage app')
        app_subparser = app_parser.add_subparsers(help='App command help')

        setup_subcommands(app_subparser, [
            CreateCommand,
            GetCommand,
            UpgradeCommand,
            PauseCommand,
            DeployCommand,
            PauseCommand,
            PrepareCommand,
            ListCommand,
        ])

        app_parser.set_defaults(func=AppCommand)
        AppCommand.parser = app_parser

    def run(self):
        AppCommand.parser.print_help()
