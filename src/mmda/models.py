from xml.etree import ElementTree


class Feed:
    traffic = {}

    def __init__(self, content):
        root = ElementTree.fromstring(content)
        channel = root.find('channel')
        items = channel.findall('item')

        for item in items:
            title = item.find('title').text
            description = item.find('description').text
            pub_date = item.find('pubDate').text
            highway, segment, direction = self._parse_title(title)

            _highway = self.traffic.get(highway)
            if not _highway:
                self.traffic[highway] = _highway = {
                    'label': highway,
                    'segments': {},
                }

            _segment = _highway.get('segments').get(segment)
            if not _segment:
                _highway.get('segments')[segment] = _segment = {
                    'label': segment,
                    'traffic': {},
                }

            traffic = _segment.get('traffic')
            traffic[direction] = {
                'label': direction,
                'status': description,
                'updated_at': pub_date,
            }

    def _parse_title(self, title):
        parts = title.split('-')
        return parts[0], parts[1], parts[2]

    def items(self):
        return [self.traffic]
