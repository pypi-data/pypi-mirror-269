"""
This is a simple fix to the issue of not being able to use DjangoFilterConnectionField with interfaces.

There is no original code here except from the extension of the assert statement in DjangoInterfaceConnectionField.

https://github.com/graphql-python/graphene-django/blob/main/graphene_django/filter/fields.py
"""

from collections import OrderedDict
from functools import partial

import graphene
from graphene.types.argument import to_arguments
from graphene.utils.str_converters import to_snake_case
from graphene_django.fields import DjangoConnectionField
from graphene_django.filter.fields import DjangoFilterConnectionField
from graphene_django.filter.utils import (
    get_filtering_args_from_filterset,
    get_filterset_class,
)
from graphene_django.types import DjangoObjectType


## THis is a hardcoded rewrite of the class to allow for proper interface support
class DjangoInterfaceConnectionField(DjangoConnectionField):
    @property
    def type(self):
        from .interface import DjangoInterface

        _type = super(graphene.relay.ConnectionField, self).type
        non_null = False
        if isinstance(_type, graphene.NonNull):
            _type = _type.of_type
            non_null = True

        assert issubclass(_type, (DjangoObjectType, DjangoInterface)), (
            "DjangoInterfaceConnectionField only accepts DjangoObjectType or "
            "DjangoInterface types"
        )
        assert _type._meta.connection, "The type {} doesn't have a connection".format(
            _type.__name__
        )
        connection_type = _type._meta.connection
        if non_null:
            return graphene.NonNull(connection_type)
        return connection_type


# class CombinedMeta(type):
#     """
#     A metaclass that combines methods and attributes from multiple parent classes.
#     """
#
#     def __new__(meta, name, bases, class_dict):
#         # Adding methods from DjangoFilterConnectionField
#         for attr_name, attr_value in vars(DjangoFilterConnectionField).items():
#             #if not attr_name.startswith('__') and callable(attr_value):
#             #if not attr_name.startswith('__'):
#                 #print("USED", attr_name)
#             class_dict[attr_name] = attr_value
#             #class_dict.__init__ = DjangoFilterConnectionField.__init__
#
#         # Creating the new class
#         return type.__new__(meta, name, bases, class_dict)


class DjangoInterfaceFilterConnectionField(
    DjangoInterfaceConnectionField,  # metaclass=CombinedMeta
):
    def __init__(
        self,
        type_,
        fields=None,
        order_by=None,
        extra_filter_meta=None,
        filterset_class=None,
        *args,
        **kwargs,
    ):
        self._fields = fields
        self._provided_filterset_class = filterset_class
        self._filterset_class = None
        self._filtering_args = None
        self._extra_filter_meta = extra_filter_meta
        self._base_args = None
        super().__init__(type_, *args, **kwargs)

    @property
    def args(self):
        return to_arguments(self._base_args or OrderedDict(), self.filtering_args)

    @args.setter
    def args(self, args):
        self._base_args = args

    @property
    def filterset_class(self):
        if not self._filterset_class:
            fields = self._fields or self.node_type._meta.filter_fields
            meta = {"model": self.model, "fields": fields}
            if self._extra_filter_meta:
                meta.update(self._extra_filter_meta)

            filterset_class = (
                self._provided_filterset_class or self.node_type._meta.filterset_class
            )
            self._filterset_class = get_filterset_class(filterset_class, **meta)

        return self._filterset_class

    @property
    def filtering_args(self):
        if not self._filtering_args:
            self._filtering_args = get_filtering_args_from_filterset(
                self.filterset_class, self.node_type
            )
        return self._filtering_args

    @classmethod
    def resolve_queryset(
        cls, connection, iterable, info, args, filtering_args, filterset_class
    ):
        def filter_kwargs():
            kwargs = {}
            for k, v in args.items():
                if k in filtering_args:
                    if k == "order_by" and v is not None:
                        v = to_snake_case(v)
                    kwargs[k] = convert_enum(v)
            return kwargs

        qs = super().resolve_queryset(connection, iterable, info, args)

        filterset = filterset_class(
            data=filter_kwargs(), queryset=qs, request=info.context
        )
        if filterset.is_valid():
            return filterset.qs
        raise ValidationError(filterset.form.errors.as_json())

    def get_queryset_resolver(self):
        return partial(
            self.resolve_queryset,
            filterset_class=self.filterset_class,
            filtering_args=self.filtering_args,
        )
