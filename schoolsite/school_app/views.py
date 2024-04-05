from django.shortcuts import render
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView, DeleteView
from school_app.forms import StudentSignUpForm, TeacherSignUpForm, TutorSignUpForm
from school_app.models import calc_online_school_stats
from school_app.models import User, Course, Teacher, Student, Tutor, Lesson, Grade
from school_app.filters import CourseFilter, TeacherFilter, StudentFilter, TutorFilter, LessonFilter
from school_app.decorators import teacher_required, student_required, tutor_required


class CourseListView(generic.ListView):
    """ Отображение информации о курсах. """

    model = Course

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = CourseFilter(self.request.GET, queryset=self.get_queryset())
        return context


class CourseDetailView(generic.DetailView):
    """ Отображение детальной информации о курсе. """
    model = Course


class TeacherListView(generic.ListView):
    """ Отображение информации о преподавателях. """
    model = Teacher

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = TeacherFilter(self.request.GET, queryset=self.get_queryset())
        return context


class TeacherDetailView(generic.DetailView):
    """ Отображение детальной информации о преподавателе. """
    model = Teacher


class StudentListView(LoginRequiredMixin, generic.ListView):
    """ Отображение информации о студентах. """

    model = Student
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = StudentFilter(self.request.GET, queryset=self.get_queryset())
        return context


class StudentDetailView(generic.DetailView):
    """ Отображение детальной информации о студенте. """
    model = Student


class TutorListView(LoginRequiredMixin, generic.ListView):
    """ Отображение информации о кураторах. """

    model = Tutor
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = TutorFilter(self.request.GET, queryset=self.get_queryset())
        return context


class MentorDetailView(generic.DetailView):
    """ Отображение детальной информации о кураторе. """
    model = Tutor


class LessonListView(LoginRequiredMixin, generic.ListView):
    """ Отображение информации об уроках. """

    model = Lesson
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = LessonFilter(self.request.GET, queryset=self.get_queryset())
        return context

    def get_queryset(self):
        if self.request.user.is_student:
            return Lesson.objects.filter(course_id__student__user=self.request.user)
        else:
            return Lesson.objects.all()


class LessonDetailView(generic.DetailView):
    """ Отображение с детальной информацией об уроке. """
    model = Lesson


class SignUpView(TemplateView):
    """ Отображение для регистрации. """
    template_name = 'registration/signup.html'


class StudentSignUpView(CreateView):
    """ Отображение для регистрации студента. """

    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return index(self.request)


class TeacherSignUpView(CreateView):
    """ Отображение для регистрации преподавателя. """

    model = User
    form_class = TeacherSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return index(self.request)


class TutorSignUpView(CreateView):
    """ Отображение для регистрации куратора. """

    model = User
    form_class = TutorSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'tutor'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return index(self.request)


@method_decorator([login_required, student_required], name='dispatch')
class StudentGradesListView(LoginRequiredMixin, generic.ListView):
    """ Отображение оценок студента. """

    model = Student
    template_name ='school_app/student_grades_list.html'

    def get_queryset(self):
        return Student.objects.filter(user=self.request.user)


@method_decorator([login_required, teacher_required], name='dispatch')
class LessonCreate(CreateView):
    """ Отображение для создания урока. """

    model = Lesson
    fields = ['title', 'course_id', 'teacher_id', 'link']
    success_url = reverse_lazy('lessons')


@method_decorator([login_required, teacher_required], name='dispatch')
class LessonDelete(DeleteView):
    """ Отображение для удаления урока. """

    model = Lesson
    success_url = reverse_lazy('lessons')


@method_decorator([login_required, teacher_required], name='dispatch')
class GradeUpdate(UpdateView):
    """ Отображение для изменения урока. """

    model = Grade
    fields = ['course', 'student', 'homework1', 'homework2', 'project', 'final_mark']
    success_url = reverse_lazy('students')


def index(request):
    """ Функция отображения для домашней страницы сайта. """

    num_courses, num_teachers, num_students = calc_online_school_stats()
    return render(request, 'index.html',
                  context={'num_courses': num_courses,
                           'num_teachers': num_teachers,
                           'num_students': num_students})