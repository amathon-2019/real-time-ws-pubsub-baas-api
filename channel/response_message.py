import json


class ResponseMessage:
    def __init__(self, receive_data):
        self.channel = receive_data['channel']

    def make_channel_list_data(self, channel_list):
        message_to_json = {
            'channel': self.channel,
            'channel_list': channel_list
        }
        return json.dumps(message_to_json)

    def make_ws_event_data(self, channel_name):
        message_to_json = {
            'channel': self.channel,
            'header': '',
            'body': ''
        }
        return json.dumps(message_to_json)

    # TMP: channel_data
