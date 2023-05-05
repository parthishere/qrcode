

# class ReloadConsumer(WebsocketConsumer):
#     def connect(self):
#         self.group_name = self.scope['user']
#         print(self.group_name)  # use this for debugging not sure what the scope returns

#         # Join group
#         async_to_sync(self.channel_layer.group_add)(
#             self.group_name,
#             self.channel_name
#         )
#         self.accept()

#     def disconnect(self, close_code):
#         # Leave group
#         async_to_sync(self.channel_layer.group_discard)(
#             self.group_name,
#             self.channel_name
#         )

#     def reload_page(self, event):
#         # Send message to WebSocket
#         self.send(text_data=json.dumps({
#             'reload': True
#         }))
#         self.disconnect()