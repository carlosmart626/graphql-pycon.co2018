import graphene
from graphene import relay
from graphene_django.types import DjangoObjectType

from .models import Course


class CourseNode(DjangoObjectType):

    class Meta:
        model = Course
        filter_fields = {
            'title': ['exact', 'icontains', 'istartswith'],
            'teacher': ['exact'],
        }
        interfaces = (relay.Node, )
