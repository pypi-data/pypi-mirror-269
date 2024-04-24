import datetime
import threading

import flask
from flask import Flask, Blueprint

from everai.app.app import App
from everai.app.context import service_context
from everai.autoscaling import Factors


def register_autoscaling_handler(flask_app: Flask, app: App):
    assert hasattr(app.autoscaling_policy, 'decide')
    decide = getattr(app.autoscaling_policy, 'decide')
    assert callable(decide)

    everai_blueprint = Blueprint('everai-autoscaling', __name__, url_prefix='/-everai-')

    @everai_blueprint.route('/autoscaling', methods=['POST'])
    def autoscaling():
        data = flask.request.data

        try:
            factors = Factors.from_json(data)
        except Exception as e:
            return f'Bad request, {e}', 400

        try:
            with service_context(app.runtime.context()):
                result = decide(factors)
        except Exception as e:
            return f'Internal Server Error, {e}', 500

        return flask.Response(result.json(), mimetype='application/json')

    flask_app.register_blueprint(everai_blueprint)
    print(f'handler is /-everai-/autoscaling')
