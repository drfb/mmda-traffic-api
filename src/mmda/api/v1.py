from functools import wraps

from flask import Blueprint, g, jsonify
import requests

from mmda import config
from mmda.models import Feed
from mmda.exceptions import ResourceNotFound


blueprint = Blueprint('v1', __name__)


def load_mmda_api(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = requests.get(config.MMDA_API_URL)
        g.feed = Feed(response.content)
        return func(*args, **kwargs)
    return wrapper


@blueprint.errorhandler(ResourceNotFound)
def handle_resource_error(error):
    return jsonify(error='{} not found.'.format(error.resource)), 404


@blueprint.route('/')
def index():
    return jsonify(
        name='TV5-MMDA Traffic Monitoring API',
        version='v1',
    )


@blueprint.route('/traffic')
@load_mmda_api
def traffic():
    return jsonify(g.feed.traffic())


@blueprint.route('/highways')
@load_mmda_api
def highways():
    return jsonify(g.feed.highways())


@blueprint.route('/highways/<highway_id>/traffic')
@load_mmda_api
def highway_traffic(highway_id):
    highway = g.feed.get_highway(highway_id)
    if not highway:
        raise ResourceNotFound('Highway')
    return jsonify(g.feed.traffic(highway=highway))


@blueprint.route('/highways/<highway_id>/segments')
@load_mmda_api
def segments(highway_id):
    highway = g.feed.get_highway(highway_id)
    if not highway:
        raise ResourceNotFound('Highway')
    return jsonify(g.feed.segments(highway))


@blueprint.route('/segments/<segment_id>/traffic')
@load_mmda_api
def segment_traffic(segment_id):
    segment = g.feed.get_segment(segment_id)
    if not segment:
        raise ResourceNotFound('Segment')
    return jsonify(g.feed.traffic(segment=segment))
