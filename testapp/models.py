from datetime import datetime
from os.path import splitext

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import DateTimeRangeField, ArrayField, HStoreField, CICharField  # , JSONField
from django.contrib.postgres.indexes import GistIndex
from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField
from django.views.generic.dates import BaseDateListView
from localflavor.generic.models import BICField
from precise_bbcode.fields import BBCodeTextField


class AdvUser(models.Model):
    is_activated = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Spare(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name}'


class Machine(models.Model):
    name = models.CharField(max_length=30)
    spares = models.ManyToManyField(Spare, through='Kit',
                                    through_fields=('machine', 'spare'))
    notes = GenericRelation('Note')

    def __str__(self):
        return f'{self.name}'


class Kit(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    spare = models.ForeignKey(Spare, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)


class Note(models.Model):
    content = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field='content_type', fk_field='object_id')


class Message(models.Model):
    content = models.TextField()


class PrivateMessage(Message):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.OneToOneField(Message, on_delete=models.CASCADE, parent_link=True)


# class Message(models.Model):
#     content = models.TextField()
#     name = models.CharField(max_length=20)
#     email = models.EmailField()
#
#     class Meta:
#         abstract = True
#         ordering = ['name']
#
#
# class PrivateMessage(Message):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=40)
#     email = None
#
#     class Meta(Message.Meta):
#         pass

# class PGSRoomReserving(models.Model):
#     name = models.CharField(max_length=20, verbose_name='Помещение')
#     reserving = DateTimeRangeField(verbose_name='Время резервирования')
#     cancelled = models.BooleanField(default=False, verbose_name='Отменить резервирование')
#
#     class Meta:
#         indexes = [
#             GistIndex(fields=['reserving'],
#                       name='i_pgsrr_reserving',
#                       opclasses=('range_ops',),
#                       fillfactor=50)
#         ]


# class PGSRubric(models.Model):
#     name = models.CharField(max_length=20, verbose_name='Имя')
#     description = models.TextField(verbose_name='Описание')
#     tags = ArrayField(base_field=models.CharField(max_length=20), verbose_name='Теги')
#
#     class Meta:
#         indexes = [
#             models.Index(fields=('name', 'description'),
#                          name='i_pgsrubric_name_description',
#                          opclasses=('varchar_pattern_ops', 'bpchar_pattern_ops'))
#         ]


# class PGSProject(models.Model):
#     name = models.CharField(max_length=40, verbose_name='Название')
#     platforms = ArrayField(base_field=ArrayField(
#         base_field=models.CharField(max_length=20)),
#         verbose_name='Используемые платформы')


# class PGSProject2(models.Model):
#     name = models.CharField(max_length=40, verbose_name='Название')
#     platforms = HStoreField(verbose_name='Используемые платформы')


# class PGSProject3(models.Model):
#     name = CICharField(max_length=40, verbose_name='Название')
#     data = JSONField()


def get_timestamp_path(instance, filename):
    # return '%s%s' % (datetime.now().timestamp(), splitext(filename)[1])
    return f'{datetime.now().timestamp()}{splitext(filename)[1]}'


class Img(models.Model):
    # archive = models.FileField(upload_to='archives/')
    # archive = models.FileField(upload_to='archives/%Y/%m/%d/')
    # file = models.FileField(upload_to=get_timestamp_path)

    img = models.ImageField(
        verbose_name='Изображение',
        upload_to=get_timestamp_path,
    )
    desc = models.TextField(verbose_name='Описание')

    def delete(self, *args, **kwargs):
        self.img.delete(save=False)
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


# class Comment(models.Model):
#
#     class Meta:
#         permissions = (
#             ('hide_comment', 'Можно скрывать комментарии')
#         )
#         default_permissions = ('change', 'delete')


class Document(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to=get_timestamp_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название категории')
    description = models.TextField(blank=True, null=True, verbose_name='Описание категории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя автора')
    bic = BICField(verbose_name='Банковский идентификационный код')

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    image = models.ImageField(upload_to='article_images/', blank=True, null=True, verbose_name='Изображение')
    active = models.BooleanField(default=False, verbose_name='Активная')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('article_detail', args=[str(self.id)])


class BBCodeText(models.Model):
    bbcode_content = BBCodeTextField(null=True, blank=True, verbose_name='Описание')

    def __str__(self):
        return f'BBCodeText #{self.pk}'


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    teacher = models.CharField(max_length=100, null=True, blank=True)
    duration_weeks = models.PositiveIntegerField(default=4)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    @classmethod
    def get_active_courses(cls):
        return cls.objects.filter(is_active=True)

    @classmethod
    def get_course_by_name(cls, name):
        try:
            return cls.objects.get(name=name)
        except cls.DoesNotExist:
            return None


class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    courses = models.ManyToManyField(Course, related_name='students')

    def __str__(self):
        return self.name

    @classmethod
    def get_students_by_course(cls, course_name):
        return cls.objects.filter(courses__name=course_name)

    @classmethod
    def get_student_by_email(cls, email):
        try:
            return cls.objects.get(email=email)
        except cls.DoesNotExist:
            return None


class StudentCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateField()
    completion_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.name} - {self.course.name}"


class StudentCourseListView(BaseDateListView):
    model = StudentCourse
    date_field = 'enrollment_date'
    allow_future = True
    template_name = 'index.html'


class SMSMessage(models.Model):
    sender = models.CharField(max_length=100)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} - {self.timestamp}"