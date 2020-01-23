from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache
from django.core.mail import EmailMessage
from django_short_url.models import ShortURL
from rest_framework.exceptions import ValidationError
from smtplib import SMTPAuthenticationError
from django.core.mail import EmailMultiAlternatives
from project.settings import EMAIL_HOST
from jwt import ExpiredSignatureError
from django_short_url.views import get_surl
from django_short_url.models import ShortURL
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.clickjacking import xframe_options_deny
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.core.validators import validate_email
from django.contrib import messages
from django.conf import settings
import django
from django.template.loader import render_to_string, get_template
from rest_framework.views import APIView
from django.shortcuts import render, redirect
from .models import Registration
import jwt
from rest_framework.authentication import authenticate
from rest_framework.response import Response
from django.contrib.auth import login, logout
from django.db.models import Q
# from django.contrib.auth.models import User
from rest_framework.generics import api_settings
from rest_framework.generics import GenericAPIView
from .serializers import (
    RegistrationSerializers,
    LoginSerializers,
    EmailSerializers,
    ResetSerializers
)
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth import authenticate, get_user_model
from django_short_url.views import get_surl
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from .token import token_activation
import json
# Create your views here.
from .utils import jwt_response_payload_handler
from rest_framework_jwt.settings import api_settings
User = get_user_model
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

#social_auth
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView

#github code uses
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_auth.registration.views import SocialLoginView


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
from django.views.generic import TemplateView


User = get_user_model()

# class GithubLogin(SocialLoginView):
#     adapter_class = GitHubOAuth2Adapter
#     callback_url = CALLBACK_URL_YOU_SET_ON_GITHUB
#     client_class = OAuth2Client
class Home(TemplateView):
    template_name = 'index.html'


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    
class Login(GenericAPIView):
    serializer_class = LoginSerializers
    # def get(self,request):
    #     return render(request,'email_validation.html')
    
    def post(self, request):
        permission_classes = [permissions.AllowAny]
        if request.user.is_authenticated:
            return Response({'details': 'user is already authenticated'})
        data = request.data
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        qs = User.objects.filter(
            Q(username__iexact=username) or
            Q(email__iexact=email)
        ).distinct()
        if qs.count() == 1:
            user_obj = qs.first()
            if user_obj.check_password(password):
                user = user_obj
                login(request, user)
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                response = jwt_response_payload_handler(token, user)
                cache.set(user.username, token)
                # print(cache.get(user.username))
                return Response({'details': 'user succesfully loggedin,thakyou'})
            return Response("check password again")
        return Response("multipale users are present with this username")


class Registration(GenericAPIView):
    serializer_class = RegistrationSerializers

    def post(self, request):
        if request.user.is_authenticated:
            return Response("your are already registred,please do login")
        data = request.data
        username = data.get('username')
        email = data.get('email')
        password1 = data.get('password1')
        password2 = data.get('password2')
        if len(password1) < 4 or len(password2) <4:
            return Response("length of the password must be greater than 4") 
        elif password1 != password2:
            return Response("passwords are not matching")
        qs_name = User.objects.filter(
            Q(username__iexact=username)
        )
        qs_email = User.objects.filter(
            Q(email__iexact=email)
        )
        if qs_name.exists():
            return Response("already user id present with this username ")
        elif qs_email.exists():
            return Response("already user id present with this  email")
        else:
            user = User.objects.create(username=username, email=email)
            user.set_password(password1)
            user.is_active = False
            user.save()
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            response = jwt_response_payload_handler(token, user)

            # user is unique then we will send token to his/her email for validation
            # token = token_activation(user.username, user.password)
            url = str(token)
            surl = get_surl(url)
            z = surl.split("/")
            mail_subject = "Activate your account by clicking below link"
            mail_message = render_to_string('email_validation.html', {
                'user': user.username,
                'domain': get_current_site(request).domain,
                'surl': z[2]
            })
            recipient_email = user.email
            subject, from_email, to = 'greeting from fundoo,Activate your account by clicking below link', EMAIL_HOST, recipient_email
            msg = EmailMultiAlternatives(subject, mail_message, from_email, [to])
            msg.attach_alternative(mail_message, "text/html")
            msg.send()
            # template_html = "email_validation.html"
            # print(mail_message)
            
            # email = EmailMessage(
            #     mail_subject, mail_message, to=[recipient_email])
            # email.send()
            return Response({"response": response,
                             "details": "verify through your email"})


def activate(request, surl):
    """
    :param request: request is made by the used
    :param token:  token is fetched from url
    :return: will register the account
    """
    try:
        tokenobject = ShortURL.objects.get(surl=surl)
        token = tokenobject.lurl
        decode = jwt.decode(token, settings.SECRET_KEY)
        username = decode['username']
        user = User.objects.get(username=username)
        # if user is not none then user account willed be activated
        if user is not None:
            user.is_active = True
            user.save()
            return redirect('login')
        else:
            return HttpResponse('not valid user')
    except KeyError as e:
        return HttpResponse(e)
    except Exception as f:
        return HttpResponse(f)


                # email_context = Context({ 'contact': contact, 'amount': amount})

                # subject, from_email, to = 'Deposit Successfully created.', settings.EMAIL_HOST_USER, contact_email
                # text_content = "Thank you for depositing the amount of " + str(amount) + "."

                # html = loader.get_template(template_html)
                # html_content = html.render(email_context)
                # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                # msg.attach_alternative(html_content, "text/html")
                # msg.send()
                
class Logout(GenericAPIView):
    serializer_class = LoginSerializers

    def get(self, request):
        try:
            user = request.user
            logout(request)
            cache.delete(user.username)
            return Response({'details': 'your succefully loggeg out,thankyou'})
        except Exception:
            return Response({'details': 'something went wrong while logout'})


class Forgotpassword(GenericAPIView):

    serializer_class = EmailSerializers

    def post(self, request):
        # data = request.data
        email = request.data['email']
        if email == "":
            return Response({'details': 'email should not be empty'})
        else:
            try:
                validate_email(email)
            except Exception:
                return Response({'details': 'not a valid email'})
            try:
                user = User.objects.filter(email=email)
                user_email = user.values()[0]['email']
                user_username = user.values()[0]['username']
                user_id = user.values()[0]['id']
                # print(user_email, user_id, user_username)
                if user_email is not None:
                    token = token_activation(user_username, user_id)
                    url = str(token)
                    surl = get_surl(url)
                    z = surl.split('/')
                    mail_subject = "Activate your account by clicking below link"
                    mail_message = render_to_string('email_validate.html', {
                        'user': user_username,
                        'domain': get_current_site(request).domain,
                        'surl': z[2]
                    })
                    # print(mail_message)
                    recipient_email = user_email
                    subject, from_email, to = 'greeting from fundoo,Activate your account by clicking below link', EMAIL_HOST, recipient_email
                    msg = EmailMultiAlternatives(subject, mail_message, from_email, [to])
                    msg.attach_alternative(mail_message, "text/html")
                    msg.send()
                    # email = EmailMessage(
                    #     mail_subject, mail_message, to=[recipient_email])
                    # email.send()
                    return Response({'details': 'please check your email,link has sent your email'})
            except:
                return Response({'details': 'something went wrong'})


def reset_password(request, surl):
    try:
        # here decode is done with jwt

        tokenobject = ShortURL.objects.get(surl=surl)
        token = tokenobject.lurl
        decode = jwt.decode(token, settings.SECRET_KEY)
        username = decode['username']
        user = User.objects.get(username=username)

        # if user is not none then we will fetch the data and redirect to the reset password page
        if user is not None:
            context = {'userReset': user.username}
            print(context)
            return redirect('/resetpassword/' + str(user)+'/')
        else:
            messages.info(request, 'was not able to sent the email')
            return redirect('forgotpassword')
    except KeyError:
        messages.info(request, 'was not able to sent the email')
        return redirect('forgotpassword')
    except Exception as e:
        print(e)
        messages.info(request, 'activation link expired')
        return redirect('forgotpassword')


class ResetPassword(GenericAPIView):
    serializer_class = ResetSerializers

    def post(self, request, user_reset):
        password1 = request.data['password']

        if user_reset is None:
            return Response({'details': 'not a valid user'})
        elif (password1 or password2) == "":
            return Response({'details': 'password should not be empty'})
        # elif (password1 != password2):
        #     return Response({'details': 'password are should match'})
        else:
            try:
                user = User.objects.get(username=user_reset)
                user.set_password(password1)
                user.save()
                return Response({'details': 'your password has been Set'})
            except Exception:
                return Response({'details': 'not a valid user'})


def session(request):
    """
    if user seeion is closed
    redirect user to session page
    """
    return render(request, 'session.html')
