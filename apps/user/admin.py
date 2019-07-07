from django.contrib import admin
from .models import UserProfile, FavouriteCourse, UserComment, FavouriteOrganization, FavouriteTeacher


class FavouriteCourseInline(admin.TabularInline):
    model = FavouriteCourse
    extra = 1


class FavouriteOrganizationInline(admin.TabularInline):
    model = FavouriteOrganization
    extra = 1


class FavouriteTeacherInline(admin.TabularInline):
    model = FavouriteTeacher
    extra = 1


class UserCommentInline(admin.TabularInline):
    model = UserComment
    extra = 1


class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        ("基础信息", {"fields": ["nick_name", "birthday", "gender",
                             "address", "mobile", "profile_photo"]}),
    ]
    inlines = (FavouriteCourseInline, FavouriteOrganizationInline,
               FavouriteTeacherInline, UserCommentInline, )


admin.site.register(UserProfile, UserAdmin)
