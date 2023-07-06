from flask_marshmallow import Schema
from flask_marshmallow.fields import fields
from config.extension import db
from src.UserApp.model.UserModel import UserSchema
from src.services.MainService import MainService, DateTimeField


class Conversation(db.Model):
    __table_args__ = ({"schema": "public"})
    __tablename__ = 'conversation'

    id_conversation = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    id_user_one = db.Column(db.Integer, db.ForeignKey('public.user.id_user'), nullable=True)
    id_user_two = db.Column(db.Integer, db.ForeignKey('public.user.id_user'), nullable=True)
    created_at = db.Column(db.DateTime, default=MainService.getDateTimeNow(), nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)
    user_one = db.relationship('User', foreign_keys='Conversation.id_user_one', backref='conversation_user_one',
                               lazy='joined')
    user_two = db.relationship('User', foreign_keys='Conversation.id_user_two', backref='conversation_user_two',
                               lazy='joined')

    def __repr__(self):
        return f"Id: {self.id_conversation}"

    def __init__(self, data):
        self.id_user_one = data.get('id_user_one', None)
        self.id_user_two = data.get('id_user_two', None)
        self.updated_at = MainService.getCurrentTimeStamp()

    def update(self, data):
        for key, item in data.items():
            if key == 'updated_at':
                self.updated_at = MainService.getDateTimeNow()
            setattr(self, key, item)
        self.save()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def getUserConversationsById(Id):
        try:
            result = Conversation.query.filter(Conversation.id_conversation == Id).first()
        except Exception as e:
            print(f"Query exception --> {e}")
            result = None
        finally:
            db.session.remove()
        return result

    @staticmethod
    def getUserConversationsByUserId(Id):
        try:
            results = Conversation.query \
                .filter((Conversation.id_user_one == Id) | (Conversation.id_user_two == Id)) \
                .order_by(Conversation.updated_at.desc())
        except Exception as e:
            print(f"Query exception --> {e}")
            results = None
        finally:
            db.session.remove()
        return results


class ConversationSchema(Schema):
    id_conversation = fields.Int()
    user_one = fields.Nested(UserSchema())
    user_two = fields.Nested(UserSchema())
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
