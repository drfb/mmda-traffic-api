class ResourceNotFound(Exception):
    def __init__(self, resource='Resource'):
        self.resource = resource
