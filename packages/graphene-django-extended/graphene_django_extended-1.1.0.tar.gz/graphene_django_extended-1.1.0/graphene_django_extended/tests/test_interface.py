# pylint: disable=missing-class-docstring
# mypy: disable-error-code=no-untyped-def

import graphene_django.registry as registry
import pytest
from django.db import models
from graphene import Connection, List, ObjectType, Schema, String
from graphene_django.types import DjangoObjectType

from ..fields import DjangoInterface  # Assuming DjangoInterface is implemented here

# Helper Function


def with_local_registry(func):
    def inner(*args, **kwargs):
        old = registry.get_global_registry()
        try:
            retval = func(*args, **kwargs)
        except Exception as e:
            registry.registry = old
            raise e
        else:
            registry.registry = old
            return retval

    return inner


# Test Models
class EmployeeModel(models.Model):
    name = models.CharField(max_length=30)
    department = models.CharField(max_length=30)

    class Meta:
        app_label = "test"


class ManagerModel(EmployeeModel):
    managed_department = models.CharField(max_length=30)

    class Meta:
        app_label = "test"


# Tests for DjangoInterface
@with_local_registry
def test_django_interface_instantiation():
    class PersonInterface(DjangoInterface):
        class Meta:
            model = EmployeeModel
            fields = "__all__"

    assert issubclass(PersonInterface, DjangoInterface)


@with_local_registry
def test_django_interface_field_mapping():
    class EmployeeInterface(DjangoInterface):
        class Meta:
            model = EmployeeModel
            fields = "__all__"

    assert "name" in EmployeeInterface._meta.fields
    assert "department" in EmployeeInterface._meta.fields


@with_local_registry
def test_django_interface_meta_configuration():
    class EmployeeInterface(DjangoInterface):
        class Meta:
            model = EmployeeModel
            fields = "__all__"

    assert EmployeeInterface._meta.model == EmployeeModel


@with_local_registry
def test_django_interface_polymorphic_type_resolution():
    class EmployeeInterface(DjangoInterface):
        class Meta:
            model = EmployeeModel
            fields = "__all__"

        @classmethod
        def resolve_type(cls, instance, info):
            return ManagerModel if isinstance(instance, ManagerModel) else EmployeeModel

    assert EmployeeInterface.resolve_type(ManagerModel(), None) == ManagerModel


@with_local_registry
def test_django_interface_graphql_query_integration():
    class EmployeeInterface(DjangoInterface):
        class Meta:
            model = EmployeeModel
            fields = "__all__"

        @classmethod
        def resolve_type(cls, instance, info):
            print(instance, "222")
            return (
                EmployeeType  # ManagerModel if isinstance(instance, ManagerModel) else
            )

    class EmployeeType(DjangoObjectType):
        class Meta:
            model = EmployeeModel
            interfaces = (EmployeeInterface,)

    class Query(ObjectType):
        employees = List(EmployeeInterface)

        def resolve_employees(root, info):
            return [EmployeeModel(name="Alice", department="Sales")]

    schema = Schema(query=Query, types=[EmployeeType])
    query = """ query { employees { name department } } """
    result = schema.execute(query)
    print(result, "result")
    assert not result.errors
    assert result.data["employees"][0]["name"] == "Alice"
    assert result.data["employees"][0]["department"] == "Sales"


# We should test this in a fully fledged schema with multiple cases. See
# graphene_django.tests.test_type.py for an example implementation
# @with_local_registry
# def test_django_interface_enum_conversion_handling():
#    class DepartmentModel(models.Model):
#        name = models.CharField(choices=[('IT', 'Information Technology'), ('HR', 'Human Resources')])
#
#        class Meta:
#            app_label = 'test'
#
#    class DepartmentInterface(DjangoInterface):
#        class Meta:
#            model = DepartmentModel
#            convert_choices_to_enum = True
#            fields = '__all__'
#
#    assert 'name' in DepartmentInterface._meta.fields


@with_local_registry
def test_django_interface_custom_name_propagation():
    class CustomEmployeeInterface(DjangoInterface):
        class Meta:
            model = EmployeeModel
            name = "CustomEmployee"
            fields = "__all__"

    assert CustomEmployeeInterface._meta.name == "CustomEmployee"


@with_local_registry
def test_django_interface_excluding_fields():
    class EmployeeInterface(DjangoInterface):
        class Meta:
            model = EmployeeModel
            exclude = ["department"]

    assert "name" in EmployeeInterface._meta.fields
    assert "department" not in EmployeeInterface._meta.fields


@with_local_registry
def test_django_interface_specifying_only_certain_fields():
    class EmployeeInterface(DjangoInterface):
        class Meta:
            model = EmployeeModel
            fields = ["name"]

    assert "name" in EmployeeInterface._meta.fields
    assert "department" not in EmployeeInterface._meta.fields


@with_local_registry
def test_django_interface_inheritance_and_extension():
    class BaseInterface(DjangoInterface):
        class Meta:
            model = EmployeeModel
            fields = ["name"]

    class ExtendedInterface(BaseInterface):
        class Meta:
            model = ManagerModel
            fields = ["managed_department"]

    assert "managed_department" in ExtendedInterface._meta.fields


@with_local_registry
def test_django_interface_custom_meta_class_functionality():
    class CustomMetaInterface(DjangoInterface):
        class Meta:
            model = EmployeeModel
            name = "CustomInterface"
            fields = "__all__"

    assert CustomMetaInterface._meta.name == "CustomInterface"


@with_local_registry
def test_django_interface_type_checking_for_fields_and_exclude():
    with pytest.raises(TypeError):

        class InvalidFieldsInterface(DjangoInterface):
            class Meta:
                model = EmployeeModel
                fields = "name"

    with pytest.raises(TypeError):

        class InvalidExcludeInterface(DjangoInterface):
            class Meta:
                model = EmployeeModel
                exclude = "department"


@with_local_registry
def test_django_interface_custom_connections():
    class CustomConnection(Connection):
        test = String()

        def resolve_test():
            return "test"

        class Meta:
            abstract = True

    class EmployeeInterface(DjangoInterface):
        class Meta:
            model = EmployeeModel
            connection_class = CustomConnection
            fields = "__all__"

    print(EmployeeInterface._meta.connection, EmployeeInterface._meta)
    assert "test" in EmployeeInterface._meta.connection._meta.fields
