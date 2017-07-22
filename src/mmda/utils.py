from xml.etree import ElementTree


def _parse_item(item):
    return {
        'title': item.find('title').text,
        'description': item.find('description').text,
        'pubDate': item.find('pubDate').text,
        'guid': item.find('guid').text,
    }


def parse_mmda_rss(content):
    root = ElementTree.fromstring(content)
    channel = root.find('channel')
    items = channel.findall('item')
    return [_parse_item(item) for item in items]
