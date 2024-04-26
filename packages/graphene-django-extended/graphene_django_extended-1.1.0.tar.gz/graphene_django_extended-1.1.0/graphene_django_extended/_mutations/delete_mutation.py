import graphene
from django.db import models
from graphene.types.objecttype import yank_fields_from_attrs
from graphql_relay import from_global_id


class DeleteMutationOptions(graphene.types.mutation.MutationOptions):
    model_class = None


class DeleteMutation(
    graphene.relay.ClientIDMutation
    # graphene.Mutation
):
    class Meta:
        abstract = True

    @classmethod
    def Field(cls, *args, **kwargs) -> graphene.Field:
        # print(";;;;;;", cls, cls._meta)
        # cls._meta.arguments['input']._meta.fields.update({'id': UUIDInput()})
        return super().Field(*args, **kwargs)

    @classmethod
    def __init_subclass_with_meta__(cls, _meta=None, model_class=None, **options):
        assert issubclass(
            model_class, models.Model
        ), "You need to pass a Django model in Meta class"
        input_fields = {"id": graphene.InputField(graphene.String, required=True)}
        if not _meta:
            _meta = DeleteMutationOptions(cls)  # SerializerMutationOptions(cls)
        _meta.model_class = model_class
        output_fields = {
            "success": graphene.Boolean(
                description="True if the deletion was successful", required=True
            )
        }
        _meta.fields = yank_fields_from_attrs(output_fields, _as=graphene.types.Field)
        super().__init_subclass_with_meta__(
            _meta=_meta, input_fields=input_fields, **options
        )

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        # Relay uses global IDs, so we need to convert the ID back to a database ID
        # _, db_id = from_global_id(input.get('id'))

        # Perform the deletion
        success = False
        try:
            instance = cls._meta.model_class.objects.get(pk=input.get("id"))
            instance.delete()
            success = True
        except cls._meta.model_class.DoesNotExist:
            success = False

        # Return the original ID for client reference and the success status
        return cls(success=success)
