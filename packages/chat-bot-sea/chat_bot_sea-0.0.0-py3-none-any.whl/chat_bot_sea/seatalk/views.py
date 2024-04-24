from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView

from .function_interactive import *
from .models import *
from .services import *

EVENT_VERIFICATION = "event_verification"
NEW_BOT_SUBSCRIBER = "new_bot_subscriber"
MESSAGE_FROM_BOT_SUBSCRIBER = "message_from_bot_subscriber"
INTERACTIVE_MESSAGE_CLICK = "interactive_message_click"
BOT_ADDED_TO_GROUP_CHAT = "bot_added_to_group_chat"
BOT_REMOVED_FROM_GROUP_CHAT = "bot_removed_from_group_chat"
NEW_MENTIONED_MESSAGE_RECEIVED_FROM_GROUP_CHAT = "new_mentioned_message_received_from_group_chat"


class BotView(APIView):
    def get(self, request, format=None):
        return Response(status=HTTP_200_OK)

    def post(self, request, format=None):
        if 'Signature' in request.headers:
            body = request.body
            data = request.data
            event_type = data.get("event_type")
            app = App.objects.get(id=data.get("app_id"))
            signing_secret = bytes(app.signing_secret, 'utf-8')

            if is_valid_signature(
                signing_secret=signing_secret,
                body=body,
                signature=request.headers.get('Signature'),
            ):
                if event_type == EVENT_VERIFICATION:
                    return Response(
                        data={'seatalk_challenge': data['event']['seatalk_challenge']}, status=HTTP_200_OK)
                elif event_type == NEW_MENTIONED_MESSAGE_RECEIVED_FROM_GROUP_CHAT:
                    # input
                    group_id = data.get("event").get("group_id")
                    seatalk_id = data.get("event").get(
                        "message").get("sender").get("seatalk_id")
                    message = data.get("event").get(
                        "message").get("text").get("plain_text")

                    # react
                    if '/start' in message:
                        send_to_group_though_app(app_name="Gau Gau", group_id=group_id).interactive(
                            title='🐶 Hello, may I can assist you today?', description='Please select your tools:', content=start_interactive())

                    # elif '/match' in user_message:
                    #     read_url(user_message)
                else:
                    return Response(
                        data={'message': 'Event type not exist. Abort'}, status=HTTP_400_BAD_REQUEST)
            else:
                return Response(
                    data={'message': 'Failed to validate the signature. Aborted'}, status=HTTP_400_BAD_REQUEST)
        else:
            return Response(
                data={'message': 'There is no signature in the header. Aborted'}, status=HTTP_400_BAD_REQUEST)
            #         elif event_type == NEW_BOT_SUBSCRIBER:
            #             # fill with your own code
            #             pass
            #         elif event_type == MESSAGE_FROM_BOT_SUBSCRIBER:
            #             # fill with your own code
            #             pass
            #         elif event_type == INTERACTIVE_MESSAGE_CLICK:
            #             # get events
            #             value = json.loads(data.get("event").get("value").replace("\'", "\""))
            #             # choose group, button
            #             button = value.get("type")
            #             group_id = value.get("group_id")
            #             ufunc = UserFunction(group_id=group_id)
            #             # choose function
            #             dict_button = {
            #                 'Search News': ufunc.search_news,
            #                 'Read News': ufunc.rag_news,
            #             }
            #             # run
            #             dict_button[button]()

            #             return Response(status=HTTP_200_OK)
            #         elif event_type == BOT_ADDED_TO_GROUP_CHAT:
            #             # fill with your own code
            #             pass
            #         elif event_type == BOT_REMOVED_FROM_GROUP_CHAT:
            #             # fill with your own code
            #             pass
