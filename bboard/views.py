from django.db.models import Count
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template, render_to_string
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView

from .forms import BbForm
from .models import Bb, Rubric
from django.template import loader


# def index(request):
#     bbs = Bb.objects.order_by('-published')
#     # rubrics = Rubric.objects.filter(bb__in=bbs).distinct()
#     rubrics = Rubric.objects.annotate(count=Count('bb')).filter(count__gt=0)
#     context = {'bbs': bbs, 'rubrics': rubrics}
#     return render(request, 'index.html', context)


# def index(request):
#     response = HttpResponse('Здесь будет', content_type='text/plain; charset=utf-8')
#     response.write(' главная')
#     response.writelines((' страница', ' сайта'))
#     return response


def index(request):
    bbs = Bb.objects.all()
    rubrics = Rubric.objects.annotate(count=Count('bb')).filter(count__gt=0)
    context = {'bbs': bbs, 'rubrics': rubrics}

    return HttpResponse(render_to_string('index.html', context, request))

    # template = get_template('index.html')
    # return HttpResponse(template.render(context=context, request=request))


def by_rubric(request, rubric_id):
    bbs = Bb.objects.filter(rubric=rubric_id)
    rubrics = Rubric.objects.annotate(count=Count('bb')).filter(count__gt=0)
    current_rubric = Rubric.objects.get(pk=rubric_id)
    context = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric': current_rubric}
    return render(request, 'by_rubric.html', context)


# def add(request):
#     bbf = BbForm()
#     context = {'form': bbf}
#     return render(request, 'create.html', context)
#
#
# def add_save(request):
#     bbf = BbForm(request.POST)
#
#     if bbf.is_valid():
#         bbf.save()
#         return HttpResponseRedirect(reverse('bboard:by_rubric'),
#                                     kwargs={'rubric_id': bbf.clean_data['rubric'].pk})
#     else:
#         context = {'form': bbf}
#         return render(request, 'create.html', context)


def add_and_save(request):
    print(request.headers['Accept-Encoding'])
    print(request.headers['accept-encoding'])
    print(request.headers['Accept_Encoding'])

    if request.method == 'POST':
        bbf = BbForm(request.POST)
        if bbf.is_valid():
            bbf.save()
            return HttpResponseRedirect(reverse('bboard:by_rubric'),
                                        kwargs={'rubric_id': bbf.clean_data['rubric'].pk})
        else:
            context = {'form': bbf}
            return render(request, 'create.html', context)
    else:
        bbf = BbForm()
        context = {'form': bbf}
        return render(request, 'create.html', context)


class BbCreateView(CreateView):
    template_name = 'create.html'
    form_class = BbForm
    success_url = reverse_lazy('bboard:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context
