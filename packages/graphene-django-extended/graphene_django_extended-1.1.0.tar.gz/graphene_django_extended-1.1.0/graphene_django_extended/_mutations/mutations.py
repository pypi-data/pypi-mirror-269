from enum import Enum

import graphene
from django.contrib.auth.models import Permission
from graphene import String
from graphene_django.rest_framework.mutation import SerializerMutation
from graphql.error import GraphQLError
from graphql_jwt.exceptions import PermissionDenied

from ..authorization import BasePermissionMixin
from ..errors import ObscureGraphQLError  # Import ObscureGraphQLError


class PermissionedSerializerMutation(SerializerMutation):
    """
    A SerializerMutation subclass that incorporates permission checks.
    """

    class Meta(SerializerMutation.Meta):
        abstract = True

    @classmethod
    def has_permission(cls, user, permissions):
        """
        Checks if the user has the given permissions.

        Args:
            user (User): The user object.
            permissions (list of str): List of permission codenames.

        Returns:
            bool: True if the user has all the given permissions, False otherwise.
        """
        user_permissions = user.get_user_permissions()
        return all(permission in user_permissions for permission in permissions)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        """
        Override mutate_and_get_payload to perform permission checks.
        """
        # Extract permissions from Meta class
        permissions = getattr(cls.Meta, "permissions", [])

        # Check if the user has the required permissions
        if not cls.has_permission(info.context.user, permissions):
            raise PermissionDenied("You do not have permission to perform this action.")

        # Proceed with the original mutation if permissions are satisfied
        return super().mutate_and_get_payload(root, info, **input)


class MutationPermissionMixin(BasePermissionMixin):
    """
    Mixin class for handling mutation permissions.

    This mixin extends the functionality of BasePermissionMixin to provide permission checks for mutations.

    Attributes:
        Inherits all attributes from BasePermissionMixin.
    """

    @classmethod
    def mutate_and_get_payload(
        cls, root: "Mutation", info: graphene.ResolveInfo, **input
    ) -> "Mutation":
        user = info.context.user
        if cls.is_user_authorized(user):
            return super().mutate_and_get_payload(root, info, **input)
        raise ObscureGraphQLError("Unauthorized")  # Use ObscureGraphQLError


class ValidateWithErrorExtensionMixin:
    """
    Mixin class for validating input data with error extensions.

    This mixin performs input validation using a serializer and raises a GraphQL error with validation errors if validation fails.

    Methods:
        mutate_and_get_payload(cls, root, info, **input) -> 'Mutation':
            Perform mutation and return the payload.
    """

    @classmethod
    def mutate_and_get_payload(
        cls, root: "Mutation", info: graphene.ResolveInfo, **input
    ) -> "Mutation":
        kwargs = cls.get_serializer_kwargs(root, info, **input)
        serializer = cls._meta.serializer_class(**kwargs)
        if serializer is None or serializer.is_valid():
            return cls.perform_mutate(serializer, info)
        else:
            raise ObscureGraphQLError(
                extensions=serializer.errors, message="Validation Error"
            )  # Use ObscureGraphQLError


class MutationDeleteMixin(BasePermissionMixin):
    """
    Mixin class for handling deletion mutations.

    This mixin retrieves an object by ID, deletes it, and returns the deleted instance.

    Args:
        SubclassWithMeta: A subclass with metadata.
    """

    id = graphene.Field(graphene.UUID, required=True)

    @classmethod
    def Field(cls, *args, **kwargs) -> graphene.Field:
        cls._meta.arguments["input"]._meta.fields.update(
            {"id": graphene.InputField(graphene.UUID, required=True)}
        )
        return super().Field(*args, **kwargs)

    @classmethod
    def mutate_and_get_payload(
        cls, root: "Mutation", info: graphene.ResolveInfo, **input
    ) -> "Mutation":
        id = input["id"]
        try:
            instance = cls._kwargs["model"].objects.get(id=id)
        except cls._kwargs["model"].DoesNotExist:
            raise ObscureGraphQLError(
                "Object not found"
            )  # Use ObscureGraphQLError for specific error
        deleted = instance.delete()
        if deleted[0] == 1:
            return cls(**input)
        raise ObscureGraphQLError(
            "Deletion failed"
        )  # Use ObscureGraphQLError for specific error

    @classmethod
    def __init_subclass_with_meta__(
        cls,
        name: str = None,
        description: str = None,
        _meta: Any = None,
        **_kwargs: Any,
    ) -> None:
        super().__init_subclass_with_meta__(name, description, _meta, **_kwargs)
        cls._kwargs = _kwargs


class ResolveEnumToValueMixin:
    """
    Mixin class for resolving enum inputs to their actual values.

    This mixin resolves enum inputs to their values before performing a mutation.
    This is only needed because of a bug in django-graphene

    Example:
        class MyMutation(ResolveEnumToValueMixin, Mutation):
            ...
    """

    @classmethod
    def mutate_and_get_payload(
        cls, root: "Mutation", info: graphene.ResolveInfo, **inputs
    ) -> "Mutation":
        enum_type_inputs = {
            key: enum_input.value
            for (key, enum_input) in inputs.items()
            if isinstance(enum_input, Enum)
        }
        transformed_inputs = {**inputs, **enum_type_inputs}
        return super().mutate_and_get_payload(root, info, **transformed_inputs)
