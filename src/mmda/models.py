from xml.etree import ElementTree


class Feed:
    traffic = {}

    def __init__(self, content):
        root = ElementTree.fromstring(content)
        channel = root.find('channel')
        items = channel.findall('item')

        for item in items:
            self._parse_item(item)

    def _parse_item(self, item):
        title = item.find('title').text
        description = item.find('description').text
        pub_date = item.find('pubDate').text
        highway_key, segment_key, direction_key = self._parse_title(title)

        highway = self.traffic.get(highway_key)
        if not highway:
            self.traffic[highway_key] = highway = {
                'label': self._parse_name(highway_key),
                'segments': {},
            }

        segment = highway.get('segments').get(segment_key)
        if not segment:
            highway.get('segments')[segment_key] = segment = {
                'label': self._parse_name(segment_key),
                'traffic': {},
            }

        traffic = segment.get('traffic')
        traffic[direction_key] = {
            'label': self._parse_direction(direction_key),
            'status': self._parse_status(description),
            'updated_at': pub_date,
        }

    def _parse_title(self, title):
        parts = title.split('-')
        last_index = len(parts) - 1

        highway = parts[0]
        segment = '-'.join(parts[1:last_index])
        direction = parts[last_index]

        return highway, segment, direction

    def _parse_name(self, name):
        name = name.replace('_', ' ')
        name = name.replace('AVE.', 'Avenue')
        name = name.replace('BLVD.', 'Boulevard')

        if name not in ['EDSA', 'U.N.']:
            name = name.title()

        return name

    def _parse_direction(self, direction):
        directions = {
            'NB': 'Northbound',
            'SB': 'Southbound',
        }
        return directions.get(direction)

    def _parse_status(self, status):
        statuses = {
            'L': 'Light',
            'ML': 'Light to Moderate',
            'M': 'Moderate',
            'MH': 'Moderate to Heavy',
            'H': 'Heavy',
        }
        return statuses.get(status)

    def items(self):
        return [self.traffic]
