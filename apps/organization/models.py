from django.db import models
from datetime import datetime


class CityDict(models.Model):
    name = models.CharField("城市", max_length=20, default="")
    description = models.CharField("描述", max_length=200, default="")
    add_time = models.DateTimeField("添加时间", default=datetime.now)

    class Meta:
        verbose_name = "城市"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

def org_image_upload_path(instance, filename):
    return "image/org_{0}/{1}".format(instance.id, filename)


class Organization(models.Model):
    category_choices = (
        ("pxjg", "培训机构"),
        ("gx", "高校"),
        ("gr", "个人"),
    )
    name = models.CharField("机构名称", max_length=50, default="")
    description = models.CharField("机构描述", max_length=200, default="")
    category = models.CharField("机构类别", max_length=5, choices=category_choices, default="pxjg")
    click_nums = models.IntegerField("点击数", default=0)
    tag = models.CharField("机构标签", max_length=10, default="全国知名")
    fav_nums = models.IntegerField("收藏数", default=0)
    students = models.IntegerField("学习人数", default=0)
    course_nums = models.IntegerField("课程数", default=0)
    image = models.ImageField("logo", upload_to=org_image_upload_path, max_length=100)
    address = models.CharField("机构地址", max_length=150, )
    city = models.ForeignKey(CityDict, verbose_name="所在城市", on_delete=models.CASCADE)
    add_time = models.DateTimeField("添加时间", default=datetime.now)

    class Meta:
        verbose_name = "课程机构"
        verbose_name_plural = verbose_name

    def get_teacher_nums(self):
        return self.teacher_set.all().count()

    def __str__(self):
        return self.name


def teacher_image_upload_path(instance, filename):
    return "image/teacher_{0}/{1}".format(instance.id, filename)

class Teacher(models.Model):
    org = models.ForeignKey(Organization, verbose_name='所属机构', on_delete=models.CASCADE)
    name = models.CharField('教师名', max_length=50)
    work_years = models.IntegerField('工作年限', default=0)
    work_company = models.CharField('就职公司', max_length=50)
    work_position = models.CharField('公司职位', max_length=50)
    points = models.CharField('教学特点', max_length=50)
    click_nums = models.IntegerField('点击数', default=0)
    fav_nums = models.IntegerField('收藏数', default=0)
    teacher_age = models.IntegerField('年龄', default=25)
    image = models.ImageField("头像", default="image/default.png", upload_to=teacher_image_upload_path)
    add_time = models.DateTimeField("添加时间", default=datetime.now)

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "[{0}]的教师: {1}".format(self.org, self.name)

    def get_course_nums(self):
        return self.course_set.all().count()
