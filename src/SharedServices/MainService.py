import datetime
import enum
import json
import re
from flask import Response
from marshmallow import fields, ValidationError
from src.SharedServices.messages.EnglishMessage import EnglishMessage
from src.SharedServices.messages.ItalianMessage import ItalianMessage


class StatusType(enum.Enum):
    success = "SUCCESS"
    fail = "FAIL"
    error = "ERROR"


class Date(enum.Enum):
    format = "%d/%m/%Y"


class FileByte(fields.Field):
    """Field that serializes to a string of numbers and deserializes
    to a list of numbers.
    """

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return ""
        return "".join(str(d) for d in value)

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return [int(c) for c in value]
        except ValueError as error:
            raise ValidationError("File bytes must contain only digits.") from error


class DateTimeField(fields.Field):
    """Field that serializes to a string of numbers and deserializes
    to a list of numbers.
    """

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return ""
        value = float(value)
        date = datetime.datetime.fromtimestamp(int(value))
        date = date.strftime(Date.format.value)
        return date

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return [int(c) for c in value]
        except ValueError as error:
            raise ValidationError("Datetime field must contain only digits.") from error


class MainService:
    def __init__(self):
        pass

    @staticmethod
    def getDateTimeNow():
        return datetime.datetime.now()

    @staticmethod
    def getCurrentTimeStamp():
        return datetime.datetime.timestamp(datetime.datetime.now())

    # Create response data
    @classmethod
    def responseModel(cls, values):
        if values.get('status') == StatusType.error.value:
            msg = cls.__setErrorMessages(values.get('data', ''))
            response = {
                "status": values.get('status', ''),
                "data": dict(),
                "message": msg,
                "errors": values.get('data', '')
            }
        else:
            try:
                data = json.loads(values.get('data', ''))
            except Exception as e:
                if type(values.get('data', '')) == dict:
                    data = values.get('data', '')
                else:
                    data = dict()
            response = {
                "status": values.get('status', ''),
                "data": data,
                "message": values.get('message', '')
            }
        response = json.dumps(response)
        return response

    # Response method
    @classmethod
    def response(cls, data, status_code):
        """
        Custom Response Function
        """
        response = cls.responseModel(data)
        return Response(
            mimetype="application/json",
            response=response,
            status=status_code
        )

    # Error message create
    @staticmethod
    def __setErrorMessages(data):
        message = ""
        for k, v in data.items():
            if message:
                message = str(message) + str(', ') + str(v)
            else:
                message = str(v)
        return message

    @staticmethod
    def validation(fields: list, data: dict) -> dict:
        errors = {}
        for field in fields:
            name = field.replace('_', ' ')
            if data.get(field) is None or data.get(field) == "":
                errors[field] = f"The {name} field is required."
            else:
                if field == "email":
                    EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
                    if data.get(field) and not re.match(EMAIL_REGEX, data.get(field)):
                        errors[field] = f"The {name} field is not valid."
                if field == "product":
                    product = data.get(field)
                    for k, v in product.items():
                        if v is None or v == "":
                            n = k.replace('_', ' ')
                            errors[k] = f"The {n} field is required."
        return errors

    @staticmethod
    def message(lang):
        # Check language code and return message class as refresh according to language
        if lang == "en":
            return EnglishMessage
        elif lang == "it":
            return ItalianMessage
        else:
            return EnglishMessage
