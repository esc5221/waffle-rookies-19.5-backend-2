from django.db import models

# class BaseManager(models.Manager):

#     def get_or_none(self, *args, **kwargs):
#         try:
#             return self.get(*args, **kwargs)
#         except self.model.DoesNotExist:
#             return None

class ErrorLog(models.Model):
    #objects = BaseManager()
    timestamp = models.DateTimeField(auto_now_add=True)
    request_url = models.CharField(max_length=200)
    request_body = models.CharField(max_length=500)
    response_code = models.PositiveSmallIntegerField()
    error_detail = models.CharField(max_length=500)