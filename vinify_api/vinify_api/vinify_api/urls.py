from django.contrib import admin
from django.urls import include, path
from . import views
import api

from .views import LoginAPIView, save_analytics, get_redwine_data, get_whitewine_data, update_customer_data, \
    get_bothwine_data, update_wines_table, store_user_info, get_user_details

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/accounts/', include('api.urls')),
    path('api/accounts/', include('authemail.urls')),

    path('landing/', views.LandingFrontEnd.as_view(), name='landing_page'),

    path('signup/', views.SignupFrontEnd.as_view(), name='signup_page'),
    path('signup/email_sent/', views.SignupEmailSentFrontEnd.as_view(),
         name='signup_email_sent_page'),
    path('signup/verify/', views.SignupVerifyFrontEnd.as_view()),
    path('signup/verified/', views.SignupVerifiedFrontEnd.as_view(),
         name='signup_verified_page'),
    path('signup/not_verified/', views.SignupNotVerifiedFrontEnd.as_view(),
         name='signup_not_verified_page'),

    path('login/', views.LoginFrontEnd.as_view(), name='login_page'),
    path('home/', views.HomeFrontEnd.as_view(), name='home_page'),
    path('recommendation/', api.views.Get_recomendations.as_view(), name='home_page'),

    path('logout/', views.LogoutFrontEnd.as_view(), name='logout_page'),

    path('password/reset/', views.PasswordResetFrontEnd.as_view(),
         name='password_reset_page'),
    path('password/reset/email_sent/',
         views.PasswordResetEmailSentFrontEnd.as_view(),
         name='password_reset_email_sent_page'),
    path('password/reset/verify/', views.PasswordResetVerifyFrontEnd.as_view()),
    path('password/reset/verified/',
         views.PasswordResetVerifiedFrontEnd.as_view(),
         name='password_reset_verified_page'),
    path('password/reset/not_verified/',
         views.PasswordResetNotVerifiedFrontEnd.as_view(),
         name='password_reset_not_verified_page'),
    path('password/reset/success/', views.PasswordResetSuccessFrontEnd.as_view(),
         name='password_reset_success_page'),

    path('email/change/', views.EmailChangeFrontEnd.as_view(),
         name='email_change_page'),
    path('email/change/emails_sent/',
         views.EmailChangeEmailsSentFrontEnd.as_view(),
         name='email_change_emails_sent_page'),
    path('email/change/verify/', views.EmailChangeVerifyFrontEnd.as_view()),
    path('email/change/verified/',
         views.EmailChangeVerifiedFrontEnd.as_view(),
         name='email_change_verified_page'),
    path('email/change/not_verified/',
         views.EmailChangeNotVerifiedFrontEnd.as_view(),
         name='email_change_not_verified_page'),

    path('password/change/', views.PasswordChangeFrontEnd.as_view(),
         name='password_change_page'),
    path('password/change/success/', views.PasswordChangeSuccessFrontEnd.as_view(),
         name='password_change_success_page'),

    path('users/me/change/', views.UsersMeChangeFrontEnd.as_view(),
         name='users_me_change_page'),
        path('demodata', views.index,
         name='demodata'),
    path('location', views.index1,
         name='location'),
    path('wine_data', views.index_wine,
         name='wine_data'),
    path('registration', views.register,
         name='registration'),
    path('users/me/change/success/', views.UsersMeChangeSuccessFrontEnd.as_view(),
         name='users_me_change_success_page'),
    path('api/login/',LoginAPIView.as_view(),name='login_api'),
    path('save_analytics/',save_analytics,name='save_analytics'),
    path('get_redwine_data/',get_redwine_data,name='get_redwine_data'),
    path('get_whitewine_data/',get_whitewine_data,name='get_whitewine_data'),
    path('get_bothwine_data/',get_bothwine_data,name='get_bothwine_data'),
    path('update_customer_data/',update_customer_data,name='get_whitewine_data'),
    path('update_wines_table/',update_wines_table,name='update_wines_table'),
    path('store_user_info/',store_user_info,name='store_user_info'),
    path('get_user_details/',get_user_details,name='get_user_details'),

]
