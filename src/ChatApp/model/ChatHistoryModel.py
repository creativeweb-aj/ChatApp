from flask_marshmallow import Schema
from flask_marshmallow.fields import fields
from config.extension import db
from src.ChatApp.model.ConversationModel import ConversationSchema
from src.UserApp.model.UserModel import UserSchema
from src.SharedServices.MainService import MainService, DateTimeField


class ChatHistory(db.Model):
    __table_args__ = ({"schema": "public"})
    __tablename__ = 'chat_history'

    id_chat_history = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    message = db.Column(db.String(80), nullable=True)
    id_conversation = db.Column(db.Integer, db.ForeignKey('public.conversation.id_conversation'), nullable=True)
    id_sender = db.Column(db.Integer, db.ForeignKey('public.user.id_user'), nullable=True)
    sent_at = db.Column(db.DateTime, default=MainService.getDateTimeNow(), nullable=True)
    sender = db.relationship('User', backref='chat_history', lazy='joined')
    conversation = db.relationship('Conversation', backref='chat_history', lazy='joined')

    def __repr__(self):
        return f"Id: {self.id_chat_history}"

    def __init__(self, data):
        self.message = data.get('message', None)
        self.id_conversation = data.get('id_conversation', None)
        self.id_sender = data.get('id_sender', None)
        self.updated_at = MainService.getCurrentTimeStamp()

    def update(self, data):
        for key, item in data.items():
            if key == 'updated_at':
                self.updated_at = MainService.getCurrentTimeStamp()
            setattr(self, key, item)
        self.save()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def getUserChatHistoryByIdConversation(Id):
        try:
            results = ChatHistory.query \
                .filter(ChatHistory.id_conversation == Id) \
                .order_by(ChatHistory.sent_at.asc())
        except Exception as e:
            print(f"Query exception --> {e}")
            results = None
        finally:
            db.session.remove()
        return results


class ChatHistorySchema(Schema):
    id_chat_history = fields.Int()
    message = fields.String()
    sender = fields.Nested(UserSchema())
    conversation = fields.Nested(ConversationSchema())
    sent_at = fields.DateTime()
