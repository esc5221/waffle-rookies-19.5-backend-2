from django.db import models

class ErrorLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True) # 에러 기록 시점
    request_url = models.CharField(max_length=200)      # request url (Method+path, ex: GET /api/v1/seminar/)
    request_body = models.CharField(max_length=500)     # request body (raw JSON, ex: {"email" : "foobar"})
    response_code = models.PositiveSmallIntegerField()  # response_code (int, ex: 404)
    error_detail = models.CharField(max_length=500)     # 에러 디테일 (str, ex: "Authentication credentials were not provided.")

