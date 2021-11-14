from rest_framework import exceptions, status
from rest_framework.views import Response
from rest_framework.exceptions import ValidationError, APIException

from rest_framework.exceptions import ErrorDetail
from rest_framework.views import exception_handler as ec

Exception
def exception_handler(exc, context):
    if(not hasattr(exc,"status_code")) : 
        data = {'detail': '내부 서버 에러입니다. admin@wafl.shop에 연락 부탁드립니다.'}
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return Response(data, status=status_code)
    response = ec(exc, context)
    return response