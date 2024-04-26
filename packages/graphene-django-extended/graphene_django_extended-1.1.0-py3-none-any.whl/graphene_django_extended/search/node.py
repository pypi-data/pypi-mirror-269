import graphene

from .field import SearchNodeField


class SearchNode(graphene.relay.Node):
    @classmethod
    def Field(cls, node, *args, **kwargs):  # noqa: N802
        """
        We bypass the default relay type resolution method by reading the type, from which we will be able to infer the model with its own methods (get_node).
        """
        cls.node = node
        return SearchNodeField(cls, node, *args, **kwargs)
        # return SearchNodeField(cls, node, *args, **kwargs)

    @classmethod
    def node_resolver(cls, only_type, root, info, **kwargs):
        """
        If the id is provided, we will use the default relay method to resolve the node.
        """
        id = kwargs.pop("id", None)
        if id:
            return cls.get_node_from_global_id(info, id, only_type=only_type)
        return cls.get_node_from_unique_field(info, only_type=only_type, **kwargs)

    @classmethod
    def get_node_from_unique_field(cls, info, only_type=None, **kwargs):
        """
        If the id is not provided, we will use the get_node method from the node to resolve the node, provided it's extended to "get" with kwargs.
        """
        # print(info, info.context, cls.node)
        # _type, _id = cls.resolve_global_id(info, global_id)

        # graphene_type = info.schema.get_type("OrganizationNode")
        # if graphene_type is None:
        #    raise Exception(f'Relay Node "{_type}" not found in schema')

        # !!! This is an ugly fix
        # We should find a better way to infer the Field on which
        # we are calling the get_node method.
        # Be careful with classmethods, as we can't store data on the classes
        graphene_type = info.return_type.graphene_type
        get_node = getattr(graphene_type, "get_node", None)
        if get_node:
            return get_node(info, None, **kwargs)


class InterfaceNode(graphene.relay.Node):
    @classmethod
    def get_node_from_global_id(cls, info, global_id, only_type=None):
        # print("only_type", only_type, cls)
        passed_only_type = (
            only_type if not only_type.__name__.endswith("Interface") else None
        )
        return super(InterfaceNode, cls).get_node_from_global_id(
            info, global_id, only_type=passed_only_type
        )


class SearchInterfaceNode(SearchNode, InterfaceNode):
    pass
