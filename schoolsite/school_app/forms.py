from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from school_app.models import User, Student, Tutor, Teacher, Course, Lesson


class StudentSignUpForm(UserCreationForm):
    """ Форма регистрации для студента. """

    name = forms.CharField(min_length=10, max_length=100, label='Имя и фамилия')
    email = forms.EmailField(min_length=5, max_length=100, label='Электронная почта')
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Курс(-ы), на котором(-ых) будете обучаться:'
    )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user,
                                         name=self.cleaned_data.get('name'),
                                         email=self.cleaned_data.get('email'))
        student.course_set.add(*self.cleaned_data.get('courses'))
        return user


class TutorSignUpForm(UserCreationForm):
    """ Форма регистрации для куратора. """

    name = forms.CharField(min_length=10, max_length=100, label='Имя и фамилия')
    email = forms.EmailField(min_length=5, max_length=100, label='Электронная почта')
    education = forms.CharField(max_length=100, label='Образование')
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Курс(-ы), на котором(-ых) будете Куратором:'
    )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_mentor = True
        user.save()
        tutor = Tutor.objects.create(user=user, name=self.cleaned_data.get('name'),
                                       email=self.cleaned_data.get('email'),
                                       education=self.cleaned_data.get('education'))
        tutor.course_set.add(*self.cleaned_data.get('courses'))
        return user


class TeacherSignUpForm(UserCreationForm):
    """ Форма регистрации для преподавателя. """

    name = forms.CharField(min_length=10, max_length=100, label='Имя и фамилия')
    email = forms.EmailField(min_length=5, max_length=100, label='Электронная почта')
    education = forms.CharField(max_length=100, label='Образование')
    company = forms.CharField(max_length=100, label='Компания')
    experience = forms.IntegerField(label='Опыт в годах')
    role = forms.ChoiceField(choices=[('Семинарист', 'Семинарист'), ('Лектор', 'Лектор')], label='Роль')
    courses = forms.ModelMultipleChoiceField(queryset=Course.objects.all(),
                                             widget=forms.CheckboxSelectMultiple,
                                             required=False,
                                             label='Курс(-ы), на котором(-ых) будете преподавать:')

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_teacher = True
        user.save()
        teacher = Teacher.objects.create(user=user, name=self.cleaned_data.get('name'),
                                         email=self.cleaned_data.get('email'),
                                         education=self.cleaned_data.get('education'),
                                         company=self.cleaned_data.get('company'),
                                         experience=self.cleaned_data.get('experience'),
                                         role=self.cleaned_data.get('role'))
        teacher.course_set.add(*self.cleaned_data.get('courses'))
        return user