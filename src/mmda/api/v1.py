from functools import wraps

from flask import Blueprint, g, jsonify
import requests

from mmda import config
from mmda.utils import parse_mmda_rss


blueprint = Blueprint('v1', __name__)


def load_mmda_api(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = requests.get(config.MMDA_API_URL)
        g.mmda = {
            'status_code': response.status_code,
            'data': parse_mmda_rss(response.content)
        }
        return func(*args, **kwargs)
    return wrapper


@blueprint.route('/')
def index():
    return jsonify(
        app_name='MMDA Traffic API v1',
    )
