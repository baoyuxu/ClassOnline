from django.db import models
from froala_editor.fields import FroalaField
from datetime import datetime
from apps.organization.models import Teacher, Organization

def course_image_upload_path(instance, filename):
    return "course_{0}/image/{1}".format(instance.id, filename)
class Course(models.Model):
    rank_choices = (
        ("cj", "初级"),
        ("zj", "中级"),
        ("gj", "高级"),
    )

    name = models.CharField("课程名称", max_length=50)
    description = models.CharField("课程描述", max_length=300)
    detail = FroalaField(default="")
    rank = models.CharField("课程等级", choices=rank_choices, max_length=2)
    learn_time = models.IntegerField("时长", default=0)
    students = models.IntegerField("学习人数", default=0)
    favourite_count = models.IntegerField("收藏人数", default=0)
    click_count = models.IntegerField("点击次数", default=0)
    is_banner = models.BooleanField("是否轮播", default=False)
    add_time = models.DateTimeField("", default=datetime.now)
    course_org = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name="所属机构", null=True, blank=True)
    category = models.CharField("课程类别",max_length=20, default="")
    teacher = models.ForeignKey(Teacher,verbose_name='讲师',null=True,blank=True,on_delete=models.CASCADE)
    you_need_know = models.CharField("课程须知",max_length=300,default="")
    teacher_tell = models.CharField("老师告诉你",max_length=300,default="")
    image = models.ImageField("封面图",upload_to=course_image_upload_path,max_length=100, default="image/default.png")

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name

    def get_chapter_count(self):
        return self.lesson_set.all().count()



class Lesson(models.Model):
    course = models.ForeignKey(Course,verbose_name="课程", on_delete=models.CASCADE)
    name = models.CharField("章节名", max_length=50)
    add_time = models.DateTimeField("添加时间", default=datetime.now)

    class Meta:
        verbose_name = "章节"
        verbose_name_plural = verbose_name

    def get_chapter_video(self):
        return self.video_set.all()



class Video(models.Model):
    chapter = models.ForeignKey(Lesson, verbose_name="章节名", on_delete=models.CASCADE)
    name  = models.CharField("视频名", max_length=50, default="")
    url = models.CharField("视频地址", max_length=200, default="")
    learn_time = models.IntegerField("时长", default=0)
    add_time = models.DateTimeField("添加时间", default=datetime.now)

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name

def course_resource_upload_path(instance, filename):
    return "course_{0}/resource/{1}".format(instance.course.id, filename)

class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name="课程", on_delete=models.CASCADE)
    name = models.CharField("名称", max_length=50, default="")
    download = models.FileField("资源文件", upload_to=course_resource_upload_path, max_length=100)
    add_time = models.DateTimeField("添加时间", default=datetime.now)

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name
