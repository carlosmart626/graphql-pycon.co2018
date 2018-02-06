import graphene
import graph_auth.schema

from graphene import relay
from rx import Observable
from django.contrib.auth.models import User
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.debug import DjangoDebug

from courses.schemas import CourseNode
from profiles.schemas import ProfileNode, UserNode
from profiles.mutations import UpdateProfile
from courses.mutations import CreateCourse, UpdateCourse


class Query(graphene.ObjectType):
    hello = graphene.String()
    user = relay.Node.Field(UserNode)
    users = DjangoFilterConnectionField(UserNode)

    course = relay.Node.Field(CourseNode)
    courses = DjangoFilterConnectionField(CourseNode)

    def resolve_hello(self, info, **kwargs):
        return 'world'


class Mutations(graphene.ObjectType):
    create_course = CreateCourse.Field()
    update_course = UpdateCourse.Field()
    update_profile = UpdateProfile.Field()


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


schema = graphene.Schema(query=Query, mutation=Mutations, subscription=Subscription)


class Query(graph_auth.schema.Query, graphene.ObjectType):
    node = relay.Node.Field()
    debug = graphene.Field(DjangoDebug, name='__debug')


class Mutation(graphene.ObjectType):
    register_user = graph_auth.schema.RegisterUser.Field()
    login_user = graph_auth.schema.LoginUser.Field()
    reset_password = graph_auth.schema.ResetPassword.Field()
    update_user = graph_auth.schema.UpdateUser.Field()
    debug = graphene.Field(DjangoDebug, name='__debug')


auth_schema = graphene.Schema(query=Query, mutation=Mutation)
