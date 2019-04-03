class ActionSerializerMixin:
    """
    Mixin to use different serializers for any action. If no serializer is found if falls back to the default
    serializer_class defined on the API View.

    e.g.
    serializer_class = DetailSerializer
    action_serializers = {
        'list': ListSerializer,
    }
    """
    action_serializers = {}

    def get_serializer_class(self):
        return self.action_serializers.get(self.action, super().get_serializer_class())
