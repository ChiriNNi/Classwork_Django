import json

from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import StreamingHttpResponse, FileResponse, JsonResponse
from django.urls import resolve

from bboard.models import Rubric, Bb
from testapp.forms import ImgForm
from testapp.models import Img


# def index(request):
#     resp_content = ('Здесь будет', ' главная', ' страница', ' сайта')
#     resp = StreamingHttpResponse(resp_content, content_type='text/plain; charset=utf-8')
#     return resp

# def index(request):
#     file_name = r'static/bg.jpg'
#     return FileResponse(open(file_name, 'rb'), as_attachment=True, filename='photo.jpg')


# def index(request):
#     data = {'title': 'Мотоцикл', 'content': 'Старый', 'price': 10000.0}
#     return JsonResponse(data, encoder=DjangoJSONEncoder)

# def index(request):
#     r = get_object_or_404(Rubric, name='Транспорт')
#     return redirect('bboard:by_rubric', rubric_id=r.id)


def index(request):
    r = get_object_or_404(Rubric, name='Транспорт')
    bbs = get_list_or_404(Bb, rubric=r)
    context = {'bbs': bbs}
    res = resolve('/test/')
    return render(request, 'test.html', context)


def add(request):
    if request.method == 'POST':
        form = ImgForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
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