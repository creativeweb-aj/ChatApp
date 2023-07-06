import enum


class EnglishMessage(enum.Enum):
    data_sent = "Data sent successfully!"
    user_not_found = "User not exist!"
    invalid_credentials = "Invalid Credentials!"
    login_successfully = "Login Successfully!"
    signup_successfully = "Signup successfully login now!"
    profile_updated_successfully = "Profile updated successfully!"
    email_exist = "Email is already exist!"
    username_exist = "Username is already exist!"
    mobile_exist = "Mobile is already exist!"
    password_not_match = "Password not match!"
