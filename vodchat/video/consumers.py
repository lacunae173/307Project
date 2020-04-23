from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from channels.auth import get_user, logout
from django.contrib.auth.models import User
from .models import Comment, Video

class UpvoteConsumer(WebsocketConsumer):
    def connect(self):
        self.video_id = self.scope['url_route']['kwargs']['video_id']#!!!!!!!!!!!!!!!!
        self.video_group_name = 'vote_%d' % self.video_id
        # Join video group
        async_to_sync(self.channel_layer.group_add)(
            self.video_group_name,
            self.channel_name
        )
        
        user = self.scope['user']
        if user.is_authenticated:
          async_to_sync(self.channel_layer.group_add)(
              user.username,
              self.channel_name
          )

        self.accept()

    def disconnect(self, close_code):
        # Leave video group
        async_to_sync(self.channel_layer.group_discard)(
            self.video_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        comment_pk = text_data_json['comment_pk']
        comment = Comment.objects.get(pk=int(comment_pk))
        comment.vote = comment.vote + 1
        comment.save()

        # Send message to video group
        async_to_sync(self.channel_layer.group_send)(
            self.video_group_name,
            {
                'type': 'chat_message',
                'comment_pk': comment_pk,
                'vote': comment.vote
            }
        )
        

    # Receive message from video group
    def chat_message(self, event):
        comment_pk = event['comment_pk']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'comment_pk': comment_pk,
            'vote': event['vote']
        }))
    
    # Receive message from username group
    def logout_message(self, event):
        #self.send(text_data=json.dumps({
        #    'message': event['message']
        #}))
        self.close()


class VideoConsumer(WebsocketConsumer):
    def connect(self):
        self.video_id = self.scope['url_route']['kwargs']['video_id']#!!!!!!!!!!!!!!!!
        self.video_group_name = 'video_%d' % self.video_id
        # Join video group
        async_to_sync(self.channel_layer.group_add)(
            self.video_group_name,
            self.channel_name
        )
        
        user = self.scope['user']
        if user.is_authenticated:
          async_to_sync(self.channel_layer.group_add)(
              user.username,
              self.channel_name
          )

        self.accept()

    def disconnect(self, close_code):
        # Leave video group
        async_to_sync(self.channel_layer.group_discard)(
            self.video_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        time = text_data_json['time']#~~~~~~~~~~~~~
        user = self.scope['user']
        
        # if user.is_authenticated:
        #     message = user.username + ': ' + message ##possible to be changed
        # else:
        #     message = 'Anonymous: ' + message ##possible to be changed
        
        # Store message into database
        video = Video.objects.get(pk=int(self.video_id))
        comment = Comment(video=video, text=message, time=time, vote=0)
        comment.save()

        # Send message to video group
        async_to_sync(self.channel_layer.group_send)(
            self.video_group_name,
            {
                'type': 'chat_message',
                'id': comment.id,
                'message': message,
                'time': time
            }
        )
        

    # Receive message from video group
    def chat_message(self, event):
        message = event['message']
        time = event['time']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'id': event['id'],
            'message': message,
            'time': time
        }))
    
    # Receive message from username group
    def logout_message(self, event):
        #self.send(text_data=json.dumps({
        #    'message': event['message']
        #}))
        self.close()
