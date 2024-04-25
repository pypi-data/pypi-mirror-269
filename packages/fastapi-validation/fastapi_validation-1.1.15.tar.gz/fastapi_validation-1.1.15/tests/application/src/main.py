
from fastapi import FastAPI
from fastapi_exception import FastApiException
from fastapi_exception.config import GlobalVariable
from pydantic import BaseModel

from fastapi_validation import PasswordValidation
from fastapi_validation.enums.database_type_enum import DatabaseTypeEnum

from ..config.i18n import i18n_service

app = FastAPI(title="Test App")
GlobalVariable.set('app', app)
GlobalVariable.set('database_type', DatabaseTypeEnum.SQL)

FastApiException.config(i18n_service)


class ChangePasswordDto(BaseModel):
    new_password: PasswordValidation


@app.post("/password")
def create_cars(dto: ChangePasswordDto):
    return True


def required_phone_number_and_code_pair(cls, values):
    phone_code, phone_number = values.phone_code, values.phone_number

    is_missing_only_phone_number = phone_code is not None and phone_number is None
    is_missing_only_phone_code = phone_number is not None and phone_code is None

    if is_missing_only_phone_number or is_missing_only_phone_code:
        raise ValueError()

    return values


#
# class CheckPhoneTokenDto(BaseModel):
#     phone_code: Optional[str] = None
#     phone_number: Optional[str] = None
#
#     _phone_number_and_code_validation = ModelValidator()(required_phone_number_and_code_pair)
#
#
# class PostEntity(declarative_base()):
#     __tablename__ = 'post'
#
#     id = Column(
#         UUID(as_uuid=True),
#         primary_key=True,
#         server_default=sqlalchemy.text("uuid_generate_v4()"),
#     )
#
#
# @app.post("/phone")
# def phone(dto: CheckPhoneTokenDto):
#     return True
#
#
# class ReportDto(BaseModel):
#     post_id: str
#
#     _exist_post_id = FieldValidator('post_id')(Exists(table='PostEntity', column='id'))
#
#
# @app.post("/report")
# def report(dto: ReportDto):
#     return True
