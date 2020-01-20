from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.core import cache
from django.conf import settings
import json
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
import functools


def super_user_only(function):
    """
    :param function: function is called
    :return: will check token expiration
    """

    def wrapper(request, *args, **kwargs):
        """
        :return: will check token expiration
        """
        response = {"success": False,
                    "message": "please login again", 'data': []}
        try:
            if request.META["HTTP_AUTHORIZATION"]:
                try:
                    header = request.META["HTTP_AUTHORIZATION"]
                    token = header.split(" ")
                    decode = jwt.decode(token[1], settings.SECRET_KEY)
                    user = User.objects.get(id=decode['user_id'])
                    if not user.is_superuser:
                        response['message'] = "something went wrong please login back"
                        # return HttpResponse(json.dumps(response, indent=2), status=404)
                        raise PermissionDenied
                    return function(request, *args, **kwargs)
                except jwt.exceptions.DecodeError as e:
                    response["message"] = str(e)
                    return HttpResponse(json.dumps(response, indent=2), status=404)
                except jwt.exceptions.ExpiredSignatureError as e:
                    response['message'] = str(e)
                    return HttpResponse(json.dumps(response, indent=2), status=404)
                except User.DoesNotExist as e:
                    response["message"] = str(e)
                    return HttpResponse(json.dumps(response, indent=2), status=404)
        except KeyError:
            pass

        if request.COOKIES.get(settings.SESSION_COOKIE_NAME) is None:
            response = {
                "success": False, "message":  "something went wrong please login again", 'data': []}
            return HttpResponse(json.dumps(response, indent=2), status=404)
        else:
            return function(request, *args, **kwargs)

    return wrapper


def login_decorator(function):
    """
    :param function: function is called
    :return: will check token expiration
    """

    def wrapper(request, *args, **kwargs):
        """
        :return: will check token expiration
        """
        response = {"success": False,
                    "message": "please login again", 'data': []}
        try:
            if request.META["HTTP_AUTHORIZATION"]:
                try:
                    header = request.META["HTTP_AUTHORIZATION"]
                    token = header.split(" ")
                    decode = jwt.decode(token[1], settings.SECRET_KEY)
                    user = User.objects.get(id=decode['user_id'])
                    if cache.get(user.username) is None:
                        logger.error(
                            "user credential were not found in redis ")
                        response['message'] = "something went wrong please login back"
                        return HttpResponse(json.dumps(response, indent=2), status=404)
                    return function(request, *args, **kwargs)
                except jwt.exceptions.DecodeError as e:
                    response["message"] = str(e)
                    return HttpResponse(json.dumps(response, indent=2), status=404)
                except jwt.exceptions.ExpiredSignatureError as e:
                    response['message'] = str(e)
                    return HttpResponse(json.dumps(response, indent=2), status=404)
                except User.DoesNotExist as e:
                    response["message"] = str(e)
                    return HttpResponse(json.dumps(response, indent=2), status=404)
        except KeyError:
            pass

        if request.COOKIES.get(settings.SESSION_COOKIE_NAME) is None:
            response = {
                "success": False, "message":  "something went wrong please login again", 'data': []}
            return HttpResponse(json.dumps(response, indent=2), status=404)
        else:
            return function(request, *args, **kwargs)

    return wrapper


def anonymous_required(function=None, redirect_url=None):

    if not redirect_url:
        redirect_url = settings.LOGIN_REDIRECT_URL

    actual_decorator = user_passes_test(
        lambda u: u.is_anonymous(),
        login_url=redirect_url
    )

    if function:
        return actual_decorator(function)
    return actual_decorator


def superuser_only(function):
    """Limit view to superusers only."""

    def _inner(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return function(request, *args, **kwargs)
    return _inner


def ajax_required(f):
    """
    AJAX request required decorator
    use it in your views:

    @ajax_required
    def my_view(request):
        ....

    """

    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print('%r (%r, %r) %2.2f sec' % (method.__name__, args, kw, te - ts))
        return result

    return timed


def user_can_write_a_review(func):
    """View decorator that checks a user is allowed to write a review, in negative case the decorator return Forbidden"""

    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.points < 10:
            # logger.warning(
            #     'The {} user has tried to write a review, but does not have enough points to do so'.format(request.user.pk))
            return HttpResponseForbidden()

        return func(request, *args, **kwargs)

    return wrapper
