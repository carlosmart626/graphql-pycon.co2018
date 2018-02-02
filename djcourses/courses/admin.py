from django.contrib import admin
from .models import Course


class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'teacher', )
    filter_horizontal = ('enrolled_students', )


admin.site.register(Course, CourseAdmin)
