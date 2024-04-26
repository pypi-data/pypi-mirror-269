import graphene
from django.db import models
from graphene_django import DjangoConnectionField, DjangoListField, DjangoObjectType
from graphene_django.converter import (  # convert_django_field,
    get_django_field_description,
)
from graphene_django.filter.fields import DjangoFilterConnectionField


def convert_field_to_list_or_connection(field, registry=None):
    model = field.related_model
    # print("NEW convert_field", field, model)

    def dynamic_type():
        _type = registry.get_type_for_model(model)
        if not _type:
            return

        if isinstance(field, models.ManyToManyField):
            description = get_django_field_description(field)
        else:
            description = get_django_field_description(field.field)

        # If there is a connection, we should transform the field
        # into a DjangoConnectionField
        if _type._meta.connection:
            from .connection import (
                DjangoInterfaceConnectionField,
                DjangoInterfaceFilterConnectionField,
            )

            # Use a DjangoFilterConnectionField if there are
            # defined filter_fields or a filterset_class in the
            # DjangoObjectType Meta
            if _type._meta.filter_fields or _type._meta.filterset_class:
                return DjangoInterfaceFilterConnectionField(
                    _type, required=True, description=description
                )

            return DjangoInterfaceConnectionField(
                _type, required=True, description=description
            )

        return DjangoListField(
            _type,
            required=True,  # A Set is always returned, never None.
            description=description,
        )

    return graphene.Dynamic(dynamic_type)
