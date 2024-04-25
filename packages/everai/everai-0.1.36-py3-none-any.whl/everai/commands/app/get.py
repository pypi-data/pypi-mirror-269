import typing

from everai.commands.command import ClientCommand, command_error
from everai.commands.app import app_detect, add_app_name_to_parser
from argparse import _SubParsersAction
from everai.app import App
from everai.app.app_manager import AppManager


class GetCommand(ClientCommand):
    def __init__(self, args):
        self.args = args

    @staticmethod
    @app_detect(optional=True)
    def setup(parser: _SubParsersAction, app: typing.Optional[App]):
        get_parser = parser.add_parser("get", help="Get app information")

        add_app_name_to_parser(get_parser, app, arg_name='name')

        get_parser.set_defaults(func=GetCommand)

    @command_error
    def run(self):
        resp = AppManager().get(self.args.name)
        print(resp)
