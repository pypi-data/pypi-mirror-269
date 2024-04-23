import flask
from flask import Flask, Blueprint

from everai.autoscaling import AutoScalingPolicy, Factors


def register_autoscaling_handler(flask_app: Flask, policy: AutoScalingPolicy):
    assert hasattr(policy, 'decide')
    decide = getattr(policy, 'decide')
    assert callable(decide)

    everai_blueprint = Blueprint('everai-autoscaling', __name__, url_prefix='/-everai-')

    @everai_blueprint.route('/autoscaling', methods=['POST'])
    def autoscaling():
        data = flask.request.json
        if not isinstance(data, dict):
            return 'Bad request, a json body is required', 400

        try:
            factors = Factors.from_json(data)
        except Exception as e:
            return f'Bad request, {e}', 400

        try:
            result = decide(factors)
        except Exception as e:
            return f'Internal Server Error, {e}', 500

        return flask.jsonify(result)

    flask_app.register_blueprint(everai_blueprint)
