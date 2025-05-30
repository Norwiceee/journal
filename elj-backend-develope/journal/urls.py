from django.urls import path, include
from rest_framework.routers import DefaultRouter

from journal import views


router = DefaultRouter()
router.register('study_years', views.StudyYearViewSet)
router.register('subjects', views.SubjectViewSet)
router.register('marks', views.MarkViewSet, basename='mark')
router.register('student_classes', views.StudentClassViewSet)
router.register('students', views.StudentViewSet)
router.register('journals', views.JournalAPIView, basename='journal')
router.register('school', views.SchoolViewSet)

app_name = 'journal'

urlpatterns = [
    path('', include(router.urls)),
]
