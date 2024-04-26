import graphene
from django.db.models import Q

# from graphene_django.fields import DjangoConnectionField
from graphene_django.filter import DjangoFilterConnectionField

from ..connection import DjangoInterfaceConnectionField


class SearchDjangoConnectionFieldMixin:
    def __init__(self, type_, *args, **kwargs):
        """
        Initialize the connection field and dynamically add a 'search' argument
        if 'search_fields' are specified in the Meta class of the DjangoObjectType.
        """
        # Check if the type has defined search_fields in its Meta
        if True:  # hasattr(type_, '_meta') and hasattr(type_._meta, 'search_fields'):
            if "args" not in kwargs:
                kwargs["args"] = {}
            kwargs["args"]["search"] = graphene.String(description="Search by fields")

        super().__init__(type_, *args, **kwargs)

    @classmethod
    def merge_querystrings(cls, queryset, value, search_fields):
        """
        Apply search filters to the queryset based on the search value and specified fields.
        """
        if value:
            queries = [Q(**{f"{field}__icontains": value}) for field in search_fields]
            query = queries.pop()
            for item in queries:
                query |= item
            return queryset.filter(query)
        return queryset

    @classmethod
    def resolve_queryset(cls, connection, iterable, info, args, **kwargs):
        queryset = super().resolve_queryset(connection, iterable, info, args, **kwargs)
        print("CN", info, info.context, args, cls)

        node_type = connection._meta.node
        # Apply search filter if 'search' argument is provided and 'search_fields' are defined
        if (
            "search" in args
            and hasattr(node_type, "_meta")
            and hasattr(node_type._meta, "search_fields")
        ):
            search_value = args["search"]
            search_fields = node_type._meta.search_fields
            queryset = cls.merge_querystrings(queryset, search_value, search_fields)

        return queryset


class SearchDjangoConnectionField(
    SearchDjangoConnectionFieldMixin, DjangoFilterConnectionField
):
    """
    Extension of DjangoFilterConnectionField to include search functionality
    based on a predefined list of searchable fields.
    """


class SearchDjangoInterfaceConnectionField(
    SearchDjangoConnectionFieldMixin, DjangoInterfaceConnectionField
):
    """
    Extension of DjangoInterfaceConnectionField to include search functionality
    based on a predefined list of searchable fields.
    """
