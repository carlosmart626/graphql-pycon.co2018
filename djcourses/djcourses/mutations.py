import django
import graphene
from graphene import relay
from profiles.schemas import UserNode
from django.contrib.auth.models import User


class LoginUser(relay.ClientIDMutation):
    class Input:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserNode)

    @classmethod
    def mutate_and_get_payload(root, info, *args, **input):
        model = User
        print("Input", input, args, info, root)

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