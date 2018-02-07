import django
import graphene
from graphene.types.datetime import DateTime
from graphene import relay
from django.contrib.auth.models import User

from .schemas import ProfileNode, UserNode
from .models import Profile


class ProfileInput(graphene.InputObjectType):
    user_name = graphene.String(required=True)
    bio = graphene.String()
    location = graphene.String()
    birth_date = DateTime()


class UpdateProfile(graphene.Mutation):

    class Arguments:
        profile_data = ProfileInput()

    ok = graphene.Boolean()
    profile = graphene.Field(ProfileNode)

    def mutate(self, info, profile_data):

        try:
            user_name = profile_data.pop('user_name')
            profile = Profile.objects.get(user__username=user_name)
            profile.__dict__.update(profile_data)
            profile.save()
            ok = True

        except Exception as e:
            ok = False
            profile = None

        return UpdateProfile(ok=ok, profile=profile)


class LoginUser(relay.ClientIDMutation):
    class Input:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserNode)

    @classmethod
    def mutate_and_get_payload(root, info, *args, **input):
        model = User

        params = {
            model.USERNAME_FIELD: input.get(model.USERNAME_FIELD, ''),
            'password': input.get('password')
        }

        user = django.contrib.auth.authenticate(**params)

        if user:
            user.is_current_user = True
            return LoginUser(ok=True, user=user)
        else:
            return LoginUser(ok=False, user=None)
