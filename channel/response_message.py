import json


class ResponseMessage:
    def __init__(self, receive_data):
        self.channel = "channels"
        self.channel_name = receive_data['channel_name']

    def make_channel_list_data(self, channel_list):
        message_to_json = {
            'channel': self.channel,
            'channel_list': channel_list
        }
        return json.dumps(message_to_json)

    def make_ws_event_data(self, header, body):
        message_to_json = {
            'channel': self.channel_name,
            'header': header,
            'body': body
        }
        return json.dumps(message_to_json)

    # TMP: channel_data
