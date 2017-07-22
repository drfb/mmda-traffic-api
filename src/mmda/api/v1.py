from flask import Blueprint, g, jsonify

from mmda.exceptions import ResourceNotFound
from mmda.decorators import (
    load_mmda_api, validate_highway,
    validate_segment, validate_filters,
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


@blueprint.route('/highways')
@load_mmda_api
def highways():
    return jsonify(g.feed.get_highways())


@blueprint.route('/segments')
@load_mmda_api
def segments():
    return jsonify(g.feed.get_segments())


@blueprint.route('/highways/<highway_id>/segments')
@load_mmda_api
@validate_highway
def highway_segments(highway_id):
    return jsonify(
        g.feed.get_segments_by_highway(g.highway)
    )


@blueprint.route('/traffic')
@load_mmda_api
@validate_filters
def traffic():
    return jsonify(
        g.feed.get_traffic(filters=g.filters)
    )


@blueprint.route('/highways/<highway_id>/traffic')
@load_mmda_api
@validate_highway
@validate_filters
def highway_traffic(highway_id):
    return jsonify(
        g.feed.get_traffic_by_highway(
            g.highway,
            filters=g.filters
        )
    )


@blueprint.route('/segments/<segment_id>/traffic')
@load_mmda_api
@validate_segment
@validate_filters
def segment_traffic(segment_id):
    return jsonify(
        g.feed.get_traffic_by_segment(
            g.segment,
            filters=g.filters
        )
    )
