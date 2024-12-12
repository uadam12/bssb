from json import dumps, loads
from django.http import HttpRequest, HttpResponse
from django.contrib.messages import get_messages


class ToastMiddlewere:
    def __init__(self, get_response) -> None:
        self.get_response = get_response
        
    def __call__(self, request:HttpRequest):
        response:HttpResponse = self.get_response(request)

        if (
            'HX-Request' not in request.headers
            or 300 <= response.status_code < 400
        ): return response
        
        messages = [
            {
                'message': message.message, 
                'tags': message.tags
            } for message in get_messages(request)
        ]
        
        if not messages: return response

        trigger:str = response.headers.get('HX-Trigger', None)
        
        if trigger is None:
            trigger = {}
        elif trigger.startswith('{'):
            trigger = loads(trigger)
        else:
            trigger = {
                trigger: True
            }

        trigger['messages'] = messages
        response.headers['HX-Trigger'] = dumps(trigger)

        return response