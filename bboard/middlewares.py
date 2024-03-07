from django.contrib.auth.models import User
from django.db.models import Count

from bboard.models import Rubric


def my_middleware(_next):
    def core_middleware(request):
        response = _next(request)
        print('Р А Б О Т А Е Т!')
        return response
    return core_middleware


class MyMiddleware:
    def __init__(self, get_response):
        self._next = get_response

    def __call__(self, request):
        response = self._next(request)
        return response


class RubricMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        return self._get_response(request)

    def process_template_response(self, request, response):
        # response.context_data['rubrics'] = Rubric.objects.all()
        response.context_data['rubrics'] = Rubric.objects.annotate(count=Count('bb')).filter(count__gt=0)
        return response


class UserMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        return self._get_response(request)

    def process_template_response(self, request, response):
        if request.user.is_authenticated:
            users_with_groups = []
            for user in User.objects.all():
                user_with_groups = {
                    'user': user,
                    'groups': user.groups.all()
                }
                users_with_groups.append(user_with_groups)
            response.context_data['users_with_groups'] = users_with_groups
        return response


def rubrics(request):
    return {'rubrics': Rubric.objects.annotate(count=Count('bb')).filter(count__gt=0)}

