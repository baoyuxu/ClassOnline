from django.contrib import admin
from .models import Course, CourseResource, Lesson, Video

class CourseAdmin(admin.ModelAdmin):
    list_display = ["name"]
    fieldsets = (
        (None, {"fields":
                ["name", "description", "detail", "rank",
                 "learn_time", "students", "favourite_count", "image",
                 "is_banner", "add_time", "course_org",
                 "category", "teacher", "you_need_know", "teacher_tell"]}),
    )

class LessonAdmin(admin.ModelAdmin):
    list_display = ["name"]
    fieldsets = (
        (None, {"fields":
               ["course", "name", "add_time"]}),
    )
class VideoAdmin(admin.ModelAdmin):
    list_display = ["name"]
    fieldsets = (
        (None, {"fields":[
            "lesson", "name", "url", "learn_time", "add_time"
        ]}),
    )
class CourseResourceAdmin(admin.ModelAdmin):
    list_display = ["name"]
    fieldsets = (
        (None, {"fields":[
            "course", "name", "download", "add_time"
        ]}),
    )

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(CourseResource, CourseResourceAdmin)

