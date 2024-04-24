import typing
from argparse import _SubParsersAction

from everai.app import App
from everai.app.app_manager import AppManager
from everai.commands.command import command_error, ClientCommand

from everai.commands.app import app_detect, add_app_name_to_parser

route_name_description = ('Globally unique route name. '
                          'By default, it is same with the app name. '
                          'Once the application name conflicts, route-name needs to be set explicitly.')


class CreateCommand(ClientCommand):
    def __init__(self, args):
        self.args = args

    @staticmethod
    @app_detect(optional=True)
    def setup(parser: _SubParsersAction, app: typing.Optional[App]):
        create_parser = parser.add_parser("create", help="Create an app")
        create_parser.add_argument('--route-name', '-r', help=route_name_description, type=str)

        add_app_name_to_parser(create_parser, app, arg_name='name')
        # create_parser.add_argument('--ignore-scaffold', action='store_true',
        #                            help='let everai client do not scaffold, e.g. app2.py')

        create_parser.set_defaults(func=CreateCommand)

        CreateCommand.parser = create_parser

    @command_error
    def run(self):
        app = AppManager().create(app_name=self.args.name,
                                  app_route_name=self.args.route_name)
        print(app)
