from flask_marshmallow import Schema
from flask_marshmallow.fields import fields
from src.SharedServices.MainService import MainService, FileByte, DateTimeField
from config.extension import db
from werkzeug.security import generate_password_hash, check_password_hash


class UserImage(db.Model):
    __table_args__ = ({"schema": "public"})
    __tablename__ = 'user_image'

    id_user_image = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    file_name = db.Column(db.String(80), nullable=True)
    file = db.Column(db.LargeBinary, nullable=True)
    created_at = db.Column(db.DateTime, default=MainService.getDateTimeNow(), nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"Id: {self.id_user_image}"

    def __init__(self, data):
        self.file_name = data.get('file_name', None)
        self.file = data.get('file', None)

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
    def getUserImageById(Id):
        try:
            result = UserImage.query.filter(UserImage.id_user_image == Id).first()
        except Exception as e:
            print(f"Query exception --> {e}")
            result = None
        finally:
            db.session.remove()
        return result


class User(db.Model):
    # __bind_key__ = 'chat_app_db'
    __table_args__ = ({"schema": "public"})
    __tablename__ = 'user'

    id_user = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=True)
    last_name = db.Column(db.String(80), nullable=True)
    id_user_image = db.Column(db.Integer, db.ForeignKey('public.user_image.id_user_image'), nullable=True)
    username = db.Column(db.String(100), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    mobile = db.Column(db.String(20), unique=True, nullable=True)
    password = db.Column(db.String(200), nullable=True)
    is_online = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_verify = db.Column(db.Boolean, default=False, nullable=False)
    is_delete = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=MainService.getDateTimeNow(), nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)
    user_image = db.relationship('UserImage', backref='user', lazy='joined')

    def __repr__(self):
        return f"Id: {self.id_user}"

    def __init__(self, data):
        self.first_name = data.get('first_name', None)
        self.last_name = data.get('last_name', None)
        self.id_user_image = data.get('id_user_image', None)
        self.username = data.get('username', None)
        self.email = data.get('email', None)
        self.password = generate_password_hash(data.get('password', ''))

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

    def checkPassword(self, password: str):
        return check_password_hash(self.password, password)

    @staticmethod
    def getUsers():
        try:
            result = User.query.order_by(User.id_user.desc()).all()
        except Exception as e:
            print(f"Query exception --> {e}")
            result = None
        finally:
            db.session.remove()
        return result

    @staticmethod
    def getUserById(Id):
        try:
            result = User.query.filter(User.id_user == Id).first()
        except Exception as e:
            print(f"Query exception --> {e}")
            result = None
        finally:
            db.session.remove()
        return result

    @staticmethod
    def getUserByUsername(value):
        try:
            result = User.query.filter(User.username == value).first()
        except Exception as e:
            print(f"Query exception --> {e}")
            result = None
        finally:
            db.session.remove()
        return result

    @staticmethod
    def getUserByEmail(value):
        try:
            result = User.query.filter(User.email == value).first()
        except Exception as e:
            print(f"Query exception --> {e}")
            result = None
        finally:
            db.session.remove()
        return result

    @staticmethod
    def getUserByMobile(value):
        try:
            result = User.query.filter(User.mobile == value).first()
        except Exception as e:
            print(f"Query exception --> {e}")
            result = None
        finally:
            db.session.remove()
        return result


class UserSession(db.Model):
    # __bind_key__ = 'chat_app_db'
    __table_args__ = ({"schema": "public"})
    __tablename__ = 'user_session'

    id_user_session = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('public.user.id_user'), nullable=True)
    session_token = db.Column(db.String(100), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=MainService.getDateTimeNow(), nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)
    user = db.relationship('User', backref='user_session', lazy='joined')

    def __repr__(self):
        return f"Id: {self.id_user}"

    def __init__(self, data):
        self.id_user = data.get('id_user', None)
        self.session_token = data.get('session_token', None)
        self.updated_at = MainService.getDateTimeNow()

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
    def getUserSessionTokenByUserId(Id):
        try:
            result = UserSession.query.filter(UserSession.id_user == Id).first()
        except Exception as e:
            print(f"Query exception --> {e}")
            result = None
        finally:
            db.session.remove()
        return result


class UserImageSchema(Schema):
    id_user_image = fields.Int()
    file_name = fields.String()
    file = FileByte()
    created_at = fields.DateTime()


class UserSchema(Schema):
    id_user = fields.Int()
    first_name = fields.String()
    last_name = fields.String()
    user_image = fields.Nested(UserImageSchema())
    username = fields.String()
    email = fields.String()
    mobile = fields.Int()
    is_online = fields.Boolean()
    is_active = fields.Boolean()
    is_verify = fields.Boolean()
    created_at = fields.DateTime()


class UserSessionSchema(Schema):
    id_user_session = fields.Int()
    user = fields.Nested(UserSchema())
    session_token = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
