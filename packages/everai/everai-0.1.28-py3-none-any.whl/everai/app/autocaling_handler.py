import flask
from flask import Flask, Blueprint

from everai.autoscaling import AutoScalingPolicy, Factors
from everai.autoscaling.action import actions_to_json


def register_autoscaling_handler(flask_app: Flask, policy: AutoScalingPolicy):
    assert hasattr(policy, 'decide')
    decide = getattr(policy, 'decide')
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
            result = decide(factors)
        except Exception as e:
            return f'Internal Server Error, {e}', 500

        result_json_str = actions_to_json(result)
        return flask.Response(result_json_str, mimetype='application/json')

    flask_app.register_blueprint(everai_blueprint)
