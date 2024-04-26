from typing import Any, Dict, Type

import graphene
from activitystreams.models import Image
from django.db import models
from graphene_django.rest_framework.mutation import SerializerMutation
from graphene_django_polymorphic import RelaySerializerMutation
from rest_framework import serializers

from .delete_mutation import DeleteMutation
from .global_id_serializer_mutation import GlobalIDSerializerMutation

# SerializerMutation = GlobalIDSerializerMutation
SerializerMutation = RelaySerializerMutation


class ModelMutationOptions(graphene.types.mutation.MutationOptions):
    model_class = None
    create_fields = "__all__"
    update_fields = "__all__"
    delete_fields = None
    registry = None
    additional_options = {}


def generate_serializer_class(
    model_class: Type[models.Model], operation: str, **kwargs: Any
) -> Type[serializers.ModelSerializer]:
    """
    Dynamically generates serializer classes based on the given model class and operation.

    Args:
        model_class: The Django model class to generate a serializer for.
        operation: The operation the serializer is for ('create' or 'update').
        **kwargs: Additional keyword arguments for customizing the serializer.

    Returns:
        A dynamically created serializer class.
    """
    class_name = f"{operation.capitalize()}{model_class.__name__}Serializer"
    Meta = type("Meta", (), {"model": model_class, "fields": "__all__"})
    return type(class_name, (serializers.ModelSerializer,), {"Meta": Meta})


def generate_mutation_class(
    model_class: Type[models.Model],
    operation: str,
    registry=None,
    **additional_options: Any,
) -> Type[graphene.Mutation]:
    """
    Dynamically generates mutation classes based on the model_class, operation, and additional meta options.

    Args:
        model_class: The Django model to generate a mutation for.
        operation: The operation type ('create', 'update', 'delete').
        **additional_options: Additional keyword arguments for mutation configuration.

    Returns:
        A dynamically created Graphene Mutation class.
    """
    serializer_class = None
    if operation in ["create", "update"]:
        serializer_class = generate_serializer_class(model_class, operation)

    meta_attrs = {
        "model_class": model_class,
        "fields": "__all__",
        "convert_choices_to_enum": [],
        **additional_options,
    }
    if operation == "update":
        meta_attrs["lookup_field"] = "id"
    if operation in ["create", "update"]:
        meta_attrs["serializer_class"] = serializer_class
        meta_attrs["registry"] = registry
    Meta = type("Meta", (), meta_attrs)

    base_class = SerializerMutation if serializer_class else DeleteMutation

    mutation_attrs = {"Meta": Meta}
    if serializer_class:
        mutation_attrs["serializer_class"] = serializer_class

    mutation_class_name = f"{operation.capitalize()}{model_class.__name__}Mutation"
    return type(mutation_class_name, (base_class,), mutation_attrs)


class ModelMutation(graphene.ObjectType):
    """
    Dynamically generate mutation fields for CRUD operations on a given model_class.
    """

    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(
        cls,
        _meta=None,
        model_class=None,
        registry=None,
        additional_options={},
        **options,
    ):
        if model_class is None:
            # This is called when the class is subclassed, for instance
            # class Mutation(ImageModelMutation)
            # In this case we only want to create the fields in the parent
            # class and not in the subclass
            super().__init_subclass_with_meta__(_meta=_meta, **options)
            return
        if not hasattr(cls, "_meta") or not hasattr(cls._meta, "model_class"):
            assert model_class is not None and issubclass(
                model_class, models.Model
            ), "model_class is required for ModelMutation and must be a Django model."
        else:
            model_class = cls._meta.model_class

        model_name = model_class._meta.model_name.lower()

        # Create the serializer and mutation classes dynamically
        create_mutation = generate_mutation_class(
            model_class,
            "create",
            registry=registry,
        )
        update_mutation = generate_mutation_class(
            model_class,
            "update",
            registry=registry,
        )
        delete_mutation = generate_mutation_class(
            model_class,
            "delete",
        )

        setattr(cls, f"create_{model_name}", create_mutation.Field())
        setattr(cls, f"update_{model_name}", update_mutation.Field())
        setattr(cls, f"delete_{model_name}", delete_mutation.Field())

        if not _meta:
            _meta = ModelMutationOptions(cls)  # SerializerMutationOptions(cls)
        _meta.model_class = model_class

        # output_fields = {
        #    "success": graphene.Boolean(
        #        description="True if the deletion was successful", required=True
        #    )
        # }

        _meta = ModelMutationOptions(cls)
        _meta.model_class = model_class
        # _meta.fields = yank_fields_from_attrs(output_fields, _as=Field)

        super().__init_subclass_with_meta__(_meta=_meta, **options)
