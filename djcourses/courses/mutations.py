import graphene
from graphene.types.datetime import DateTime
from django.contrib.auth.models import User

from .schemas import CourseNode
from .models import Course


class CourseInput(graphene.InputObjectType):
    title = graphene.String(required=True)
    description = graphene.String()
    teacher_id = graphene.Int(required=True)
    

class CourseUpdateInput(CourseInput):
    id = graphene.Int(required=True)
    is_active = graphene.Boolean()


class CreateCourse(graphene.Mutation):

    class Arguments:
        course_data = CourseInput()

    ok = graphene.Boolean()
    course = graphene.Field(CourseNode)

    def mutate(self, info, course_data):
        try:
            username = profile_data.pop('teacher_username')
            user = User.objects.get(username=username)
            course = Course.objects.create(
                title=title,
                description=description,
                teacher=user)
            ok = True

        except Exception as e:
            ok = False
            profile = None

        return CreateCourse(ok=ok, course=course)


class UpdateCourse(graphene.Mutation):

    class Arguments:
        course_data = CourseUpdateInput()

    ok = graphene.Boolean()
    course = graphene.Field(CourseNode)

    def mutate(self, info, course_data):

        try:
            course_id = course_data.pop('id')
            course = Course.objects.get(id=course_id)
            course.__dict__.update(course_data)
            course.save()
            ok = True

        except Exception as e:
            ok = False
            profile = None

        return CreateCourse(ok=ok, course=course)
