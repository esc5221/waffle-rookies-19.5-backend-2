from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods
from rest_framework import status, viewsets, permissions
from rest_framework.response import Response


class error500API(viewsets.GenericViewSet):
    permission_classes = (permissions.AllowAny(), )

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return (permissions.AllowAny(), )
        return self.permission_classes

    def list(self, request):

        # Incurring a 500 error by null referencing
        a = None
        if(a.attr == "foobar") : data = "attr is foobar"

        return Response(status=status.HTTP_423_LOCKED)

