import graphene


class UUIDInput(graphene.InputObjectType):
    id = graphene.InputField(graphene.UUID, required=True)
