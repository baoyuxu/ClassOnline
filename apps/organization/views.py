# organization/views.py

from django.shortcuts import render

from django.views.generic import View
from .models import Organization,CityDict,Teacher
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from apps.utils.mixin_utils import LoginRequiredMixin
from django.http import HttpResponse
from .forms import UserAskForm
from apps.course.models import Course
from apps.user.models import FavouriteTeacher, FavouriteOrganization, FavouriteCourse
from django.contrib.auth import authenticate
from django.db.models import Q
from django.conf import settings
from datetime import datetime

class OrgView(View):
    '''课程机构'''

    def get(self, request):
        # 所有课程机构
        all_orgs = Organization.objects.all()

        # 所有城市
        all_citys = CityDict.objects.all()

        # 机构搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            # 在name字段进行操作,做like语句的操作。i代表不区分大小写
            # or操作使用Q
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))
        # 城市筛选
        city_id = request.GET.get('city','')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 类别筛选
        category = request.GET.get('ct','')
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 热门课程机构排名
        hot_orgs = all_orgs.order_by('-click_nums')[:3]
        # 学习人数和课程数筛选
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")
        # 有多少家机构
        org_nums = all_orgs.count()
        # 对课程机构进行分页
        # 尝试获取前台get请求传递过来的page参数
        # 如果是不合法的配置参数默认返回第一页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 这里指从allorg中取五个出来，每页显示5个
        p = Paginator(all_orgs, 2, request=request)
        orgs = p.page(page)

        for org in all_orgs:
            ans = 0
            for cour in Course.objects.all():
                if str(cour.course_org) == str(org.name):
                    ans = ans + 1
            org.course_nums = ans
            org.save()
        return render(request, "organization/org-list.html", {
            "all_orgs": orgs,
            "all_citys": all_citys,
            "org_nums": org_nums,
            'city_id':city_id,
            "category": category,
            'hot_orgs':hot_orgs,
            'sort':sort,
        })



class AddUserAskView(View):
    """
    用户添加咨询
    """
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            # 如果保存成功,返回json字符串,后面content type是告诉浏览器返回的数据类型
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            # 如果保存失败，返回json字符串,并将form的报错信息通过msg传递到前端
            return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type='application/json')



class OrgHomeView(View):
    '''机构首页'''

    def get(self,request,org_id):
        current_page = 'home'
        # 根据id找到课程机构
        course_org = Organization.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()
        # 判断收藏状态
        has_fav = False
        if request.user.is_authenticated:
            if request.user.favourite_organization.all():
                has_fav = True
        # 反向查询到课程机构的所有课程和老师
        all_courses = course_org.course_set.all()[:4]
        all_teacher = course_org.teacher_set.all()[:2]
        return render(request,'organization/org-detail-homepage.html',{
            'course_org':course_org,
            'all_courses':all_courses,
            'all_teacher':all_teacher,
            'current_page':current_page,
            'has_fav':has_fav,
        })

class OrgCourseView(View):
    """
   机构课程列表页
    """
    def get(self, request, org_id):
        current_page = 'course'
        # 根据id取到课程机构
        course_org = Organization.objects.get(id= int(org_id))
        # 通过课程机构找到课程。内建的变量，找到指向这个字段的外键引用
        all_courses = course_org.course_set.all()
        # 判断收藏状态
        has_fav = False
        if request.user.is_authenticated:
            if request.user.favourite_organization.all():
                has_fav = True

        return render(request, 'organization/org-detail-course.html',{
           'all_courses':all_courses,
            'course_org': course_org,
            'current_page':current_page,
            'has_fav': has_fav,
        })


class OrgDescView(View):
    '''机构介绍页'''
    def get(self, request, org_id):
        current_page = 'desc'
        # 根据id取到课程机构
        course_org = Organization.objects.get(id= int(org_id))
        # 判断收藏状态
        has_fav = False
        if request.user.is_authenticated:
            if request.user.favourite_organization.all():
                has_fav = True
        return render(request, 'organization/org-detail-desc.html',{
            'course_org': course_org,
            'current_page':current_page,
            'has_fav': has_fav,
        })

class OrgTeacherView(View):
    """
   机构教师页
    """
    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = Organization.objects.get(id=int(org_id))
        all_teacher = course_org.teacher_set.all()
        # 判断收藏状态
        has_fav = False
        if request.user.is_authenticated:
            if request.user.favourite_organization.all():
                has_fav = True

        return render(request, 'organization/org-detail-teachers.html',{
           'all_teacher':all_teacher,
            'course_org': course_org,
            'current_page':current_page,
            'has_fav': has_fav,
        })

class AddFavView(View):
    """
    用户收藏和取消收藏
    """
    def post(self, request):
        id = request.POST.get('fav_id', 0)         # 防止后边int(fav_id)时出错
        type = request.POST.get('fav_type', 0)     # 防止int(fav_type)出错

        if not request.user.is_authenticated:
            # 未登录时返回json提示未登录，跳转到登录页面是在ajax中做的
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        if int(type) == 1:
            course = Course.objects.get(id=id)
            exist_record = FavouriteCourse.objects.filter(user_profile=request.user, course=course)
            print(course)
            print(1)
            print(exist_record)
            if exist_record:
                course.fav_nums -= 1
                course.save()
                exist_record.delete()
                return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
            else:
                FavouriteCourse(user_profile=request.user, course=course, add_time=datetime.now()).save()
                course.fav_nums += 1
                course.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
        elif int(type) == 2:
            org = Organization.objects.get(id=id)
            exist_record = FavouriteOrganization.objects.filter(user_profile=request.user, organization=org)
            print(2)
            print(exist_record)
            if exist_record:
                org.fav_nums -= 1
                org.save()
                exist_record.delete()
                return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
            else:
                FavouriteOrganization(user_profile=request.user, organization=org, add_time=datetime.now()).save()
                org.fav_nums += 1
                org.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
        elif int(type) == 3:
            teacher = Teacher.objects.get(id=id)
            exist_record = FavouriteTeacher.objects.filter(user_profile=request.user, teacher_id=id)
            print(3)
            print(exist_record)
            if exist_record:
                teacher.fav_nums -= 1
                teacher.save()
                exist_record.delete()
                return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
            else:
                FavouriteTeacher(user_profile=request.user, teacher=teacher, add_time=datetime.now()).save()
                teacher.fav_nums += 1
                teacher.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')

        return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')


# 讲师列表
class TeacherListView(View):
    def get(self, request):
        all_teachers = Teacher.objects.all()
        # 总共有多少老师使用count进行统计
        teacher_nums = all_teachers.count()

        # 搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            # 在name字段进行操作,做like语句的操作。i代表不区分大小写
            # or操作使用Q
            all_teachers = all_teachers.filter(name__icontains=search_keywords)
        # 人气排序
        sort = request.GET.get('sort','')
        if sort:
            if sort == 'hot':
                all_teachers = all_teachers.order_by('-click_nums')

        #讲师排行榜
        sorted_teacher = Teacher.objects.all().order_by('-click_nums')[:3]
        # 进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, 3, request=request)
        teachers = p.page(page)
        return render(request, "teacher/teachers-list.html", {
            "all_teachers": teachers,
            "teacher_nums": teacher_nums,
            'sorted_teacher':sorted_teacher,
            'sort':sort,
        })


#讲师详情
class TeacherDetailView(LoginRequiredMixin,View):
    def get(self,request,teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_nums += 1
        teacher.save()
        all_course = Course.objects.filter(teacher=teacher)
        # 教师收藏和机构收藏
        has_teacher_faved = False
        if request.user.favourite_teacher.filter(favouriteteacher__teacher=teacher):
            has_teacher_faved = True

        has_org_faved = False
        if request.user.favourite_organization.filter(favouriteorganization__organization=teacher.org):
            has_org_faved = True
        # 讲师排行榜
        sorted_teacher = Teacher.objects.all().order_by('-click_nums')[:3]
        # print(teacher.image)
        return render(request,'teacher/teacher-detail.html',{
            'teacher':teacher,
            'all_course':all_course,
            'sorted_teacher':sorted_teacher,
            'has_teacher_faved':has_teacher_faved,
            'has_org_faved':has_org_faved,
        })
