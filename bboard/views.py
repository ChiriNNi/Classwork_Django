from django.core.paginator import Paginator
from django.db.models import Count
from django.forms import modelformset_factory
from django.forms.formsets import ORDERING_FIELD_NAME
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template, render_to_string
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView, ArchiveIndexView, MonthArchiveView, RedirectView
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView

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


# class IndexView(TemplateView):
#     template_name = 'index.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['bbs'] = Bb.objects.all()
#         context['rubrics'] = Rubric.objects.annotate(count=Count('bb')).filter(count__gt=0)
#         return context


# def by_rubric(request, rubric_id):
#     bbs = Bb.objects.filter(rubric=rubric_id)
#     rubrics = Rubric.objects.annotate(count=Count('bb')).filter(count__gt=0)
#     current_rubric = Rubric.objects.get(pk=rubric_id)
#     context = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric': current_rubric}
#     return render(request, 'by_rubric.html', context)


# class BbByRubricView(TemplateView):
#     template_name = "by_rubric.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['bbs'] = Bb.objects.filter(rubric=context['rubric_id'])
#         context['rubrics'] = Rubric.objects.all()
#         context['current_rubric'] = Rubric.objects.get(pk=context['rubric_id'])
#         return context


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


# def add_and_save(request):
#     print(request.headers['Accept-Encoding'])
#     print(request.headers['accept-encoding'])
#     print(request.headers['Accept_Encoding'])
#
#     if request.method == 'POST':
#         bbf = BbForm(request.POST)
#         if bbf.is_valid():
#             bbf.save()
#             return HttpResponseRedirect(reverse('bboard:by_rubric'),
#                                         kwargs={'rubric_id': bbf.clean_data['rubric'].pk})
#         else:
#             context = {'form': bbf}
#             return render(request, 'create.html', context)
#     else:
#         bbf = BbForm()
#         context = {'form': bbf}
#         return render(request, 'create.html', context)


# class BbIndexView(ArchiveIndexView):
#     model = Bb
#     template_name = 'index.html'
#     date_field = 'published'
#     date_list_period = 'year'
#     context_object_name = 'bbs'
#     allow_empty = True
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['rubrics'] = Rubric.objects.annotate(count=Count('bb')).filter(count__gt=0)
#         return context


def index(request):
    bbs = Bb.objects.all()
    rubrics = Rubric.objects.annotate(count=Count('bb')).filter(count__gt=0)

    paginator = Paginator(bbs, 2)

    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1

    page = paginator.get_page(page_num)

    context = {'bbs': page.object_list, 'rubrics': rubrics, 'page_obj': page}

    return render(request, 'index.html', context)

    # template = get_template('index.html')
    # return HttpResponse(template.render(context=context, request=request))


def select_columns(request):
    bbs = Bb.objects.values('title', 'price')
    context = {'bbs': bbs}
    return render(request, 'select_columns.html', context)


def exclude_values(request):
    bbs = Bb.objects.exclude(price__gt=100500)
    context = {'bbs': bbs}
    return render(request, 'exclude_values.html', context)

# class BbIndexView(ListView):
#     model = Bb
#     template_name = 'index.html'
#     context_object_name = 'bbs'
#     paginate_by = 2
#
#     def get_queryset(self):
#         return Bb.objects.all()
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['rubrics'] = Rubric.objects.annotate(count=Count('bb')).filter(count__gt=0)
#         return context


class BbMonthView(MonthArchiveView):
    model = Bb
    template_name = 'index.html'
    date_field = 'published'
    date_list_period = 'month'
    month_format = '%m'
    context_object_name = 'bbs'
    allow_empty = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.annotate(count=Count('bb')).filter(count__gt=0)
        return context


class BbByRubricView(ListView):
    template_name = 'by_rubric.html'
    context_object_name = 'bbs'

    def get_queryset(self):
        return Bb.objects.filter(rubric=self.kwargs['rubric_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['current_rubric'] = Rubric.objects.get(pk=self.kwargs['rubric_id'])
        return context


def rubrics(request):
    RubricFormSet = modelformset_factory(Rubric, fields=('name', ), can_order=True, can_delete=True)

    if request.method == 'POST':
        formset = RubricFormSet(request.POST)

        if formset.is_valid():
            instances = formset.save(commit=False)
            for obj in formset:
                if obj.cleaned_data:
                    rubric = obj.save(commit=False)
                    rubric.order = obj.cleaned_data[ORDERING_FIELD_NAME]
                    rubric.save()

            for obj in formset.deleted_objects:
                obj.delete()

            return redirect('bboard:rubrics')

    else:
        formset = RubricFormSet()

    context = {'formset': RubricFormSet}

    return render(request, 'bboard/rubrics.html', context)



class BbDetailView(DetailView):
    model = Bb

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubric'] = Rubric.objects.all()
        return context


# class BbCreateView(CreateView):
#     template_name = 'create.html'
#     form_class = BbForm
#     success_url = reverse_lazy('bboard:index')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['rubrics'] = Rubric.objects.all()
#         return context

class BbCreateView(CreateView):
    template_name = 'create.html'
    form_class = BbForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class BbEditView(UpdateView):
    model = Bb
    form_class = BbForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class BbDeleteView(DeleteView):
    model = Bb
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


# class BbAddView(FormView):
#     template_name = 'create.html'
#     form_class = BbForm
#     initial = {'price': 0.0}
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['rubrics'] = Rubric.objects.all()
#         return context
#
#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)
#
#     def get_form(self, form_class=None):
#         self.object = super().get_form(form_class)
#         return self.object
#
#     def get_success_url(self):
#         return reverse('bboard:by_rubric', kwargs={'rubric:id': self.object.cleaned_data['rubric'].pk})

class AllUsersView(ListView):
    model = User
    template_name = 'all_users.html'
    context_object_name = 'users'


class UserProfileView(DetailView):
    model = User
    template_name = 'user_profile.html'
    context_object_name = 'user'