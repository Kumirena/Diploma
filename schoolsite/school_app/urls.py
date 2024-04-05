from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('courses/', views.CourseListView.as_view(), name='courses'),
    path('courses/<int:pk>', views.CourseDetailView.as_view(), name='course_detail'),
    path('teachers/', views.TeacherListView.as_view(), name='teachers'),
    path('teachers/<int:pk>', views.TeacherDetailView.as_view(), name='teacher_detail'),
    path('tutors/', views.TutorListView.as_view(), name='tutors'),
    path('tutors/<int:pk>', views.TutorDetailView.as_view(), name='tutor_detail'),
    path('students/', views.StudentListView.as_view(), name='students'),
    path('students/<int:pk>', views.StudentDetailView.as_view(), name='student_detail'),
    path('lessons/', views.LessonListView.as_view(), name='lessons'),
    path('lessons/<int:pk>', views.LessonDetailView.as_view(), name='lesson_detail'),
    path('mygrades/', views.StudentGradesListView.as_view(), name='grades'),
    path('lessons/create/', views.LessonCreate.as_view(), name='lesson_create'),
    path('lessons/<int:pk>/delete/', views.LessonDelete.as_view(), name='lesson_delete'),
    path('grades/<int:pk>/update/', views.GradeUpdate.as_view(), name='grades_update')
]