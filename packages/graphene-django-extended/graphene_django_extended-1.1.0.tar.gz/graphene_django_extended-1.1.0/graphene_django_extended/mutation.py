from collections import OrderedDict
from enum import Enum

import graphene
from django.shortcuts import get_object_or_404
from graphene.relay.mutation import ClientIDMutation
from graphene.types import Field, InputField
from graphene.types.mutation import MutationOptions
from graphene.types.objecttype import yank_fields_from_attrs
from graphene_django.rest_framework.mutation import (
    SerializerMutationOptions,
    fields_for_serializer,
)
from graphene_django.rest_framework.serializer_converter import convert_serializer_field
from graphene_django.types import ErrorType
from graphql_relay import to_global_id
from rest_framework import serializers


class RelaySerializerMutationOptions(SerializerMutationOptions):
    registry = None


class RelaySerializerMutation(ClientIDMutation):
    class Meta:
        abstract = True

    errors = graphene.List(
        ErrorType, description="May contain more than one error for same field."
    )

    @classmethod
    def __init_subclass_with_meta__(
        cls,
        lookup_field=None,
        serializer_class=None,
        model_class=None,
        model_operations=("create", "update"),
        only_fields=(),
        exclude_fields=(),
        registry=None,
        convert_choices_to_enum=True,
        _meta=None,
        optional_fields=(),
        **options,
    ):
        if not serializer_class:
            raise Exception("serializer_class is required for the SerializerMutation")

        if "update" not in model_operations and "create" not in model_operations:
            raise Exception('model_operations must contain "create" and/or "update"')
        serializer = serializer_class()
        if model_class is None:
            serializer_meta = getattr(serializer_class, "Meta", None)
            if serializer_meta:
                model_class = getattr(serializer_meta, "model", None)

        if lookup_field is None and model_class:
            lookup_field = model_class._meta.pk.name

        input_fields = fields_for_serializer(
            serializer,
            only_fields,
            exclude_fields,
            is_input=True,
            convert_choices_to_enum=convert_choices_to_enum,
            lookup_field=lookup_field,
            optional_fields=optional_fields,
        )
        output_fields = fields_for_serializer(
            serializer,
            only_fields,
            exclude_fields,
            is_input=False,
            convert_choices_to_enum=convert_choices_to_enum,
            lookup_field=lookup_field,
        )

        if not _meta:
            _meta = RelaySerializerMutationOptions(cls)
        _meta.lookup_field = lookup_field
        _meta.model_operations = model_operations
        _meta.serializer_class = serializer_class
        _meta.model_class = model_class
        ## Addition in the if only
        if registry:
            _meta.registry = registry
            node_type = registry.get_type_for_model(model_class)
            _meta.node_type = node_type
            corrected_output_fields = OrderedDict()
            corrected_output_fields["instance"] = graphene.Field(
                node_type, description="The created/updated instance."
            )
            _meta.fields = yank_fields_from_attrs(corrected_output_fields, _as=Field)
            # ipdb.set_trace()
            # if _meta.model_class.__name__ is "Image":
            #    print("META FIELDS", _meta.fields)
            #    # ipdb.set_trace()
        else:
            _meta.fields = yank_fields_from_attrs(output_fields, _as=Field)

        input_fields = yank_fields_from_attrs(input_fields, _as=InputField)
        super().__init_subclass_with_meta__(
            _meta=_meta, input_fields=input_fields, **options
        )

    @classmethod
    def get_serializer_kwargs(cls, root, info, **input):
        lookup_field = cls._meta.lookup_field
        model_class = cls._meta.model_class
        if model_class:
            for input_dict_key, maybe_enum in input.items():
                if isinstance(maybe_enum, Enum):
                    input[input_dict_key] = maybe_enum.value
            if "update" in cls._meta.model_operations and lookup_field in input:
                instance = get_object_or_404(
                    model_class, **{lookup_field: input[lookup_field]}
                )
                partial = True
            elif "create" in cls._meta.model_operations:
                instance = None
                partial = False
            else:
                raise Exception(
                    'Invalid update operation. Input parameter "{}" required.'.format(
                        lookup_field
                    )
                )

            return {
                "instance": instance,
                "data": input,
                "context": {"request": info.context},
                "partial": partial,
            }

        return {"data": input, "context": {"request": info.context}}

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        kwargs = cls.get_serializer_kwargs(root, info, **input)
        serializer = cls._meta.serializer_class(**kwargs)

        if serializer.is_valid():
            return cls.perform_mutate(serializer, info)
        else:
            errors = ErrorType.from_errors(serializer.errors)
            # ipdb.set_trace()

            return cls(errors=errors)

    @classmethod
    def perform_mutate(cls, serializer, info):
        obj = serializer.save()

        kwargs = {}
        for f, field in serializer.fields.items():
            if not field.write_only:
                if isinstance(field, serializers.SerializerMethodField):
                    kwargs[f] = field.to_representation(obj)
                else:
                    kwargs[f] = field.get_attribute(obj)
        if cls._meta.registry:
            # print("PFMS", kwargs)
            node_type = cls._meta.node_type
            kwargs["id"] = to_global_id(node_type.__name__, obj.pk)
            # kwargs["pk"] = to_global_id(node_type.__name__, obj.pk)
            # instance = node_type(**kwargs)
            instance = obj
            return cls(errors=None, instance=instance)

        return cls(errors=None, **kwargs)
