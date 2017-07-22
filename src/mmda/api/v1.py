from flask import Blueprint, jsonify


blueprint = Blueprint('v1', __name__)


@blueprint.route('/')
def index():
    return jsonify(
        app_name='MMDA Traffic API v1',
    )
