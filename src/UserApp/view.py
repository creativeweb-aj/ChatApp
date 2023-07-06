from flask import Blueprint, request
from src.UserApp.model.UserModel import User, UserImage, UserSchema
from src.services.Authentication import Auth
from src.services.MainService import MainService, StatusType

UserApi = Blueprint('user view', __name__)


@UserApi.route('/login', methods=['POST'])
def login():
    defaultLang = "en"
    if 'Accept-Language' in request.headers:
        langCode = request.headers.get('Accept-Language', defaultLang)
        if langCode is None or langCode == "":
            langCode = defaultLang
    else:
        langCode = defaultLang
    data = request.get_json()

    fields = ['email', 'password']
    errors = MainService.validation(fields, data)
    if errors:
        response = {
            "status": StatusType.error.value,
            "data": errors,
            "message": ""
        }
        return MainService.response(data=response, status_code=200)
    # check if user detail
    user = User.getUserByEmail(data.get('email', ''))
    if not user:
        response = {
            "status": StatusType.fail.value,
            "data": None,
            "message": MainService.message(langCode).invalid_credentials.value
        }
        return MainService.response(data=response, status_code=200)
    if not user.checkPassword(data.get('password')):
        response = {
            "status": StatusType.fail.value,
            "data": None,
            "message": MainService.message(langCode).password_not_match.value
        }
        return MainService.response(data=response, status_code=200)

    userSchema = UserSchema()
    userData = userSchema.dump(user)
    token = Auth.generate_token(userData.get('id_user', ''))
    response = {
        "status": StatusType.success.value,
        "data": {"token": str(token), "user": userData},
        "message": MainService.message(langCode).login_successfully.value
    }
    return MainService.response(data=response, status_code=200)


@UserApi.route('/signup', methods=['POST'])
def signup():
    defaultLang = "en"
    if 'Accept-Language' in request.headers:
        langCode = request.headers.get('Accept-Language', defaultLang)
        if langCode is None or langCode == "":
            langCode = defaultLang
    else:
        langCode = defaultLang
    data = request.get_json()

    fields = ['first_name', 'last_name', 'username', 'mobile', 'email', 'password']
    errors = MainService.validation(fields, data)
    if errors:
        response = {
            "status": StatusType.error.value,
            "data": errors,
            "message": ""
        }
        return MainService.response(data=response, status_code=200)
    # Check username
    user = User.getUserByUsername(data.get('username', ''))
    if user:
        response = {
            "status": StatusType.fail.value,
            "data": None,
            "message": MainService.message(langCode).username_exist.value
        }
        return MainService.response(data=response, status_code=200)
    # Check mobile
    user = User.getUserByMobile(data.get('mobile', ''))
    if user:
        response = {
            "status": StatusType.fail.value,
            "data": None,
            "message": MainService.message(langCode).mobile_exist.value
        }
        return MainService.response(data=response, status_code=200)
    # Check email
    user = User.getUserByEmail(data.get('email', ''))
    if user:
        response = {
            "status": StatusType.fail.value,
            "data": None,
            "message": MainService.message(langCode).email_exist.value
        }
        return MainService.response(data=response, status_code=200)
    user = User(data)
    user.save()
    response = {
        "status": StatusType.success.value,
        "data": None,
        "message": MainService.message(langCode).signup_successfully.value
    }
    return MainService.response(data=response, status_code=200)


@UserApi.route('/current-user', methods=['GET'])
@Auth.auth_required
def loggedInUser(current_user, langCode):
    userSchema = UserSchema()
    userData = userSchema.dump(current_user)
    response = {
        "status": StatusType.success.value,
        "data": {"user": userData},
        "message": MainService.message(langCode).data_sent.value
    }
    return MainService.response(data=response, status_code=200)


@UserApi.route('/profile-update', methods=['POST'])
@Auth.auth_required
def profileUpdate(current_user, langCode):
    data = {
        "first_name": request.form.get('first_name'),
        "last_name": request.form.get('last_name'),
        "username": request.form.get('username'),
        "mobile": request.form.get('mobile'),
        "email": request.form.get('email'),
    }
    file = request.files['image']
    fields = ['first_name', 'last_name', 'username', 'mobile', 'email']
    errors = MainService.validation(fields, data)
    if errors:
        response = {
            "status": StatusType.error.value,
            "data": errors,
            "message": ""
        }
        return MainService.response(data=response, status_code=200)
    # Check username
    if current_user.username != data.get('username', None):
        user = User.getUserByUsername(data.get('username', ''))
        if user:
            response = {
                "status": StatusType.fail.value,
                "data": None,
                "message": MainService.message(langCode).username_exist.value
            }
            return MainService.response(data=response, status_code=200)
    # Check mobile
    if current_user.mobile != data.get('mobile', None):
        user = User.getUserByMobile(data.get('mobile', ''))
        if user:
            response = {
                "status": StatusType.fail.value,
                "data": None,
                "message": MainService.message(langCode).mobile_exist.value
            }
            return MainService.response(data=response, status_code=200)
    # Check email
    if current_user.email != data.get('email', None):
        user = User.getUserByEmail(data.get('email', ''))
        if user:
            response = {
                "status": StatusType.fail.value,
                "data": None,
                "message": MainService.message(langCode).email_exist.value
            }
            return MainService.response(data=response, status_code=200)

    user = User.getUserById(current_user.id_user)
    if user:
        data['id_user_image'] = user.id_user_image
        if file:
            userImage = UserImage({"file_name": file.filename, "file": file.read()})
            userImage.save()
            data['id_user_image'] = userImage.id_user_image
            if user.id_user_image:
                userImage = UserImage.getUserImageById(user.id_user_image)
                if userImage:
                    userImage.delete()
        user.update(data)
        user = User.getUserById(current_user.id_user)
        userSchema = UserSchema()
        userData = userSchema.dump(user)
        response = {
            "status": StatusType.success.value,
            "data": {"user": userData},
            "message": MainService.message(langCode).profile_updated_successfully.value
        }
        return MainService.response(data=response, status_code=200)
    else:
        response = {
            "status": StatusType.success.value,
            "data": None,
            "message": MainService.message(langCode).user_not_found.value
        }
        return MainService.response(data=response, status_code=200)