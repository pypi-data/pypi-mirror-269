import graphene
import ipdb
from django.db.models import Q
from django.db.models.query import QuerySet
from graphene import ObjectType, ResolveInfo
from graphene.relay.node import Node, NodeField
from graphene.types.objecttype import ObjectTypeOptions
from graphene_django.types import DjangoObjectType

from ..interface import DjangoInterface, DjangoInterfaceOptions
from .field import SearchNodeField


class SearchDjangoObjectTypeOptions(ObjectTypeOptions):
    search_fields = []


class SearchDjangoInterfaceOptions(
    SearchDjangoObjectTypeOptions, DjangoInterfaceOptions
):
    pass


class SearchMixin:
    @classmethod
    def get_queryset(cls, queryset, info):
        """
        Extension of the base get_queryset method to allow for
        searching by fields if the 'search' argument is provided.
        """
        if not hasattr(info.context, "search"):
            return super().get_queryset(queryset, info)

        search_query = info.context.get("search")

        if search_query and cls._meta.search_fields:
            q_objects = Q()
            for field in cls._meta.search_fields:
                q_objects |= Q(**{f"{field}__icontains": search_query})
            queryset = queryset.filter(q_objects)
        return queryset

    @classmethod
    def get_node(cls, info, id, **kwargs):
        """
        Extension of the base get_node method to allow for querying by kwargs if the id is not provided.
        It is to be remarked that we only extend the ObjectTypes, not the Interface.
        """
        if id:
            return super().get_node(info, id)
        queryset = cls.get_queryset(cls._meta.model.objects, info)
        if not bool(kwargs):
            return None
        try:
            return queryset.get(**kwargs)
        except cls._meta.model.DoesNotExist:
            # raise Exception( f"The node {cls._meta.model.__name__} with kwargs {kwargs} does not exist.")
            return None


class SearchDjangoObjectType(SearchMixin, DjangoObjectType):
    """
    It is crucial that this is used with SearchNode, as it is the only way to resolve the node by kwargs.
    object = SearchNode.Field(SearchNodeDjangoObjectType)
    """

    @classmethod
    def __init_subclass_with_meta__(
        cls,
        search_fields=None,
        _meta=None,
        **options,
    ):
        if not _meta:
            # ipdb.set_trace()
            _meta = SearchDjangoObjectTypeOptions(cls)
        _meta.search_fields = search_fields or []
        super(SearchDjangoObjectType, cls).__init_subclass_with_meta__(
            _meta=_meta, **options
        )

    @classmethod
    def get_node(cls, info, id, **kwargs):
        """
        Extension of the base get_node method to allow for querying by kwargs if the id is not provided.
        It is to be remarked that we only extend the ObjectTypes, not the Interface.
        """
        if id:
            return super().get_node(info, id)
        queryset = cls.get_queryset(cls._meta.model.objects, info)
        try:
            # Todo only do this if kwargs are not empty
            if bool(kwargs):
                return queryset.get(**kwargs)
            return None
        except cls._meta.model.DoesNotExist:
            # raise Exception( f"The node {cls._meta.model.__name__} with kwargs {kwargs} does not exist.")
            return None

    class Meta:
        abstract = True


class SearchDjangoInterface(SearchMixin, DjangoInterface):
    @classmethod
    def __init_subclass_with_meta__(
        cls,
        search_fields=None,
        _meta=None,
        **options,
    ):
        if not _meta:
            _meta = SearchDjangoInterfaceOptions(cls)

        _meta.search_fields = search_fields or []

        super().__init_subclass_with_meta__(_meta=_meta, **options)

    class Meta:
        abstract = True
