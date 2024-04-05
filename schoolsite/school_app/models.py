from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Модель для пользователя.
    Пользователь может принадлежать к одной из трех групп: студент, преподаватель, куратор.
    """
    is_student = models.BooleanField(default=False, verbose_name='Студент')
    is_teacher = models.BooleanField(default=False, verbose_name='Преподаватель')
    is_tutor = models.BooleanField(default=False, verbose_name='Куратор')


class Teacher(models.Model):
    """ Модель для преподавателя. """

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False, verbose_name='Имя и фамилия преподавателя')
    email = models.EmailField(max_length=100, blank=True, null=True, verbose_name='E-mail преподавателя')
    role = models.CharField(max_length=20, blank=True, null=True, verbose_name='Роль преподавателя',
                            choices=[('Семинарист', 'Семинарист'), ('Лектор', 'Лектор')])
    education = models.CharField(max_length=100, blank=True, null=True, verbose_name='Образование преподавателя (ВУЗ)')
    company = models.CharField(max_length=100, blank=True, null=True, verbose_name='Компания')
    experience = models.SmallIntegerField(blank=True, null=True, verbose_name='Опыт в годах')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('teacher_detail', args=[str(self.id)])

    class Meta:
        ordering = ['name']


class Student(models.Model):
    """ Модель для студента. """

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False, verbose_name='Имя студента')
    email = models.EmailField(max_length=100, blank=True, null=True, verbose_name='E-mail студента')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('student_detail', args=[str(self.id)])

    class Meta:
        ordering = ['name']


class Tutor(models.Model):
    """ Модель для куратора. """

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, blank=False, verbose_name='Имя куратора')
    email = models.EmailField(max_length=100, blank=True, null=True, verbose_name='E-mail куратора')
    education = models.CharField(max_length=100, blank=True, null=True, verbose_name='Образование куратора')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tutor_detail', args=[str(self.id)])

    class Meta:
        ordering = ['name']


class Course(models.Model):
    """ Модель для курса. """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=False, verbose_name='Название курса')
    description = models.TextField(blank=False, verbose_name='Описание курса')
    duration = models.PositiveSmallIntegerField(blank=False, default=6, verbose_name='Продолжительность курса',
                                                choices=[(6, '6 месяцев'), (12, '12 месяцев'), (18, '18 месяцев')])
    price = models.PositiveIntegerField(blank=False, default=50000, verbose_name='Стоимость курса')
    student = models.ManyToManyField(Student, through='Grade')
    teacher = models.ManyToManyField(Teacher)
    tutor = models.ManyToManyField(Tutor)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('course_detail', args=[str(self.id)])

    class Meta:
        ordering = ['id']


class Lesson(models.Model):
    """ Модель для урока. """

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=40, blank=False, verbose_name='Тема занятия')
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    teacher_id = models.ForeignKey(Teacher, on_delete=models.SET_NULL, blank=True, null=True,
                                   verbose_name='Преподаватель')
    link = models.CharField(max_length=100, blank=True, null=True, verbose_name='Ссылка на занятие в Zoom')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('lesson_detail', args=[str(self.id)])

    class Meta:
        ordering = ['course_id']


class Grade(models.Model):
    """ Модель для оценок. """

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='Студент')
    homework1 = models.SmallIntegerField(blank=True, null=True, verbose_name='Оценка за 1 ДЗ',
                                         choices=[(2, 2), (3, 3), (4, 4), (5, 5)])
    homework2 = models.SmallIntegerField(blank=True, null=True, verbose_name='Оценка за 2 ДЗ',
                                         choices=[(2, 2), (3, 3), (4, 4), (5, 5)])
    project = models.SmallIntegerField(blank=True, null=True, verbose_name='Оценка за проект',
                                       choices=[(2, 2), (3, 3), (4, 4), (5, 5)])
    final_mark = models.FloatField(blank=True, null=True, verbose_name='Оценка за курс')

    class Meta:
        ordering = ['course']


def calc_online_school_stats():
    """ Расчёт основных показателей онлайн-школы для вывода на главной странице. """

    num_courses = Course.objects.all().count()
    num_teachers = Teacher.objects.all().count()
    num_students = Student.objects.all().count()
    return num_courses, num_teachers, num_students


def calc_student_final_mark(instance, **kwargs):
    """ Автоматический расчёт итоговой оценки за курс, если выставлены оценки за ДЗ1, ДЗ2 и проект. """

    if instance.homework1 and instance.homework2 and instance.project:
        instance.final_mark = 1 / 3 * sum([instance.homework1, instance.homework2, instance.project])
    return instance.final_mark


pre_save.connect(calc_student_final_mark, sender=Grade, dispatch_uid=__file__)
def calc_online_school_stats():
    """ Расчёт основных показателей онлайн-школы для вывода на главной странице. """

    num_courses = Course.objects.all().count()
    num_teachers = Teacher.objects.all().count()
    num_students = Student.objects.all().count()
    return num_courses, num_teachers, num_students


def calc_student_final_mark(instance, **kwargs):
    """ Автоматический расчёт итоговой оценки за курс, если выставлены оценки за ДЗ1, ДЗ2 и проект. """

    if instance.homework1 and instance.homework2 and instance.project:
        instance.final_mark = 1 / 3 * sum([instance.homework1, instance.homework2, instance.project])
    return instance.final_mark


pre_save.connect(calc_student_final_mark, sender=Grade, dispatch_uid=__file__)