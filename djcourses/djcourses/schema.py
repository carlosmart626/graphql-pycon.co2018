import graphene
from graphene import relay
from rx import Observable
from graphene_django.filter import DjangoFilterConnectionField
from courses.schemas import CourseNode
from profiles.schemas import ProfileNode, UserNode
from django.contrib.auth.models import User


class Query(graphene.ObjectType):
    hello = graphene.String()
    user = relay.Node.Field(UserNode)
    users = DjangoFilterConnectionField(UserNode)

    course = relay.Node.Field(CourseNode)
    courses = DjangoFilterConnectionField(CourseNode)

    def resolve_hello(self, info, **kwargs):
        return 'world'


class Subscription(graphene.ObjectType):

    count_seconds = graphene.Int(up_to=graphene.Int())
    sub_user = graphene.Field(
        UserNode, description='subscribe to updated product', username=graphene.String())

    def resolve_count_seconds(root, info, up_to=5):
        return Observable.interval(1000)\
                         .map(lambda i: "{0}".format(i))\
                         .take_while(lambda i: int(i) <= up_to)

    def resolve_sub_user(root, info, *args, **kwargs):
        username = kwargs.get('username')

        def get_object(observer):
            instance = User.objects.get(username=username)
            return instance
        return Observable.interval(1000) \
            .map(lambda s: get_object(s)) \
            .share()


schema = graphene.Schema(query=Query, subscription=Subscription)
