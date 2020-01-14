from django.core import cache
from django.conf import settings
import json
from django.http import HttpResponse


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
