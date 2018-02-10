import graphene
from graphene import relay
from graphene_django.types import DjangoObjectType
from rest_framework_jwt.settings import api_settings

from .models import Profile
from .models import User


class Person(graphene.ObjectType):
    first_name = graphene.String()
    last_name = graphene.String()
    full_name = graphene.String()

    def resolve_full_name(self, info):
        return '{} {}'.format(self.first_name, self.last_name)


class ProfileNode(DjangoObjectType):

    class Meta:
        model = Profile
        exclude_fields = ()
        interfaces = (relay.Node, )


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        interfaces = (relay.Node, )
        exclude_fields = ('password', 'is_staff', 'is_superuser', )
        filter_fields = ['username', 'email']

    @classmethod
    def get_node(cls, info, id):
        user = super(UserNode, cls).get_node(info, id)
        if info.context.user.id and (user.id == info.context.user.id or info.context.user.is_staff):
            return user
        else:
            return None

    token = graphene.String()

    def resolve_token(self, info, **args):
        if self.id != info.context.user.id and \
            not getattr(self, 'is_current_user', False):
                return None

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(self)
        token = jwt_encode_handler(payload)

        return token
