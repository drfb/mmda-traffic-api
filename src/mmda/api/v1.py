from flask import Blueprint, g, jsonify

from mmda.exceptions import ResourceNotFound
from mmda.decorators import (
    load_mmda_api, validate_highway,
    validate_segment, validate_direction,
)


blueprint = Blueprint('v1', __name__)


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
    return jsonify(
        g.feed.traffic(
            direction=g.direction
        )
    )


@blueprint.route('/highways')
@load_mmda_api
def highways():
    return jsonify(g.feed.highways())


@blueprint.route('/highways/<highway_id>/traffic')
@load_mmda_api
@validate_highway
def highway_traffic(highway_id):
    return jsonify(
        g.feed.traffic(
            highway=g.highway
        )
    )


@blueprint.route('/highways/<highway_id>/traffic/<direction>')
@load_mmda_api
@validate_highway
@validate_direction
def highway_traffic_in_on_direction(highway_id, direction):
    return jsonify(
        g.feed.traffic(
            highway=g.highway,
            direction=g.direction
        )
    )


@blueprint.route('/highways/<highway_id>/segments')
@load_mmda_api
@validate_highway
def segments(highway_id):
    return jsonify(
        g.feed.segments(g.highway)
    )


@blueprint.route('/segments/<segment_id>/traffic')
@load_mmda_api
@validate_segment
def segment_traffic(segment_id):
    return jsonify(
        g.feed.traffic(
            segment=g.segment
        )
    )


@blueprint.route('/segments/<segment_id>/traffic/<direction>')
@load_mmda_api
@validate_segment
@validate_direction
def segment_traffic_in_one_direction(segment_id, direction):
    return jsonify(
        g.feed.traffic(
            segment=g.segment,
            direction=g.direction
        )
    )
