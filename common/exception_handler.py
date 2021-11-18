from rest_framework import exceptions, status
from rest_framework.views import Response
from rest_framework.exceptions import ValidationError, APIException

from rest_framework.exceptions import ErrorDetail
from rest_framework.views import exception_handler as ec

from rest_framework import serializers
from common.models import ErrorLog
import pprint

Exception
def exception_handler(exc, context):
    if(not hasattr(exc,"status_code")) : 
        data = {'detail': '내부 서버 에러입니다. admin@wafl.shop에 연락 부탁드립니다.'}
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        
        request = context['request']._request
        request_data = context['request'].data
        
        # print("1 : ", (request.method+" "+request.path))
        # print("2 : ", request_data)
        # print("3 : ", 500)
        # print("4 : ", str(exc))
        error_log = ErrorLog.objects.create(
            request_url=(request.method+" "+request.path),
            request_body=request_data,
            response_code=500,
            error_detail=str(exc),
        )

        return Response(data, status=status_code)
    else :
        response = ec(exc, context)
        request = context['request']._request
        request_data = context['request'].data
    
        # print("1 : ", (request.method+" "+request.path))
        # print("2 : ", request_data)
        # print("3 : ", exc.status_code)
        # print("4 : ", exc.detail)
        error_log = ErrorLog.objects.create(
            request_url=(request.method+" "+request.path),
            request_body=request_data,
            response_code=exc.status_code,
            error_detail=exc.detail,
        )

    return response
