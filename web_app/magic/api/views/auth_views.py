from datetime import datetime

from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework import permissions as drf_permissions, status
from rest_framework.decorators import list_route
from rest_framework.exceptions import ParseError
from rest_framework.response import Response

from magic.api import permissions
from magic.api.serializers.auth_serializers import UserSerializer
from magic.api.views.BaseViews import MagicModelViewSet


class UserViewSet(MagicModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)

    def list(self, request, *args, **kwargs):
        print ("T:{}".format(datetime.now()))
        return super().list(request, *args, **kwargs)

    @list_route(methods=['post'], permission_classes=(drf_permissions.AllowAny,))
    def register(self, request):
        try:
            user = User.objects.get(username=request.data.get('username'))
            return Response(self.serializer_class(user).data)
        except User.DoesNotExist:
            try:
                user = User.objects.create(
                    username=request.data.get("username"),
                    email=request.data.get("email"),
                )
                return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                raise ParseError(detail=e.message)

