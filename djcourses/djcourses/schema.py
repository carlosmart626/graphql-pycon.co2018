import graphene

from graphene import relay
from rx import Observable
from django.contrib.auth.models import User
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.debug import DjangoDebug

from courses.schemas import CourseNode
from profiles.schemas import ProfileNode, UserNode
from profiles.mutations import UpdateProfile, LoginUser
from courses.mutations import CreateCourse, UpdateCourse


class Query(graphene.ObjectType):
    hello = graphene.String()
    user = relay.Node.Field(UserNode)
    users = DjangoFilterConnectionField(UserNode)

    course = relay.Node.Field(CourseNode)
    courses = DjangoFilterConnectionField(CourseNode)

    me = graphene.Field(UserNode)

    debug = graphene.Field(DjangoDebug, name='__debug')

    def resolve_me(self, info):
        return UserNode.get_node(info, info.context.user.id)

    def resolve_hello(self, info, **kwargs):
        return 'world'


class Mutations(graphene.ObjectType):
    create_course = CreateCourse.Field()
    update_course = UpdateCourse.Field()
    update_profile = UpdateProfile.Field()


class Subscription(graphene.ObjectType):

    count_seconds = graphene.Int(up_to=graphene.Int())
    sub_user = graphene.Field(
        UserNode, description='subscribe to updated user', username=graphene.String())

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


schema = graphene.Schema(
    query=Query,
    mutation=Mutations,
    subscription=Subscription)


class AuthQuery(graphene.ObjectType):
    node = relay.Node.Field()


class AuthMutation(graphene.ObjectType):
    login_user = LoginUser.Field()


auth_schema = graphene.Schema(query=AuthQuery, mutation=AuthMutation)
