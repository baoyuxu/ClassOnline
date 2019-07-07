from django.contrib import admin
from .models import CityDict, Organization, Teacher

class CityDictAdmin(admin.ModelAdmin):
    list_display = ["name", ]
    fieldsets = (
        ("城市信息", {"fields": ["name", "description", "add_time"]}),
    )

class OrganizationAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": [
            "name", "image", "description", "category", "click_nums", "tag",
            "fav_nums", "students", "course_nums", "address",
            "city", "add_time"
        ]}),
    )
class TeacherAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields":[
            "org", "name", "image", "work_years", "work_company", "work_position",
            "points", "click_nums", "fav_nums", "teacher_age", "add_time"
        ]}),
    )

admin.site.register(CityDict, CityDictAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Teacher, TeacherAdmin)

