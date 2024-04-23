from everai.commands.command import ClientCommand, command_error
from argparse import _SubParsersAction
from everai.app.app_manager import AppManager


class ListCommand(ClientCommand):
    def __init__(self, args):
        self.args = args

    @staticmethod
    def setup(parser: _SubParsersAction):
        list_parser = parser.add_parser("list", help="List all apps")
        list_parser.set_defaults(func=ListCommand)

    @command_error
    def run(self):
        from tabulate import tabulate
        apps = AppManager().list()
        print(tabulate(
            [
                [app.name, app.status, app.created_at] for app in apps
            ],
            headers=["NAME", "CREATED_AT", "STATUS"]
        ))
