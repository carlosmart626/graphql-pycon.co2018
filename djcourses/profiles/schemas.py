import graphene
from graphene import relay
from graphene_django.types import DjangoObjectType

from .models import Profile
from .models import User


class ProfileNode(DjangoObjectType):

    class Meta:
        model = Profile
        exclude_fields = ()
        interfaces = (relay.Node, )


class UserNode(DjangoObjectType):

    class Meta:
        model = User
        filter_fields = []
        exclude_fields = ('password', 'is_staff', 'is_superuser', )
        interfaces = (relay.Node, )
