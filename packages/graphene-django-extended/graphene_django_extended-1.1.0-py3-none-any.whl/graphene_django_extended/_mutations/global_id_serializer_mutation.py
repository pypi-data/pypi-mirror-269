from graphene_django.rest_framework.mutation import SerializerMutation
from graphql_relay import to_global_id


class GlobalIDSerializerMutation(SerializerMutation):
    class Meta:
        abstract = True

    @classmethod
    def get_global_id(cls, id):
        return to_global_id(f"{cls._meta.model_class.__name__}Node", id)

    @classmethod
    def perform_mutate(cls, serializer, info):
        """
        Override to include 'id' field conversion from database ID to global ID in the response.
        """
        # obj = serializer.save()
        response = super().perform_mutate(serializer, info)
        response.id = cls.get_global_id(response.id)
        response.__typename = f"{cls._meta.model_class.__name__}Node"
        return response
