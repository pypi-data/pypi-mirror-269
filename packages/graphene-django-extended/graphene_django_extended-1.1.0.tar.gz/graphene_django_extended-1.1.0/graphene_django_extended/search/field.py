from functools import partial

import graphene
from graphene.relay.node import Node, NodeField


# TODO add dynamic parameters instead of hardcoding the fields
class SearchNodeField(NodeField):
    def __init__(self, node, type_=False, **kwargs):
        """
        We override the default NodeField to remove the required flag on the id field, and to add extra querying extension arguments.
        """
        assert issubclass(node, Node), "NodeField can only operate in Nodes"
        self.node_type = node
        self.field_type = type_
        global_id_type = node._meta.global_id_type

        super(NodeField, self).__init__(
            # If we don't specify a type, the field type will be the node interface
            type_ or node,
            id=global_id_type.graphene_type(
                required=False, description="The ID of the object"
            ),
            x_slug=graphene.String(
                required=False, description="The slug of the object."
            ),
            url=graphene.String(required=False, description="The url of the object."),
            **kwargs,
        )
