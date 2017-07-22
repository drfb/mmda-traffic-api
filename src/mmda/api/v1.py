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


def validate_highway(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        highway_id = kwargs.get('highway_id')
        g.highway = g.feed.get_highway(highway_id)
        if not g.highway:
            raise ResourceNotFound('Highway')
        return func(*args, **kwargs)
    return wrapper


def validate_segment(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        segment_id = kwargs.get('segment_id')
        g.segment = g.feed.get_segment(segment_id)
        if not g.segment:
            raise ResourceNotFound('Segment')
        return func(*args, **kwargs)
    return wrapper


def validate_direction(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        directions = ['NB', 'SB']
        g.direction = kwargs.get('direction').upper()
        if g.direction not in directions:
            raise ResourceNotFound('Direction')
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


@blueprint.route('/traffic/<direction>')
@load_mmda_api
@validate_direction
def traffic_in_one_direction(direction):
    return jsonify(g.feed.traffic(direction=g.direction))


@blueprint.route('/highways')
@load_mmda_api
def highways():
    return jsonify(g.feed.highways())


@blueprint.route('/highways/<highway_id>/traffic')
@load_mmda_api
@validate_highway
def highway_traffic(highway_id):
    return jsonify(g.feed.traffic(highway=g.highway))


@blueprint.route('/highways/<highway_id>/segments')
@load_mmda_api
@validate_highway
def segments(highway_id):
    return jsonify(g.feed.segments(g.highway))


@blueprint.route('/segments/<segment_id>/traffic')
@load_mmda_api
@validate_segment
def segment_traffic(segment_id):
    return jsonify(g.feed.traffic(segment=g.segment))


@blueprint.route('/segments/<segment_id>/traffic/<direction>')
@load_mmda_api
@validate_segment
@validate_direction
def segment_traffic_in_one_direction(segment_id, direction):
    return jsonify(g.feed.traffic(segment=g.segment, direction=g.direction))
