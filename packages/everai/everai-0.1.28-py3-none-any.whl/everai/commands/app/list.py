import typing

from everai.app import App
from everai.commands.command import ClientCommand, command_error
from argparse import _SubParsersAction
from everai.app.app_manager import AppManager


class ListCommand(ClientCommand):
    def __init__(self, args):
        self.args = args

    @staticmethod
    def setup(parser: _SubParsersAction):
        list_parser = parser.add_parser("list", help="List all apps")
        list_parser.add_argument("--output", "-o",
                                 help="Output format, One of: (json, yaml, table, wide)",
                                 nargs="?", default="table")
        list_parser.set_defaults(func=ListCommand)

    @command_error
    def run(self):
        from tabulate import tabulate
        apps = AppManager().list()
        wide = False

        match self.args.output:
            case 'wide':
                titles = App.table_title(True)
                wide = True
            case 'yaml':
                ...
            case 'json':
                ...
            case _:
                titles = App.table_title()
                wide = False

        if apps is not None and len(apps) > 0:
            apps[0].table_title()

        print(tabulate(
            [app.table_row(wide=wide) for app in apps],
            headers=titles,
        ))
