from django.urls import path
from django.conf.urls import include


from .import views

#from .views import obtain_auth_token,CustomObtainAuthToken
urlpatterns = [
    #path('api-token-auth1/', obtain_auth_token),
    #path('api-token-auth/', CustomObtainAuthToken.as_view()),

    


    #path('google/', views.GoogleLogin.as_view(), name='google_login'),

]
