import graphene
from graphene.types.datetime import DateTime

from .schemas import ProfileNode
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
