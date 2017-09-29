from rest_framework import status
from rest_framework.compat import set_rollback
from rest_framework.response import Response
from rest_framework.views import exception_handler

from magic.core.exception import MagicException


def magic_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if isinstance(exc, MagicException):
        set_rollback()
        return Response({'detail': str(exc)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        headers={})

    return response