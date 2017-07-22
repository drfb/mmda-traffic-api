from functools import wraps

from flask import g, request
import requests

from mmda import config
from mmda.exceptions import ResourceNotFound
from mmda.repository import Feed


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


def validate_filters(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        filters = {}
        direction = request.args.get('direction')
        status = request.args.get('status')

        if direction:
            direction = direction.upper()

            if direction not in ['NB', 'SB']:
                raise ResourceNotFound('Direction')

            filters['direction'] = direction

        if status:
            status = status.upper()

            if status and status not in ['L', 'ML', 'M', 'MH', 'H']:
                raise ResourceNotFound('Status')

            filters['status'] = status

        g.filters = filters

        return func(*args, **kwargs)
    return wrapper
