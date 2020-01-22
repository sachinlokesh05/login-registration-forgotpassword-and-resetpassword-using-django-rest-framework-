from django.urls import path, include
from rest_framework_jwt import views
from rest_framework_jwt.views import obtain_jwt_token
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('api/auth/', obtain_jwt_token),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('register/', views.Registration.as_view(), name='register'),
    path('activate/<surl>/', views.activate, name="activate"),
    path('forgotpassword/', views.Forgotpassword.as_view(), name="forgotpassword"),
    path('reset_password/<surl>/', views.reset_password, name="reset_password"),
    path('resetpassword/<user_reset>/',
         views.ResetPassword.as_view(), name="resetpassword"),
    path('session/', views.session),

    # path('password-reset/',
    #      auth_views.PasswordResetView.as_view(

    #      ),
    #      name='password_reset'),
    # path('password-reset/done/',
    #      auth_views.PasswordResetDoneView.as_view(

    #      ),
    #      name='password_reset_done'),
    # path('password-reset-confirm/<uidb64>/<token>/',
    #      auth_views.PasswordResetConfirmView.as_view(

    #      ),
    #      name='password_reset_confirm'),
    # path('password-reset-complete/',
    #      auth_views.PasswordResetCompleteView.as_view(

    #      ),
    #      name='password_reset_complete'),
]
