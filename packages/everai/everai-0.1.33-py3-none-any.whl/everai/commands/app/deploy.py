from everai.commands.command import ClientCommand, command_error
from argparse import _SubParsersAction

from everai.commands.app import app_detect
from everai.app import App, AppManager
from everai.logger.logger import getLogger

logger = getLogger(__name__)


class DeployCommand(ClientCommand):
    def __init__(self, args):
        self.args = args

    @staticmethod
    def setup(parser: _SubParsersAction):
        deploy_parser = parser.add_parser("deploy", help="Deploy an app to serving status")

        deploy_parser.set_defaults(func=DeployCommand)

    @command_error
    @app_detect(optional=False)
    def run(self, app: App):
        AppManager().deploy(app)
