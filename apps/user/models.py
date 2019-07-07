from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from apps.course.models import Course
from apps.organization.models import Teacher, Organization


def user_image_directory_path(instance, filename):
    return "image/user_{0}/{1}".format(instance.id, filename)


class UserProfile(AbstractUser):
    gender_choices = (
        ("male", "男"),
        ("female", "女"),
    )

    nick_name = models.CharField("昵称", max_length=50, default="")
    birthday = models.DateTimeField("出生日期", null=True, blank=True)
    gender = models.CharField("性别", max_length=10, choices=gender_choices, default="male")
    address = models.CharField("地址", max_length=100, default="")
    mobile = models.CharField("手机号码", max_length=15, default="")
    image = models.ImageField("头像", upload_to=user_image_directory_path, default="image/default.png",
                                      max_length=100)
    course = models.ManyToManyField(Course, through="UserCourse", related_name="user_course")
    favourite_course = models.ManyToManyField(Course, through="FavouriteCourse", related_name="user_favourite_course")
    favourite_teacher = models.ManyToManyField(Teacher, through="FavouriteTeacher",
                                               related_name="user_favourite_teacher")
    favourite_organization = models.ManyToManyField(Organization, through="FavouriteOrganization",
                                                    related_name="user_favourite_organization")

    comments = models.ManyToManyField(Course, through="UserComment", related_name="user_comment")

    test_field = models.DateTimeField("test_field", default=datetime.now)
    test_field2 = models.DateTimeField("test_field", default=datetime.now)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name


class UserCourse(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    add_time = models.DateTimeField("添加时间", default=datetime.now)


class FavouriteCourse(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    add_time = models.DateTimeField("添加时间", default=datetime.now)


class FavouriteTeacher(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    add_time = models.DateTimeField("添加时间", default=datetime.now)


class FavouriteOrganization(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    add_time = models.DateTimeField("添加时间", default=datetime.now)


class UserComment(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    comment = models.CharField("评论", max_length=200, default="")
    add_time = models.DateTimeField("添加时间", default=datetime.now)

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name
