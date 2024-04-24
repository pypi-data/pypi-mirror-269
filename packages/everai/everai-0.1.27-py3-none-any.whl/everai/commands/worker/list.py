import typing

from everai.app import App, AppManager
from everai.commands.command import ClientCommand, command_error
from argparse import _SubParsersAction
from everai.commands.app import app_detect, add_app_name_to_parser


class ListCommand(ClientCommand):
    def __init__(self, args):
        self.args = args

    @staticmethod
    @app_detect(optional=True)
    def setup(parser: _SubParsersAction, app: typing.Optional[App]):
        list_parser = parser.add_parser("list", help="List workers of app")
        add_app_name_to_parser(list_parser, app)

        list_parser.set_defaults(func=ListCommand)

    @command_error
    def run(self):
        AppManager().list_worker(app_name=self.args.app_name)
