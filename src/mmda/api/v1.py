from functools import wraps

from flask import Blueprint, g, jsonify
import requests

from mmda import config
from mmda.models import Feed


blueprint = Blueprint('v1', __name__)


def load_mmda_api(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = requests.get(config.MMDA_API_URL)
        g.feed = Feed(response.content)
        return func(*args, **kwargs)
    return wrapper


@blueprint.route('/')
def index():
    return jsonify(
        name='TV5-MMDA Traffic Monitoring API',
        version='v1',
    )


@blueprint.route('/feed')
@load_mmda_api
def feed():
    return jsonify(g.feed.items())
