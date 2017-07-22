from functools import wraps

from flask import g
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


def validate_direction(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        directions = ['NB', 'SB']
        g.direction = kwargs.get('direction').upper()
        if g.direction not in directions:
            raise ResourceNotFound('Direction')
        return func(*args, **kwargs)
    return wrapper


def validate_status(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        statuses = ['L', 'ML', 'M', 'MH', 'H']
        g.status = kwargs.get('status').upper()
        if g.status not in statuses:
            raise ResourceNotFound('Status')
        return func(*args, **kwargs)
    return wrapper
