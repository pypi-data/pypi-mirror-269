import typing

from everai.app import App, AppManager
from everai.commands.command import ClientCommand, command_error, ListDisplayer
from argparse import _SubParsersAction
from everai.commands.app import app_detect, add_app_name_to_parser
from everai.worker import Worker


class ListCommand(ClientCommand):
    def __init__(self, args):
        self.args = args

    @staticmethod
    @app_detect(optional=True)
    def setup(parser: _SubParsersAction, app: typing.Optional[App]):
        list_parser = parser.add_parser('list', aliases=['ls'], help='List workers of app')
        add_app_name_to_parser(list_parser, app)
        ListDisplayer.add_output_to_parser(list_parser)
        list_parser.add_argument('--all', '-a', action='store_true',
                                 help='show all workers, include deleted and errors')
        list_parser.add_argument('--recent-days', '-d', nargs='?', type=int,
                                 default=2,
                                 help='show not running workers who is created in recent days')

        list_parser.set_defaults(func=ListCommand)

    @command_error
    def run(self):
        workers = AppManager().list_worker(app_name=self.args.app_name)
        ListDisplayer[Worker](workers).show_list(self.args.output)
