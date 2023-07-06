from flask import request
from config.extension import socketio
from flask_socketio import ConnectionRefusedError, emit

from src.ChatApp.model.ChatHistoryModel import ChatHistory
from src.ChatApp.model.ConversationModel import Conversation
from src.UserApp.model.UserModel import UserSession
from src.SharedServices.Authentication import Auth


@socketio.on('connect')
def handleConnect(payload):
    print(f"payload --> {payload}, {request.sid}")
    if payload.get('token', None):
        data = Auth.decodeToken(payload.get('token', ''))
        print(f"data --> {data}")
        if data.get('token'):
            userSession = UserSession.getUserSessionTokenByUserId(data.get('user_id', None))
            if userSession:
                userSession.update({'session_token': request.sid})
            else:
                userSession = UserSession({'id_user': data.get('user_id', None), 'session_token': request.sid})
                userSession.save()
            response = {
                "is_connect": True,
                "is_session_added": True
            }
            emit('connected', response)
        else:
            response = {
                "is_connect": True,
                "is_session_added": False
            }
            emit('connected', response)
    else:
        response = {
            "is_connect": True,
            "is_session_added": False
        }
        emit('connected', response)


@socketio.on('message')
def handleMessage(payload):
    print(f"handleMessage --> {payload}")
    conversation = Conversation.getUserConversationsById(payload.get('conversation_id', None))
    if conversation:
        chatHistory = ChatHistory({
            'id_conversation': conversation.id_conversation,
            'id_sender': payload.get('user_id', None),
            'message': payload.get('message', None)
        })
        chatHistory.save()
    else:
        conversation = Conversation(
            {
                'id_user_one': payload.get('user_id', None),
                'id_user_two': payload.get('participant_id', None)
            }
        )
        conversation.save()
        chatHistory = ChatHistory({
            'id_conversation': conversation.id_conversation,
            'id_sender': payload.get('user_id', None),
            'message': payload.get('message', None)
        })
        chatHistory.save()
    userSession = UserSession.getUserSessionTokenByUserId(payload.get('participant_id', None))
    if userSession:
        sessionId = userSession.session_token
        emit(
            'new_message',
            {'user_id': payload.get('user_id', None), 'message': payload.get('message', None)},
            to=sessionId
        )
