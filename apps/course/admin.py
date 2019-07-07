from django.contrib import admin
from .models import Course

class CourseAdmin(admin.ModelAdmin):
    list_display = ["name"]
    fieldsets = (
        (None, {"fields":
                ["name", "description", "detail", "rank",
                 "learn_time", "students", "favourite_count", "image",
                 "is_banner", "add_time", "course_org",
                 "category", "teacher", "you_need_know", "teacher_tell"]}),
    )
admin.site.register(Course, CourseAdmin)

