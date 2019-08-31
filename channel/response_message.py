import json


def make_channel_data(channel_name, cnt, rpm):
    message_to_json = {
        'channel_name': channel_name,
        'cnt': cnt,
        'rpm': rpm
    }
    return json.dumps(message_to_json)

# TMP: channel_data
