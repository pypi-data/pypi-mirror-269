

def start_interactive():
    button_list = ['Read News', 'Search News', 'BD']

    return [
        {'element_type': 'button',
         'button': {
             'button_type': 'callback',
             'text': button,
         }} for button in button_list]


# class BotFunction:
#     def __init__(self, group_id: str):

        # def message_template(self, content: str = ''):
        #     return {
        #         'group_id': self.group_id,
        #         'message': {
        #             'tag': 'text',
        #             'text': {
        #                 'format': 1,  # markdown
        #                 'content': content,
        #             },
        #         }
        #     }

        # def post(self, message_body: dict = None):
        #     r = requests.post(self.end_point, json=message_body, headers=self.header)
        #     return r

        # def interact_button(self, name: str) -> dict:
        #     return {
        #         'element_type': 'button',
        #         'button': {
        #             'button_type': 'callback',
        #             'text': name,
        #             'value': str({
        #                 'group_id': self.group_id,
        #                 'type': name
        #             })
        #         }
        #     }

        # def interact_info(self, title: str = None, description: str = None) -> dict:
        #     if title:
        #         return {
        #             'element_type': 'title',
        #             'title': {'text': title}
        #         }
        #     if description:
        #         return {
        #             'element_type': 'description',
        #             'description': {'text': description}
        #         }
