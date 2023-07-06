from flask import Blueprint
from src.ChatApp.model.ChatHistoryModel import ChatHistory, ChatHistorySchema
from src.ChatApp.model.ConversationModel import Conversation, ConversationSchema
from src.services.Authentication import Auth
from src.services.MainService import MainService, StatusType
from src.ChatApp.ChatService import *

ChatApi = Blueprint('chat view', __name__)


@ChatApi.route('/conversations', methods=['GET'])
@Auth.auth_required
def conversations(current_user, langCode):
    conversation = Conversation.getUserConversationsByUserId(current_user.id_user)
    conversationSchema = ConversationSchema()
    conversationData = conversationSchema.dump(conversation, many=True)
    response = {
        "status": StatusType.success.value,
        "data": {"conversations": conversationData},
        "message": MainService.message(langCode).data_sent.value
    }
    return MainService.response(data=response, status_code=200)


@ChatApi.route('/chat-history/<id>', methods=['GET'])
@Auth.auth_required
def chatHistory(current_user, langCode, id):
    chatHistories = ChatHistory.getUserChatHistoryByIdConversation(id)
    chatHistorySchema = ChatHistorySchema()
    chatHistoryData = chatHistorySchema.dump(chatHistories, many=True)
    response = {
        "status": StatusType.success.value,
        "data": {"chat_history": chatHistoryData},
        "message": MainService.message(langCode).data_sent.value
    }
    return MainService.response(data=response, status_code=200)


