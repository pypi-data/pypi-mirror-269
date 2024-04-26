import typing

from everai.commands.command import ClientCommand, command_error
from argparse import _SubParsersAction

from everai.app import App
from everai.app.app_manager import AppManager
from everai.commands.app import app_detect

route_name_description = ('Globally unique route name. '
                          'By default, it is same with the app name. '
                          'Once the application name conflicts, route-name needs to be set explicitly.')

rollout_notify = 'this operation will trigger the worker rollout'


class UpgradeCommand(ClientCommand):
    parser: _SubParsersAction = None

    def __init__(self, args):
        self.args = args

    @staticmethod
    def setup(parser: _SubParsersAction):
        upgrade_parser = parser.add_parser("upgrade", help="Upgrade an app")
        upgrade_parser.add_argument('--autoscaling-policy', action='store_true',
                                    help="Upgrade the autoscaling policy only")
        upgrade_parser.add_argument('--resource-requests', action='store_true',
                                    help=f'Upgrade the resource requests only, {rollout_notify}')
        upgrade_parser.add_argument('--volume-requests', action='store_true',
                                    help=f'Upgrade the volume requests only, {rollout_notify}')
        upgrade_parser.add_argument('--secret-requests', action='store_true',
                                    help=f'Upgrade the secret requests only, {rollout_notify}')
        upgrade_parser.add_argument('--image', action='store_true',
                                    help=f'Upgrade the image only, {rollout_notify}')
        upgrade_parser.add_argument('--all', action='store_true',
                                    help=f'Upgrade all of the settings, {rollout_notify}')

        upgrade_parser.set_defaults(func=UpgradeCommand)
        UpgradeCommand.parser = upgrade_parser

    @command_error
    @app_detect(optional=False)
    def run(self, app: typing.Optional[App] = None):
        affected = 0
        app_manager = AppManager()

        if self.args.autoscaling_policy or self.args.all:
            app_manager.setup_autoscaling_policy(app.name, app.autoscaling_policy)
            affected += 1

        if self.args.resource_requests or self.args.all:
            assert self.args.resource_requests is not None
            app_manager.setup_resource_requests(app.name, app.resource_requests)
            affected += 1

        if self.args.volume_requests or self.args.all:
            app_manager.setup_volume_requests(app.name, app.volume_requests)
            affected += 1

        if self.args.secret_requests or self.args.all:
            app_manager.setup_secret_requests(app.name, app.secret_requests)
            affected += 1

        if self.args.image or self.args.all:
            app_manager.setup_image(app.name, app.image)
            affected += 1

        if affected == 0:
            UpgradeCommand.parser.print_help()
            exit(1)
