import warnings

import graphene
from graphene.relay import Connection, Node  # , Node
from graphene.relay.node import NodeField  # , Node
from graphene.types.interface import Interface, InterfaceOptions
from graphene.types.utils import yank_fields_from_attrs
from graphene_django.registry import Registry, get_global_registry
from graphene_django.types import ALL_FIELDS, construct_fields, validate_fields
from graphene_django.utils import (  # camelize,; get_model_fields,
    DJANGO_FILTER_INSTALLED,
    is_valid_django_model,
)


class DjangoInterfaceOptions(InterfaceOptions):
    model = None  # type: Type[Model]
    registry = None  # type: Registry
    connection = None  # type: Type[Connection]

    filter_fields = ()
    filterset_class = None


class DjangoInterface(Interface):
    @classmethod
    def __init_subclass_with_meta__(
        cls,
        model=None,
        registry=None,
        # skip_registry=False,
        # only_fields=None,  # deprecated in favour of `fields`
        fields=None,
        # exclude_fields=None,  # deprecated in favour of `exclude`
        exclude=None,
        filter_fields=None,
        filterset_class=None,
        connection=None,
        connection_class=None,
        use_connection=None,
        interfaces=(),
        convert_choices_to_enum=None,
        _meta=None,
        **options,
    ):

        assert is_valid_django_model(model), (
            'You need to pass a valid Django Model in {}.Meta, received "{}".'
        ).format(cls.__name__, model)

        if not registry:
            registry = get_global_registry()

        assert isinstance(registry, Registry), (
            f"The attribute registry in {cls.__name__} needs to be an instance of "
            f'Registry, received "{registry}".'
        )

        if filter_fields and filterset_class:
            raise Exception("Can't set both filter_fields and filterset_class")

        if not DJANGO_FILTER_INSTALLED and (filter_fields or filterset_class):
            raise Exception(
                "Can only set filter_fields or filterset_class if "
                "Django-Filter is installed"
            )

        assert not (fields and exclude), (
            "Cannot set both 'fields' and 'exclude' options on "
            f"DjangoInterface {cls.__name__}."
        )

        if fields and fields != ALL_FIELDS and not isinstance(fields, (list, tuple)):
            raise TypeError(
                'The `fields` option must be a list or tuple or "__all__". '
                "Got %s." % type(fields).__name__
            )

        if exclude and not isinstance(exclude, (list, tuple)):
            raise TypeError(
                "The `exclude` option must be a list or tuple. Got %s."
                % type(exclude).__name__
            )

        if fields is None and exclude is None:
            warnings.warn(
                "Creating a DjangoInterface without either the `fields` "
                "or the `exclude` option is deprecated. Add an explicit `fields "
                f"= '__all__'` option on DjangoInterface {cls.__name__} to use all "
                "fields",
                DeprecationWarning,
                stacklevel=2,
            )

        django_fields = yank_fields_from_attrs(
            construct_fields(model, registry, fields, exclude, convert_choices_to_enum),
            _as=graphene.Field,
        )

        ## Hack to make the interface inheritance work
        # other_fields = yank_fields_from_attrs(
        #    {"id": graphene.ID(required=True)}, _as=graphene.Field
        # )

        if use_connection is None and interfaces:
            use_connection = any(
                issubclass(interface, Node) for interface in interfaces
            )
        use_connection = True

        if use_connection and not connection:
            # We create the connection automatically
            if not connection_class:
                connection_class = Connection

            connection = connection_class.create_type(
                "{}Connection".format(options.get("name") or cls.__name__), node=cls
            )

        if connection is not None:
            assert issubclass(
                connection, Connection
            ), f"The connection must be a Connection. Received {connection.__name__}"

        if not _meta:
            _meta = DjangoInterfaceOptions(cls)
            _meta.fields = django_fields

        if _meta and _meta.fields:
            _meta.fields = {
                **django_fields,
                **_meta.fields,
                # **other_fields,
            }
        # del _meta.fields["id"]

        _meta.model = model
        _meta.registry = registry
        _meta.filter_fields = filter_fields
        _meta.filterset_class = filterset_class
        _meta.connection = connection
        _meta.convert_choices_to_enum = convert_choices_to_enum

        super().__init_subclass_with_meta__(
            _meta=_meta,
            interfaces=interfaces,
            **options,
        )

        # Validate fields
        validate_fields(cls, model, _meta.fields, fields, exclude)

        # if not skip_registry:
        #    registry.register(cls)

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset
