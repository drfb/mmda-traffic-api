from xml.etree import ElementTree


class Feed:
    data = {}

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

        highway = self.data.get(highway_key)
        if not highway:
            self.data[highway_key] = highway = {
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

    def traffic(self, highway=None, segment=None, direction=None):
        if highway:
            return highway.get('segments')
        elif segment:
            traffic = segment.get('traffic')
            if direction:
                return traffic.get(direction)
            return traffic
        elif direction:
            data = self.data.copy()
            for key, highway in data.items():
                for key, segment in highway.get('segments').items():
                    traffic = segment.get('traffic')
                    traffic_in_one_direction = traffic.get(direction)
                    segment['traffic'] = traffic_in_one_direction
            return data
        return self.data

    def highways(self):
        highway_keys = self.data.keys()
        highways = []
        for key in highway_keys:
            highways.append({
                'id': key,
                'label': self._parse_name(key),
            })
        return highways

    def get_highway(self, highway_id):
        return self.data.get(highway_id)

    def segments(self, highway):
        segments = []
        for key, segment in highway.get('segments').items():
            segments.append({
                'id': key,
                'label': self._parse_name(key),
            })
        return segments

    def get_segment(self, segment_id):
        for key, highway in self.data.items():
            segments = highway.get('segments')
            if segment_id in segments.keys():
                return segments.get(segment_id)
