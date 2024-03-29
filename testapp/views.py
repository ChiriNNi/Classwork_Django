import json
import os
from datetime import datetime

from django.contrib.auth.models import User
from django.core.mail import EmailMessage, get_connection, EmailMultiAlternatives, send_mail, send_mass_mail, \
    mail_admins
from django.core.paginator import Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import StreamingHttpResponse, FileResponse, JsonResponse
from django.template.loader import render_to_string
from django.urls import resolve
from django.views.decorators.gzip import gzip_page
from django.views.decorators.http import require_http_methods, require_GET, require_POST, require_safe

from bboard.models import Rubric, Bb
from samplesite.settings import BASE_DIR
from testapp.forms import ImgForm, DocumentForm, BBCodeForm, CourseForm, StudentForm, ImageUploadForm
from testapp.models import Img, BBCodeText, Course, Student
from PIL import Image
from django.core.files.storage import FileSystemStorage
from django.conf import settings

FILES_ROOT = os.path.join(BASE_DIR, 'files')


# def index(request):
#     resp_content = ('Здесь будет', ' главная', ' страница', ' сайта')
#     resp = StreamingHttpResponse(resp_content, content_type='text/plain; charset=utf-8')
#     return resp

# def index(request):
#     # file_name = r'static/bg.jpg'
#     file_name = r'static/lesson_15.zip'
#     return FileResponse(open(file_name, 'rb'),
#                         as_attachment=True,
#                         filename='file.zip')

# def index(request):
#     data = {'title': 'Мотоцикл', 'content': 'Старый', 'price': 10000.0}
#     return JsonResponse(data, encoder=DjangoJSONEncoder)

# def index(request):
#     context = {'title': 'Тестовая страница'}
#     return render(request, 'test.html', context)

# def index(request):
#     r = get_object_or_404(Rubric, name="Транспорт")
#     return redirect('bboard:by_rubric', rubric_id=r.id)

# @require_http_methods(['GET', 'POST'])
# @require_GET()
# @require_POST()
# @require_safe()  # GET, HEAD
# @gzip_page()
# def index(request):
#     rubric = get_object_or_404(Rubric, name="Транспорт")
#     bbs = get_list_or_404(Bb, rubric=rubric)
#
#     res = resolve('/2/')
#
#     context = {'title': 'Тестовая страница', 'bbs': bbs, 'res': res}
#
#     return render(request, 'test.html', context)


def index(request):
    imgs = []

    for entry in os.scandir(FILES_ROOT):
        imgs.append(os.path.basename(entry))

    context = {'title': 'Тестовая страница', 'imgs': imgs}

    return render(request, 'testapp/index.html', context)


def get(request, filename):
    fn = os.path.join(FILES_ROOT, filename)
    return FileResponse(open(fn, 'rb'),
                        content_type='application/octet-stream')


def add(request):
    if request.method == 'POST':
        form = ImgForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['img']
            # fn = '%s%s' % (datetime.now().timestamp(),
            #                os.path.splitext(uploaded_file.name)[1])
            fn = f'{datetime.now().timestamp()}{os.path.splitext(uploaded_file.name)[1]}'
            fn = os.path.join(FILES_ROOT, fn)

            with open(fn, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            return redirect('test:add')
    else:
        form = ImgForm()
    context = {'form': form}
    return render(request, 'testapp/add.html', context)


def delete(request, pk):
    img = Img.objects.get(pk=pk)
    img.img.delete()
    img.delete()
    return redirect('test:add')


def add_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            documents_path = os.path.join(FILES_ROOT, 'documents')
            if not os.path.exists(documents_path):
                os.makedirs(documents_path)

            fn = f'{datetime.now().timestamp()}{os.path.splitext(uploaded_file.name)[1]}'
            fn = os.path.join(documents_path, fn)

            with open(fn, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            return redirect('test:add_document')
    else:
        form = DocumentForm()
    context = {'form': form}
    return render(request, 'testapp/add_document.html', context)


# def hide_comment(request):
#     if request.user.has_perm('testapp.hide_comments'):
#         pass


def test_email(request):
    # em = EmailMessage(subject='Test', body='Test', to=['user@supersite.kz'])

    # em = EmailMessage(subject='Ваш новый пароль',
    #                   body='Ваш новый пароль находится во вложении',
    #                   attachments=[('password.txt', '123456789', 'text/plain')],
    #                   to=['user@supersite.kz'])

    # em = EmailMessage(subject='Запрошенный вами файл',
    #                   body='Получите файл',
    #                   to=['user@supersite.kz'])
    # em.attach_file(os.path.join(BASE_DIR, 'tmp', 'file.txt'))

    # context = {'user': 'Вася Пупкин'}
    # s = render_to_string('email/letter.txt', context)
    # em = EmailMessage(subject='Опопвещение', body=s, to=['vpupkin@supersite.kz'])
    #
    # em.send()

    # con = get_connection()
    # con.open()
    # em_1 = EmailMessage(subject='Test1', body='Test1',
    #                     to=['user1@supersite.kz'], connection=con)
    # em_1.send()
    # em_2 = EmailMessage(subject='Test2', body='Test2',
    #                     to=['user2@supersite.kz'], connection=con)
    # em_2.send()
    # em_3 = EmailMessage(subject='Test3', body='Test3',
    #                     to=['user3@supersite.kz'], connection=con)
    # em_3.send()
    # con.close()

    # con = get_connection()
    # con.open()
    # em_1 = EmailMessage(subject='Test1', body='Test1',
    #                     to=['user1@supersite.kz'])
    # em_2 = EmailMessage(subject='Test2', body='Test2',
    #                     to=['user2@supersite.kz'])
    # em_3 = EmailMessage(subject='Test3', body='Test3',
    #                     to=['user3@supersite.kz'])
    # con.send_messages([em_1, em_2, em_3])
    # con.close()

    # em = EmailMultiAlternatives(subject='Test', body='Test',
    #                             to=['user@supersite.kz'])
    # em.attach_alternative('<h1>Test</h1>', 'text/html')
    # em.send()

    # send_mail('Test', 'Test!!!', 'webmaster@supersite.kz',
    #           ['user@othersite.kz'], html_message='<h1>Test!!!</h1>')

    # msg1 = ('Подписка', 'Подтвердите подписку', 'webmaster@supersite.kz',
    #         ['user1@othersite.kz', 'user2@othersite.kz'])
    # msg2 = ('Подписка', 'Подписка подтверждена', 'webmaster@supersite.kz',
    #         ['user3@othersite.kz'])
    # send_mass_mail((msg1, msg2))

    # user = User.objects.get(username='admin')
    # user.email_user('Подъём!', 'Admin, не спи!', fail_silently=True)

    mail_admins('Подъём!', 'Admin-ы, не спите!',
                html_message='<strong>Админы, не спите!!!</strong>')

    return redirect('test:index')


def create_bbcode_text(request):
    if request.method == 'POST':
        form = BBCodeForm(request.POST)
        if form.is_valid():
            bbcode_text = form.save()
            return redirect('test:view_bbcode_text', pk=bbcode_text.pk)
    else:
        form = BBCodeForm()
    return render(request, 'testapp/create_bbcode_text.html', {'form': form})


def view_bbcode_text(request, pk):
    bbcode_text = BBCodeText.objects.get(pk=pk)
    return render(request, 'testapp/view_bbcode_text.html', {'bbcode_text': bbcode_text})


def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('test:course_list')
    else:
        form = CourseForm()
    return render(request, 'testapp/add_course.html', {'form': form})


def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('test:student_list')
    else:
        form = StudentForm()
    return render(request, 'testapp/add_student.html', {'form': form})


def course_list(request):
    courses = Course.objects.all()
    return render(request, 'testapp/course_list.html', {'courses': courses})


def student_list(request):
    students = Student.objects.all()
    return render(request, 'testapp/student_list.html', {'students': students})



thumbnails_urls = []


def upload_and_create_thumbnail(request):
    paginator = Paginator(thumbnails_urls, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = request.FILES['image']
            thumbnail_size = form.cleaned_data['thumbnail_size']

            image = Image.open(uploaded_image)

            thumbnail_size = (thumbnail_size, thumbnail_size)
            image.thumbnail(thumbnail_size)

            thumbnails_dir = os.path.join(settings.MEDIA_ROOT, 'thumbnails')
            if not os.path.exists(thumbnails_dir):
                os.makedirs(thumbnails_dir)

            thumbnail_path = os.path.join(thumbnails_dir, uploaded_image.name)

            image.save(thumbnail_path)

            thumbnail_url = os.path.join(settings.MEDIA_URL, 'thumbnails', uploaded_image.name)

            thumbnails_urls.append(thumbnail_url)

            return render(request, 'testapp/index.html',
                          {'thumbnails_urls': thumbnails_urls, 'form': form, 'page_obj': page_obj})
    else:
        form = ImageUploadForm()

    return render(request, 'testapp/upload.html', {'form': form})

