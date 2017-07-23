from xml.etree import ElementTree


class Feed:
    """
    Feed Repository contains feed content from
    TV5-MMDA Traffic Monitoring API's feed, with
    helper functions to dissect and present data
    beautifully.
    """

    def __init__(self, content):
        """
        Parses content (xml string) from traffic feed API.
        """
        self.data = {}
        root = ElementTree.fromstring(content)
        channel = root.find('channel')
        items = channel.findall('item')

        for item in items:
            self._parse_item(item)

    def _parse_item(self, item):
        """
        Parses item into json objects
        """
        # Parse item data
        title = item.find('title').text
        description = item.find('description').text
        pub_date = item.find('pubDate').text
        highway_key, segment_key, direction_key = self._parse_title(title)

        # Parse highway
        highway = self.data.get(highway_key)
        if not highway:
            self.data[highway_key] = highway = {
                'label': self._parse_name(highway_key),
                'segments': {},
            }

        # Parse highway segment
        segment = highway.get('segments').get(segment_key)
        if not segment:
            highway.get('segments')[segment_key] = segment = {
                'label': self._parse_name(segment_key),
                'traffic': {},
            }

        # Parse traffic direction and data
        traffic = segment.get('traffic')
        traffic[direction_key] = {
            'label': self._parse_direction(direction_key),
            'status': self._parse_status(description),
            'updated_at': pub_date,
        }

    def _parse_title(self, title):
        """
        Parses item title. The title is composed
        of three parts, separated by a '-':
        HIGHWAY-SEGMENT-DIRECTION
        """
        parts = title.split('-')
        last_index = len(parts) - 1

        highway = parts[0]
        segment = '-'.join(parts[1:last_index])
        direction = parts[last_index]

        return highway, segment, direction

    def _parse_name(self, name):
        """
        Converts highway/segment ID into
        more human-readable text.
        """
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

    def _get_opposite_direction(self, direction):
        opposite_directions = {
            'NB': 'SB',
            'SB': 'NB',
        }
        return opposite_directions.get(direction)

    def _parse_status(self, status):
        statuses = {
            'L': 'Light',
            'ML': 'Light to Moderate',
            'M': 'Moderate',
            'MH': 'Moderate to Heavy',
            'H': 'Heavy',
        }
        return statuses.get(status)

    def _filter_segment_by(self, segment, direction=None, status=None):
        """
        Filters segment's traffic data.
        """
        # Filter by direction
        if direction:
            opposite_direction = self._get_opposite_direction(direction)
            traffic = segment.get('traffic')
            traffic.pop(opposite_direction)

        # Filter by status
        if status:
            status = self._parse_status(status)
            traffic = segment.get('traffic')
            directions = ['NB', 'SB']
            filtered_traffic = {}

            for direction in directions:
                traffic_direction = traffic.get(direction, {})

                if traffic_direction.get('status') == status:
                    filtered_traffic[direction] = traffic_direction

            if filtered_traffic:
                segment['traffic'] = filtered_traffic
            else:
                return None

        return segment

    def _filter_segments_by(self, segments, direction=None, status=None):
        """
        Filters a segment dict's traffic data
        by direction or status.
        """
        for key, segment in segments.items():
            if not self._filter_segment_by(
                segment,
                direction=direction,
                status=status
            ):
                del segments[key]

    def get_highways(self):
        """
        Lists all monitored highways.
        """
        highway_keys = self.data.keys()
        highways = {}

        for key in highway_keys:
            highways[key] = self._parse_name(key)

        return highways

    def get_highway(self, highway_id):
        """
        Returns a specific highway by highway_id.
        """
        return self.data.get(highway_id)

    def get_segments(self):
        """
        Lists all monitored highway segments.
        """
        segments = {}

        for highway_key, highway in self.data.items():
            for segment_key, segment in highway.get('segments').items():
                segments[segment_key] = self._parse_name(segment_key)

        return segments

    def get_segments_by_highway(self, highway):
        """
        Lists all monitered segments in
        a given highway.
        """
        segments = {}

        for key, segment in highway.get('segments').items():
            segments[key] = self._parse_name(key)

        return segments

    def get_segment(self, segment_id):
        """
        Returns a specific highway segment
        by segment_id.
        """
        for key, highway in self.data.items():
            segments = highway.get('segments')
            if segment_id in segments.keys():
                return segments.get(segment_id)

    def get_traffic(self, filters=None):
        """
        Returns traffic data of all segments
        in all highways.
        """
        traffic = self.data

        if filters:
            direction = filters.get('direction')
            status = filters.get('status')

            for key, highway in traffic.items():
                segments = highway.get('segments')
                self._filter_segments_by(
                    segments,
                    direction=direction,
                    status=status
                )

        return traffic

    def get_traffic_by_highway(self, highway, filters=None):
        """
        Returns traffic data of all segments
        in a specific highway.
        """
        if filters:
            direction = filters.get('direction')
            status = filters.get('status')

            segments = highway.get('segments')
            if not self._filter_segments_by(
                segments,
                direction=direction,
                status=status
            ):
                return {}

        return highway

    def get_traffic_by_segment(self, segment, filters=None):
        """
        Returns traffic data of a specific
        highway segment.
        """
        if filters:
            direction = filters.get('direction')
            status = filters.get('status')

            if not self._filter_segment_by(
                segment,
                direction=direction,
                status=status
            ):
                return {}

        return segment
