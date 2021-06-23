import json
import os

from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.views.generic.edit import FormView
from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from authemail import wrapper

from .forms import SignupForm, LoginForm
from .forms import PasswordResetForm, PasswordResetVerifiedForm
from .forms import EmailChangeForm
from .forms import PasswordChangeForm, UsersMeChangeForm

from . import wrapperplus

#
from rest_framework.views import APIView

from api.models import customUser, Analytics, wine, Wines


class LandingFrontEnd(TemplateView):
    template_name = 'landing.html'


class SignupFrontEnd(FormView):
    template_name = 'signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('signup_email_sent_page')

    def form_valid(self, form):
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        account = wrapper.Authemail()
        response = account.signup(first_name=first_name, last_name=last_name,
                                  email=email, password=password)

        # Handle other error responses from API
        if 'detail' in response:
            form.add_error(None, response['detail'])
            return self.form_invalid(form)

        return super(SignupFrontEnd, self).form_valid(form)


class SignupEmailSentFrontEnd(TemplateView):
    template_name = 'signup_email_sent.html'


class SignupVerifyFrontEnd(View):
    def get(self, request, format=None):
        code = request.GET.get('code', '')

        account = wrapper.Authemail()
        response = account.signup_verify(code=code)

        # Handle other error responses from API
        if 'detail' in response:
            return HttpResponseRedirect(reverse('signup_not_verified_page'))

        return HttpResponseRedirect(reverse('signup_verified_page'))


class SignupVerifiedFrontEnd(TemplateView):
    template_name = 'signup_verified.html'


class SignupNotVerifiedFrontEnd(TemplateView):
    template_name = 'signup_not_verified.html'


class LoginFrontEnd(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home_page')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        account = wrapper.Authemail()
        response = account.login(email=email, password=password)

        if 'token' in response:
            self.request.session['auth_token'] = response['token']
        else:
            # Handle other error responses from API
            if 'detail' in response:
                form.add_error(None, response['detail'])
            return self.form_invalid(form)

        return super(LoginFrontEnd, self).form_valid(form)


class HomeFrontEnd(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeFrontEnd, self).get_context_data(**kwargs)

        token = self.request.session['auth_token']

        account = wrapper.Authemail()
        account.users_me(token=token)

        context['first_name'] = account.first_name
        context['last_name'] = account.last_name
        context['email'] = account.email

        return context


class LogoutFrontEnd(View):
    def get(self, request):
        token = self.request.session['auth_token']

        account = wrapper.Authemail()
        account.logout(token=token)

        self.request.session.flush()

        return HttpResponseRedirect(reverse('landing_page'))


class PasswordResetFrontEnd(FormView):
    template_name = 'password_reset.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('password_reset_email_sent_page')

    def form_valid(self, form):
        email = form.cleaned_data['email']

        account = wrapper.Authemail()
        response = account.password_reset(email=email)

        # Handle other error responses from API
        if 'detail' in response:
            form.add_error(None, response['detail'])
            return self.form_invalid(form)

        return super(PasswordResetFrontEnd, self).form_valid(form)


class PasswordResetEmailSentFrontEnd(TemplateView):
    template_name = 'password_reset_email_sent.html'


class PasswordResetVerifyFrontEnd(View):
    def get(self, request, format=None):
        code = request.GET.get('code', '')

        account = wrapper.Authemail()
        response = account.password_reset_verify(code=code)

        # Handle other error responses from API
        if 'detail' in response:
            return HttpResponseRedirect(
                reverse('password_reset_not_verified_page'))

        request.session['password_reset_code'] = code

        return HttpResponseRedirect(reverse('password_reset_verified_page'))


class PasswordResetVerifiedFrontEnd(FormView):
    template_name = 'password_reset_verified.html'
    form_class = PasswordResetVerifiedForm
    success_url = reverse_lazy('password_reset_success_page')

    def form_valid(self, form):
        code = self.request.session['password_reset_code']
        password = form.cleaned_data['password']

        account = wrapper.Authemail()
        response = account.password_reset_verified(code=code, password=password)

        # Handle other error responses from API
        if 'detail' in response:
            form.add_error(None, response['detail'])
            return self.form_invalid(form)

        return super(PasswordResetVerifiedFrontEnd, self).form_valid(form)


class PasswordResetNotVerifiedFrontEnd(TemplateView):
    template_name = 'password_reset_not_verified.html'


class PasswordResetSuccessFrontEnd(TemplateView):
    template_name = 'password_reset_success.html'


class EmailChangeFrontEnd(FormView):
    template_name = 'email_change.html'
    form_class = EmailChangeForm
    success_url = reverse_lazy('email_change_emails_sent_page')

    def form_valid(self, form):
        token = self.request.session['auth_token']
        email = form.cleaned_data['email']

        account = wrapper.Authemail()
        response = account.email_change(token=token, email=email)

        # Handle other error responses from API
        if 'detail' in response:
            form.add_error(None, response['detail'])
            return self.form_invalid(form)

        return super(EmailChangeFrontEnd, self).form_valid(form)


class EmailChangeEmailsSentFrontEnd(TemplateView):
    template_name = 'email_change_emails_sent.html'


class EmailChangeVerifyFrontEnd(View):
    def get(self, request, format=None):
        code = request.GET.get('code', '')

        account = wrapper.Authemail()
        response = account.email_change_verify(code=code)

        # Handle other error responses from API
        if 'detail' in response:
            return HttpResponseRedirect(
                reverse('email_change_not_verified_page'))

        request.session['email_change_code'] = code

        return HttpResponseRedirect(reverse('email_change_verified_page'))


class EmailChangeVerifiedFrontEnd(TemplateView):
    template_name = 'email_change_verified.html'


class EmailChangeNotVerifiedFrontEnd(TemplateView):
    template_name = 'email_change_not_verified.html'


class PasswordChangeFrontEnd(FormView):
    template_name = 'password_change.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_change_success_page')

    def form_valid(self, form):
        token = self.request.session['auth_token']
        password = form.cleaned_data['password']

        account = wrapper.Authemail()
        response = account.password_change(token=token, password=password)

        # Handle other error responses from API
        if 'detail' in response:
            form.add_error(None, response['detail'])
            return self.form_invalid(form)

        return super(PasswordChangeFrontEnd, self).form_valid(form)


class PasswordChangeSuccessFrontEnd(TemplateView):
    template_name = 'password_change_success.html'


class UsersMeChangeFrontEnd(FormView):
    template_name = 'users_me_change.html'
    form_class = UsersMeChangeForm
    success_url = reverse_lazy('users_me_change_success_page')

    def get_context_data(self, **kwargs):
        context = super(UsersMeChangeFrontEnd, self).get_context_data(**kwargs)

        token = self.request.session['auth_token']

        account = wrapper.Authemail()
        account.users_me(token=token)

        context['first_name'] = account.first_name
        context['last_name'] = account.last_name
        context['date_of_birth'] = account.date_of_birth

        return context

    def form_valid(self, form):
        token = self.request.session['auth_token']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        date_of_birth = form.cleaned_data['date_of_birth']

        account = wrapperplus.AuthemailPlus()
        response = account.users_me_change(token=token,
                                           first_name=first_name,
                                           last_name=last_name,
                                           date_of_birth=date_of_birth)

        # Handle other error responses from API
        if 'detail' in response:
            form.add_error(None, response['detail'])
            return self.form_invalid(form)

        return super(UsersMeChangeFrontEnd, self).form_valid(form)


class UsersMeChangeSuccessFrontEnd(TemplateView):
    template_name = 'users_me_change_success.html'


#
# data= {
#
# "botData":  "winerielondon123" ,#list(numpy.random.randint(30)),
# "wineColour": {"white":60,"red":40,"total":100,}  ,
# "customerGender": {"male":35,"female":65}  ,
# "customerAge":  { "1834":10,"3554":60,"55over":30,} ,
# "featuredLocationA":  "98.2" ,
# "featuredLocationB":   "105.2"  ,
# "featuredLocationC":   "108.2"  ,
# "featuredLocationD":   "110.2"  ,
# "wine":"None",
# "customer":   "winerielondon123",
# "username":  "winerielondon123" ,
# "helper":   {"step1":False,"step2":False,"step2":False,},
# "botId":  "123PODMZFLKS" ,            "Company_name":"Company Wine Lux" }
# from django.http import JsonResponse
# def index(request):
#     return JsonResponse(data) #HttpResponse(helloWorld.replace("{IPADDRESS}",request.get_host()))

# list_of_users=[
#
#
#
#
#     { "Name":"Med",
#      "Email":"carl@vinify.ai",
#      "Location":"United Kingdom",
#     "Age":"20",
#       "Type":"Any",
#     "WhiteBody":"Medium+",
#    "Red Body":"Medium+",
#     "Acidity":"Medium-",
#
#     } ,
#
#
#
#     { "Name":"Med",
#      "Email":"carl@vinify.ai",
#      "Location":"United Kingdom",
#     "Age":"20",
#       "Type":"Any",
#     "WhiteBody":"Medium+",
#    "Red Body":"Medium+",
#     "Acidity":"Medium-",
#
#     } ,
#
#
#     { "Name":"Med",
#      "Email":"carl@vinify.ai",
#      "Location":"United Kingdom",
#     "Age":"20",
#       "Type":"Any",
#     "WhiteBody":"Medium+",
#    "Red Body":"Medium+",
#     "Acidity":"Medium-",
#
#     } ,
#
#
#     { "Name":"Med",
#      "Email":"carl@vinify.ai",
#      "Location":"United Kingdom",
#     "Age":"20",
#       "Type":"Any",
#     "WhiteBody":"Medium+",
#    "Red Body":"Medium+",
#     "Acidity":"Medium-",
#
#     } ,
# ]


import numpy
import datetime

conversion_rate = numpy.random.random(size=30).tolist()

# data= {
# "conversionData": [[0.027675591315595383, 0.27181613172204344, 0.018550584363670852, 0.5118209211529186, 0.6031248850891863, 0.9960997565536809, 0.5246370941188205, 0.906974556652218, 0.1633648062339571, 0.3500778348090626, 0.18781220155295275, 0.7229623042003112, 0.7037101446390314, 0.41750130913189465, 0.3009788325555576, 0.6541932618808097, 0.7635404354604238, 0.2616485758403677, 0.1373728569919368, 0.3502307450744643, 0.3121491253956057, 0.5382139070775306, 0.8259986662617058, 0.8756964075573286, 0.8771569819283878, 0.14699751726870747, 0.7776762650707795, 0.46375902173760475, 0.02272670419327405, 0.12856385709132945], 0.46143437609737187],
#  "returnData": [[0.027675591315595383, 0.27181613172204344, 0.018550584363670852, 0.5118209211529186, 0.6031248850891863, 0.9960997565536809, 0.5246370941188205, 0.906974556652218, 0.1633648062339571, 0.3500778348090626, 0.18781220155295275, 0.7229623042003112, 0.7037101446390314, 0.41750130913189465, 0.3009788325555576, 0.6541932618808097, 0.7635404354604238, 0.2616485758403677, 0.1373728569919368, 0.3502307450744643, 0.3121491253956057, 0.5382139070775306, 0.8259986662617058, 0.8756964075573286, 0.8771569819283878, 0.14699751726870747, 0.7776762650707795, 0.46375902173760475, 0.02272670419327405, 0.12856385709132945], 0.46143437609737187],
#  "botData": [[0.027675591315595383, 0.27181613172204344, 0.018550584363670852, 0.5118209211529186, 0.6031248850891863, 0.9960997565536809, 0.5246370941188205, 0.906974556652218, 0.1633648062339571, 0.3500778348090626, 0.18781220155295275, 0.7229623042003112, 0.7037101446390314, 0.41750130913189465, 0.3009788325555576, 0.6541932618808097, 0.7635404354604238, 0.2616485758403677, 0.1373728569919368, 0.3502307450744643, 0.3121491253956057, 0.5382139070775306, 0.8259986662617058, 0.8756964075573286, 0.8771569819283878, 0.14699751726870747, 0.7776762650707795, 0.46375902173760475, 0.02272670419327405, 0.12856385709132945], 0.46143437609737187],
# #'':[list(conversion_rate),sum(list(conversion_rate))/len(conversion_rate) ]   ,# [[0.027675591315595383, 0.27181613172204344, 0.018550584363670852, 0.5118209211529186, 0.6031248850891863, 0.9960997565536809, 0.5246370941188205, 0.906974556652218, 0.1633648062339571, 0.3500778348090626, 0.18781220155295275, 0.7229623042003112, 0.7037101446390314, 0.41750130913189465, 0.3009788325555576, 0.6541932618808097, 0.7635404354604238, 0.2616485758403677, 0.1373728569919368, 0.3502307450744643, 0.3121491253956057, 0.5382139070775306, 0.8259986662617058, 0.8756964075573286, 0.8771569819283878, 0.14699751726870747, 0.7776762650707795, 0.46375902173760475, 0.02272670419327405, 0.12856385709132945], 0.46143437609737187],  "customerAge": {"1834": 10, "3554": 60, "55over": 30},
# "featuredLocationA": {"name": 'location1', "stat": 34, "xAxis": 24 , "yAxis": 80 },
# "featuredLocationB": {"name": 'location2', "stat": 24, "xAxis": 34 , "yAxis": 50 },
# "featuredLocationC": {"name": 'location3', "stat": 33, "xAxis": 64 , "yAxis": 80 },
# "featuredLocationD": {"name": 'location4', "stat": 20, "xAxis": 74 , "yAxis": 80 },
# 'wineColour': {"white":white_avg, "red":red_avg, "total":100, }  ,
# "customerGender": {"male":35,"female":65}  ,
# 'wine': "None",
# "customer":   "winerielondon123",
# "username":  "winerielondon123" ,
# "helper":   {"step1":False,"step2":False,"step3":False,"step":False,},
#     "users_list":({"Name": "Med",
#                'Email': "carl@vinify.ai",
#                "Location": "United Kingdom",
#                "Age": "20",
#                "Type": "Any",
#                "WhiteBody": "Medium+",
#                "Red Body": "Medium+",
#                "Acidity": "Medium-",
#
#                },
#
#               {"Name": "Med",
#                "Email": "carl@vinify.ai",
#                "Location": "United Kingdom",
#                "Age": "20",
#                "Type": "Any",
#                "WhiteBody": "Medium+",
#                "Red Body": "Medium+",
#                "Acidity": "Medium-",
#
#                },
#
#               {"Name": "Med",
#                "Email": "carl@vinify.ai",
#                "Location": "United Kingdom",
#                "Age": "20",
#                "Type": "Any",
#                "WhiteBody": "Medium+",
#                "Red Body": "Medium+",
#                "Acidity": "Medium-",
#
#                },
#
#               {"Name": "Med",
#                "Email": "carl@vinify.ai",
#                "Location": "United Kingdom",
#                "Age": "20",
#                "Type": "Any",
#                "WhiteBody": "Medium+",
#                "Red Body": "Medium+",
#                "Acidity": "Medium-",
#
#                },
#               )
# ,
#       "customerAge": {"low": 10, "mid": 60, "high": 30},
#              "botId":  "123PODMZFLKS" ,
# "Company_name":"Vinify"
# }
from django.http import JsonResponse
# def index(request):
#     return JsonResponse(data) #HttpResponse(helloWorld.replace("{IPADDRESS}",request.get_host()))


# list_of_users=[
#
#
#
#
#     { "Name":"Med",
#      "Email":"carl@vinify.ai",
#      "Location":"United Kingdom",
#     "Age":"20",
#       "Type":"Any",
#     "WhiteBody":"Medium+",
#    "Red Body":"Medium+",
#     "Acidity":"Medium-",
#
#     } ,
#
#
#
#     { "Name":"Med01",
#      "Email":"carl 02@vinify.ai",
#      "Location":"France",
#     "Age":"20",
#       "Type":"Any",
#     "WhiteBody":"Medium+",
#    "Red Body":"Medium-",
#     "Acidity":"low",
#
#     } ,
#
#
#     { "Name":"Me02",
#      "Email":"carl 02@vinify.ai",
#      "Location":"Argent",
#     "Age":"10",
#       "Type":"Any",
#     "WhiteBody":"Medium+",
#    "Red Body":"High",
#     "Acidity":"Medium+",
#
#     } ,
#
#
#     { "Name":"Med 03",
#      "Email":"carl 03@vinify.ai",
#      "Location":"Argentina",
#     "Age":"40",
#       "Type":"Any",
#     "WhiteBody":"Low",
#    "Red Body":"High",
#     "Acidity":"High",
#
#     } ,
# ]


# data["wine_data"]=[
# {"img": "https://assets.website-files.com/6024425fe4650f16992543c8/6036565b9ea0fb50cc553af1_Screenshot%202021-02-24%20at%2013.34.56.png", "Wine_name": "Wine 1", "Country": "France", "Region": "Bordueax", "Grape": "Sauvignon Blanc", "Type": "Red", "Price": "\u20ac12.99"},
# {"img": "https://assets.website-files.com/6024425fe4650f16992543c8/6036565b9ea0fb50cc553af1_Screenshot%202021-02-24%20at%2013.34.56.png", "Wine_name": "Wine 2", "Country": "USA", "Region": "Bordueax", "Grape": "Sauvignon Blanc", "Type": "White", "Price": "\u20ac11.99"},
# {"img": "https://assets.website-files.com/6024425fe4650f16992543c8/6036565b9ea0fb50cc553af1_Screenshot%202021-02-24%20at%2013.34.56.png", "Wine_name": "Wine 3", "Country": "USA", "Region": "Bordueax", "Grape": "Sauvignon Blanc", "Type": "Red", "Price": "\u20ac12.99"},
# {"img": "https://assets.website-files.com/6024425fe4650f16992543c8/6036565b9ea0fb50cc553af1_Screenshot%202021-02-24%20at%2013.34.56.png", "Wine_name": "Wine 4", "Country": "Spain", "Region": "Bordueax", "Grape": "Sauvignon Blanc", "Type": "White", "Price": "\u20ac22.99"},
# {"img": "https://assets.website-files.com/6024425fe4650f16992543c8/6036565b9ea0fb50cc553af1_Screenshot%202021-02-24%20at%2013.34.56.png", "Wine_name": "Wine 5", "Country": "France", "Region": "Bordueax", "Grape": "Sauvignon Blanc", "Type": "Red", "Price": "\u20ac12.99"},
# {"img": "https://assets.website-files.com/6024425fe4650f16992543c8/6036565b9ea0fb50cc553af1_Screenshot%202021-02-24%20at%2013.34.56.png", "Wine_name": "Wine 6", "Country": "France", "Region": "Bordueax", "Grape": "Sauvignon Blanc", "Type": "Red", "Price": "\u20ac12.99"},
# {"img": "https://assets.website-files.com/6024425fe4650f16992543c8/6036565b9ea0fb50cc553af1_Screenshot%202021-02-24%20at%2013.34.56.png", "Wine_name": "Wine 7", "Country": "USA", "Region": "Bordueax", "Grape": "Sauvignon Blanc", "Type": "White", "Price": "\u20ac19.99"},
# {"img": "https://assets.website-files.com/6024425fe4650f16992543c8/6036565b9ea0fb50cc553af1_Screenshot%202021-02-24%20at%2013.34.56.png", "Wine_name": "Wine 8", "Country": "Spain", "Region": "Bordueax", "Grape": "Sauvignon Blanc", "Type": "Red", "Price": "\u20ac16.99"},
# {"img": "https://assets.website-files.com/6024425fe4650f16992543c8/6036565b9ea0fb50cc553af1_Screenshot%202021-02-24%20at%2013.34.56.png", "Wine_name": "Wine 9", "Country": "France", "Region": "Bordueax", "Grape": "Sauvignon Blanc", "Type": "White", "Price": "\u20ac13.99"},
#  {"img": "https://assets.website-files.com/6024425fe4650f16992543c8/6036565b9ea0fb50cc553af1_Screenshot%202021-02-24%20at%2013.34.56.png", "Wine_name": "Wine 9", "Country": "Spain", "Region": "Bordueax", "Grape": "Sauvignon Blanc", "Type": "Red", "Price": "\u20ac12.99"},
#   {"img":"https://assets.website-files.com/6024425fe4650f16992543c8/6036565b9ea0fb50cc553af1_Screenshot%202021-02-24%20at%2013.34.56.png"
#     ,"Wine_name":"Yalumba The Y Series Viognier"
#     ,"Country":"France"
#     ,"Region":"Bordueax"
#     ,"Grape":"Sauvignon Blanc"
#     ,"Type":"Red"
#     ,"Price":"€12.99"},{"img":"https://assets.website-files.com/6024425fe4650f16992543c8/6036565b9ea0fb50cc553af1_Screenshot%202021-02-24%20at%2013.34.56.png"
#     ,"Wine_name":"Yalumba The Y Series Viognier"
#     ,"Country":"France"
#     ,"Region":"Bordueax"
#     ,"Grape":"Sauvignon Blanc"
#     ,"Type":"Red"
#     ,"Price":"€12.99"}
# ,{"img":"https://assets.website-files.com/6024425fe4650f16992543c8/6036565b9ea0fb50cc553af1_Screenshot%202021-02-24%20at%2013.34.56.png"
#     ,"Wine_name":"Yalumba The Y Series Viognier"
#     ,"Country":"France"
#     ,"Region":"Bordueax"
#     ,"Grape":"Sauvignon Blanc"
#     ,"Type":"Red"
#     ,"Price":"€12.99"}]


from django.http import JsonResponse

2
def index(request):
    merchant = None
    try:
        merchant = customUser.objects.get(id=request.GET.get("userid"))

        analytics_filtered = merchant.merchant_name.all()
        print("merchant   ", analytics_filtered)
        total = len(analytics_filtered.filter(preference__in=['Red', 'White']))
        total_analytics = len(analytics_filtered)
        red_wine_count = len(analytics_filtered.filter(preference="Red"))
        white_wine_count = len(analytics_filtered.filter(preference="White"))
        red_avg = (red_wine_count / total) * 100
        white_avg = (white_wine_count / total) * 100
        low_ages = len(analytics_filtered.filter(age__gte=18, age__lte=34))
        mid_ages = len(analytics_filtered.filter(age__gte=35, age__lte=54))
        high_ages = len(analytics_filtered.filter(age__gte=55))
        low_age_per = (low_ages / total_analytics) * 100
        mid_age_per = (mid_ages / total_analytics) * 100
        high_age_per = (high_ages / total_analytics) * 100

        red_avg = "{:.2f}".format(red_avg)
        white_avg = "{:.2f}".format(white_avg)
        # print("!!!!!           ", total, red_wine_count, white_wine_count, red_avg, white_avg)
        list_of_users = []
        for analytic_obj in analytics_filtered:
            white_body_index = str(analytic_obj.white_wine_score)[0]
            acidity_index = str(analytic_obj.white_wine_score)[1]
            red_body_index = str(analytic_obj.red_wine_score)[0]
            type_arr = ['Low', 'Medium - ', 'Medium', 'Medium +', 'High']
            white_body = "-"
            red_body = "-"
            acidity = "-"
            if white_body_index.isdigit():
                # print("....   ",white_body_index)
                white_body = type_arr[int(white_body_index)]
            if acidity_index.isdigit():
                acidity = type_arr[int(acidity_index)]
            if red_body_index.isdigit():
                red_body = type_arr[int(red_body_index)]
            list_of_users.append(
                {"Name": analytic_obj.name if analytic_obj.name else "-",
                 "Email": analytic_obj.email if analytic_obj.email else "-",

                 "Location": analytic_obj.location if analytic_obj.location else "-",
                 "Age": analytic_obj.age if analytic_obj.age else "-",
                 #"Type": analytic_obj.preference if analytic_obj.preference  else "-",
                 #"WhiteBody": white_body,
                 "login_count": analytic_obj.login_count,
                 #"RedBody": red_body,
                 #"Acidity": acidity,

                 }
            )
    except Exception as e:
        print("Error    ", e)
        white_avg = red_avg = low_age_per = mid_age_per = high_age_per = 0
        list_of_users = []

    data = {
        "conversionData": [list(conversion_rate), sum(list(conversion_rate)) / len(conversion_rate)],
        'returnData': [list(conversion_rate), sum(list(conversion_rate)) / len(conversion_rate)],
        "botData": [
            [0.027675591315595383, 0.27181613172204344, 0.018550584363670852, 0.5118209211529186, 0.6031248850891863,
             0.9960997565536809, 0.5246370941188205, 0.906974556652218, 0.1633648062339571, 0.3500778348090626,
             0.18781220155295275, 0.7229623042003112, 0.7037101446390314, 0.41750130913189465, 0.3009788325555576,
             0.6541932618808097, 0.7635404354604238, 0.2616485758403677, 0.1373728569919368, 0.3502307450744643,
             0.3121491253956057, 0.5382139070775306, 0.8259986662617058, 0.8756964075573286, 0.8771569819283878,
             0.14699751726870747, 0.7776762650707795, 0.46375902173760475, 0.02272670419327405, 0.12856385709132945],
            0.46143437609737187],
        "featuredLocationA": {"name": 'location1', "stat": 34, "xAxis": 24, "yAxis": 80},
        "featuredLocationB": {"name": 'location2', "stat": 24, "xAxis": 34, "yAxis": 50},
        "featuredLocationC": {"name": 'location3', "stat": 33, "xAxis": 64, "yAxis": 80},
        "featuredLocationD": {"name": 'location4', "stat": 20, "xAxis": 74, "yAxis": 80},
        'wineColour': {"white": white_avg, "red": red_avg, "total": 100, },
        "customerGender": {"male": 35, "female": 65},
        "customerAge": {"low": low_age_per, "mid": mid_age_per, "high": high_age_per},

        'wine': "None",
        "customer": "sss",
        "username": merchant.first_name if merchant and merchant.first_name and merchant.first_name != "null" else "there",
        "helper": {"step1": False, "step2": False, "step2": False, },
        "users_list": list_of_users,
        "botId": "123PODMZFLKS", "Company_name": "Vinify"

    }

    wine_list = []
    wine_map_list = []
    from api.models import WineRegions
    try:
        for analytic_obj in analytics_filtered:
            for wine in analytic_obj.selected_wines.all():
                # wine = Wines.objects.get(id=wine_id.wine_id)
                try:
                    country = str(wine.region).split("/")[0]
                    region = str(wine.region).split("/")[1]
                except:
                    country = ""
                    region = wine.region
                # print("country     ",country)
                wine_map_list.append(
                    {
                        "img": wine.image,
                        "Wine_name": wine.name,
                        "Country": str(country).replace(" ", ""),
                        "Region": region,
                        "Grape": wine.grapes,
                        "Type": wine.wine_type,
                        "Price": "€" + str(wine.price)}
                )
    except Exception as e:
        print("ERROR in analytics_filtered loop   ", e)
        pass
    data["wine_data_map"] = wine_map_list
    # print(wine_map_list)
    for wine in Wines.objects.all():
        try:
            country = str(wine.region).split("/")[0]
            region = str(wine.region).split("/")[1]
        except:
            country = ""
            region = wine.region
        wine_list.append(
            {
                "img": wine.image,
                "Wine_name": wine.name,
                "Country": str(country).replace(" ", ""),
                "Region": region,
                "Grape": wine.grapes,
                "Type": wine.wine_type,
                "Price": "€" + str(wine.price)}
        )
    data["wine_data"] = wine_list
    # data["wine_data"]=[
    # {"img": "https://assets.website-files.com/6024425fe4650f16992543c8/6036565b9ea0fb50cc553af1_Screenshot%202021-02-24%20at%2013.34.56.png", "Wine_name": "Wine 1", "Country": "France", "Region": "Bordueax", "Grape": "Sauvignon Blanc", "Type": "Red", "Price": "\u20ac12.99"},
    # {"img": "https://assets.website-files.com/6024425fe4650f16992543c8/6036565b9ea0fb50cc553af1_Screenshot%202021-02-24%20at%2013.34.56.png", "Wine_name": "Wine 2", "Country": "USA", "Region": "Bordueax", "Grape": "Sauvignon Blanc", "Type": "White", "Price": "\u20ac11.99"},
    # {"img": "https://assets.website-files.com/6024425fe4650f16992543c8/6036565b9ea0fb50cc553af1_Screenshot%202021-02-24%20at%2013.34.56.png", "Wine_name": "Wine 3", "Country": "USA", "Region": "Bordueax", "Grape": "Sauvignon Blanc", "Type": "Red", "Price": "\u20ac12.99"},
    # {"img": "https://assets.website-files.com/6024425fe4650f16992543c8/6036565b9ea0fb50cc553af1_Screenshot%202021-02-24%20at%2013.34.56.png", "Wine_name": "Wine 4", "Country": "Spain", "Region": "Bordueax", "Grape": "Sauvignon Blanc", "Type": "White", "Price": "\u20ac22.99"},
    # {"img": "https://assets.website-files.com/6024425fe4650f16992543c8/6036565b9ea0fb50cc553af1_Screenshot%202021-02-24%20at%2013.34.56.png", "Wine_name": "Wine 5", "Country": "France", "Region": "Bordueax", "Grape": "Sauvignon Blanc", "Type": "Red", "Price": "\u20ac12.99"},
    # {"img": "https://assets.website-files.com/6024425fe4650f16992543c8/6036565b9ea0fb50cc553af1_Screenshot%202021-02-24%20at%2013.34.56.png", "Wine_name": "Wine 6", "Country": "France", "Region": "Bordueax", "Grape": "Sauvignon Blanc", "Type": "Red", "Price": "\u20ac12.99"},
    # {"img": "https://assets.website-files.com/6024425fe4650f16992543c8/6036565b9ea0fb50cc553af1_Screenshot%202021-02-24%20at%2013.34.56.png", "Wine_name": "Wine 7", "Country": "USA", "Region": "Bordueax", "Grape": "Sauvignon Blanc", "Type": "White", "Price": "\u20ac19.99"},
    # {"img": "https://assets.website-files.com/6024425fe4650f16992543c8/6036565b9ea0fb50cc553af1_Screenshot%202021-02-24%20at%2013.34.56.png", "Wine_name": "Wine 8", "Country": "Spain", "Region": "Bordueax", "Grape": "Sauvignon Blanc", "Type": "Red", "Price": "\u20ac16.99"},
    # {"img": "https://assets.website-files.com/6024425fe4650f16992543c8/6036565b9ea0fb50cc553af1_Screenshot%202021-02-24%20at%2013.34.56.png", "Wine_name": "Wine 9", "Country": "France", "Region": "Bordueax", "Grape": "Sauvignon Blanc", "Type": "White", "Price": "\u20ac13.99"},
    #  {"img": "https://assets.website-files.com/6024425fe4650f16992543c8/6036565b9ea0fb50cc553af1_Screenshot%202021-02-24%20at%2013.34.56.png", "Wine_name": "Wine 9", "Country": "Spain", "Region": "Bordueax", "Grape": "Sauvignon Blanc", "Type": "Red", "Price": "\u20ac12.99"},
    #   {"img":"https://assets.website-files.com/6024425fe4650f16992543c8/6036565b9ea0fb50cc553af1_Screenshot%202021-02-24%20at%2013.34.56.png"
    #     ,"Wine_name":"Yalumba The Y Series Viognier"
    #     ,"Country":"France"
    #     ,"Region":"Bordueax"
    #     ,"Grape":"Sauvignon Blanc"
    #     ,"Type":"Red"
    #     ,"Price":"€12.99"},{"img":"https://assets.website-files.com/6024425fe4650f16992543c8/6036565b9ea0fb50cc553af1_Screenshot%202021-02-24%20at%2013.34.56.png"
    #     ,"Wine_name":"Yalumba The Y Series Viognier"
    #     ,"Country":"France"
    #     ,"Region":"Bordueax"
    #     ,"Grape":"Sauvignon Blanc"
    #     ,"Type":"Red"
    #     ,"Price":"€12.99"}
    # ,{"img":"https://assets.website-files.com/6024425fe4650f16992543c8/6036565b9ea0fb50cc553af1_Screenshot%202021-02-24%20at%2013.34.56.png"
    #     ,"Wine_name":"Yalumba The Y Series Viognier"
    #     ,"Country":"France"
    #     ,"Region":"Bordueax"
    #     ,"Grape":"Sauvignon Blanc"
    #     ,"Type":"Red"
    #     ,"Price":"€12.99"}]
    # print("SESSIONNNn   ", request.session.get('user_id'))

    return JsonResponse(data)  # HttpResponse(helloWorld.replace("{IPADDRESS}",request.get_host()))


data1 = {
    "location": [{"name": "France", "xAxis": "48", "yAxis": "39", "label": "top"}
        , {"name": "Spain", "xAxis": "47", "yAxis": "42", "label": "top"}
        , {"name": "Argentina", "xAxis": "35", "yAxis": "83", "label": "btm"}
        , {"name": "Australia", "xAxis": "74", "yAxis": "72", "label": "btm"}
        , {"name": "Austria", "xAxis": "51", "yAxis": "40", "label": "btm"}
        , {"name": "Canada", "xAxis": "28", "yAxis": "33", "label": "Top"}
        , {"name": "Chile", "xAxis": "33", "yAxis": "79", "label": "btm"}
        , {"name": "Croatia", "xAxis": "51.5", "yAxis": "41", "label": "btm"}
        , {"name": "England", "xAxis": "47", "yAxis": "35", "label": "Top"}
        , {"name": "Italy", "xAxis": "50", "yAxis": "42", "label": "Top"}
        , {"name": "Germany", "xAxis": "50", "yAxis": "37", "label": "Top"},
                 {"name": "France", "stat": 15, "xAxis": 48, "yAxis": 39, "label": "top"},
                 {"name": "Argentina", "stat": 12, "xAxis": 35, "yAxis": 83, "label": "bottom"}],

}

from django.http import JsonResponse


def index1(request):
    return JsonResponse(data1)  # HttpResponse(helloWorld.replace("{IPADDRESS}",request.get_host()))


def index_wine(request):
    return JsonResponse({"wine_data": wine_data})  # HttpResponse(helloWorld.replace("{IPADDRESS}",request.get_host()))


from django.contrib.auth import get_user_model

from rest_framework import status, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'


from authemail import wrapper


@api_view(['POST'])
def register(request):
    VALID_USER_FIELDS = [f.name for f in get_user_model()._meta.fields]
    account = wrapper.Authemail()
    data = request.POST
    data2 = request.data
    DEFAULTS = {
        # you can define any defaults that you would like for the user, here
    }
    serialized = UserSerializer(data=request.data)
    if serialized.is_valid():
        user_data = {field: data for (field, data) in request.data.items() if field in VALID_USER_FIELDS}
        user_data.update(DEFAULTS)
        user = get_user_model().objects.create_user(
            **user_data
        )
        response = None  # account.signup(**user_data)
        if not 'detail' in response:
            # return super(SignupFrontEnd, self).form_valid(form)
            return Response(UserSerializer(instance=response if response else user).data,
                            status=status.HTTP_201_CREATED)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request):
        print(">>>    ", request.data)
        email = request.data.get("Email-Address")
        password = request.data.get("Password")
        # user_obj = customUser.objects.create(username="abhilash",email="abhilash@vinify.com")
        # user_obj.set_password(password)
        # print("====   ",user_obj)
        # usr = customUser.objects.get(email = "abhilash@vinify.com")
        # usr.password = password
        # usr.save()
        # print("usr   ",usr.passwoobjectsrd)
        data = {}
        print(">>>   ", request.session.get("user_id"))
        if customUser.objects.filter(email=email, password=password):
            user_obj = customUser.objects.get(email=email)
            request.session['user_id'] = user_obj.id

            data['user_id'] = user_obj.id
            data['first_name'] = str(user_obj.first_name)
            data['status'] = True
        else:
            data['status'] = False
            data['error'] = "Incorrect email or password"
        # account = wrapper.Authemail()
        # response = account.login(email=email, password=password)
        # print("response  " ,response)
        # if 'token' in response:
        #     self.request.session['auth_token'] = response['token']
        #     data['token'] = response['token']
        #     data['status'] = True
        # else:
        #     # Handle other error responses from API
        #     if 'detail' in response:
        #         data['error'] = response['detail']
        #         data['status'] = False
        #         print("Error   ",response['detail'])
        # return HttpResponse(json.dumps(data), content_type="application/json")
        return HttpResponse(json.dumps(data), content_type="application/json")


@csrf_exempt
@api_view(["POST"])
def save_analytics(request):
    if request.method == "POST":
        print(request.data)
        data = request.data.get("fields")
        id = data.get("id")
        name = data.get("name")
        age = data.get("age")
        dob = data.get("DOB")
        red_wine_score = data.get("red wine score")
        white_wine_score = data.get("white wine score")
        location = data.get("location")
        url_accessed_from = data.get("url accessed from")
        try:
            analytic_obj = Analytics.objects.get(request_IP=request.META.get('REMOTE_ADDR')).update(
                cust_id=id,
                name=name,
                age=age,
                dob=dob,
                red_wine_score=red_wine_score,
                white_wine_score=white_wine_score,
                location=location,
                url_accessed_from=url_accessed_from,
            )
            analytic_obj.login_count += 1
            analytic_obj.save()
        except:
            analytic_obj = Analytics.objects.create(
                cust_id=id,
                login_count=1,
                request_IP=request.META.get('REMOTE_ADDR'),
                name=name,
                age=age,
                dob=dob,
                red_wine_score=red_wine_score,
                white_wine_score=white_wine_score,
                location=location,
                url_accessed_from=url_accessed_from,
            )

        resp = {
            "id": analytic_obj.id,
            "fields": {
                "id": id,
                "name": name,
                "age": age,
                "red wine score": red_wine_score,
                "white wine score": white_wine_score
            },
            "createdTime": str(datetime.datetime.now())
        }
        return HttpResponse(json.dumps(resp), content_type="application/json")


# @csrf_exempt
@api_view(["GET"])
def get_redwine_data(request):
    if request.method == "GET":
        data = request.query_params

        totals = int(data.get("totals"))
        wine_type = data.get("wine_type")
        bot_id = data.get("bot_id")
        merchant = customUser.objects.get(bot_id=bot_id)
        wine_filtered = Wines.objects.filter(merchant=merchant)
        wine_data = wine_filtered.filter(totals=totals, wine_type=wine_type)
        if len(wine_data) >= 6:
            wine_data = wine_data[:6]
        if not wine_data:
            totals1 = totals - 10
            totals2 = totals - 11
            totals3 = totals - 12
            totals4 = totals - 1
            totals5 = totals + 1
            wine_data = wine_filtered.filter(wine_type=wine_type).filter(
                Q(totals=totals1) | Q(totals=totals2) | Q(totals=totals3) | Q(totals=totals4) | Q(totals=totals5))[:6]
        records = []
        for obj in wine_data:
            records.append({
                "id": obj.id,
                "fields": {
                    "url_1": obj.url,
                    "name": obj.name,
                    "image": obj.image,
                    "price": obj.price,
                    "wine_type": obj.wine_type,
                    "grapes": obj.grapes,
                    "region": obj.region,
                    "wine_style": obj.wine_style,
                    "Acidity": obj.acidity,
                    "Intensity": obj.intensity,
                    "Totals": obj.totals
                },
                "createdTime": str(obj.created)
            })
        resp = {
            "records": records
        }
        print("RED  >>>>>>          ", resp)
        return HttpResponse(json.dumps(resp), content_type="application/json")


@api_view(["GET"])
def get_whitewine_data(request):
    if request.method == "GET":
        data_str = request.query_params.get("filterByFormula")
        bot_id = request.query_params.get("bot_id")
        totals = int(data_str.split("{Totals}=")[1].split(",")[0].replace("'", ""))
        wine_type = data_str.split("{wine_type}=")[1].split(")")[0].replace("'", "")
        merchant = customUser.objects.get(bot_id=bot_id)
        wine_filtered = Wines.objects.filter(merchant=merchant)
        wine_data = wine_filtered.filter(totals=totals, wine_type=wine_type)
        if len(wine_data) >= 6:
            wine_data = wine_data[:6]
        if not wine_data:
            totals1 = totals - 10
            totals2 = totals - 11
            totals3 = totals - 12
            totals4 = totals - 1
            totals5 = totals + 1
            wine_data = wine_filtered.filter(wine_type=wine_type).filter(
                Q(totals=totals1) | Q(totals=totals2) | Q(totals=totals3) | Q(totals=totals4) | Q(totals=totals5))[:6]

        records = []
        for obj in wine_data:
            records.append({
                "id": obj.id,
                "fields": {
                    "url_1": obj.url,
                    "name": obj.name,
                    "image": obj.image,
                    "price": obj.price,
                    "wine_type": obj.wine_type,
                    "grapes": obj.grapes,
                    "region": obj.region,
                    "wine_style": obj.wine_style,
                    "Acidity": obj.acidity,
                    "Intensity": obj.intensity,
                    "Totals": obj.totals
                },
                "createdTime": str(obj.created)
            })
        resp = {
            "records": records
        }
        return HttpResponse(json.dumps(resp), content_type="application/json")


@api_view(["GET"])
def get_bothwine_data(request):
    if request.method == "GET":
        data_str = request.query_params.get("filterByFormula")
        bot_id = request.query_params.get("bot_id")
        totals = int(request.query_params.get("filterByFormula"))
        merchant = customUser.objects.get(bot_id=bot_id)
        wine_filtered = Wines.objects.filter(merchant=merchant)
        wine_data = wine_filtered.filter(totals=totals)
        if len(wine_data) >= 6:
            wine_data = wine_data[:6]
        if not wine_data:
            totals1 = totals - 10
            totals2 = totals - 11
            totals3 = totals - 12
            totals4 = totals - 1
            totals5 = totals + 1
            wine_data = wine_filtered.filter(
                Q(totals=totals1) | Q(totals=totals2) | Q(totals=totals3) | Q(totals=totals4) | Q(totals=totals5))[:6]
        print("wineee      ", totals, wine_data)
        records = []
        for obj in wine_data:
            records.append({
                "id": obj.id,
                "fields": {
                    "url_1": obj.url,
                    "name": obj.name,
                    "image": obj.image,
                    "price": obj.price,
                    "wine_type": obj.wine_type,
                    "grapes": obj.grapes,
                    "region": obj.region,
                    "wine_style": obj.wine_style,
                    "Acidity": obj.acidity,
                    "Intensity": obj.intensity,
                    "Totals": obj.totals
                },
                "createdTime": str(obj.created)
            })
        resp = {
            "records": records
        }
        print("resp   ", resp)
        return HttpResponse(json.dumps(resp), content_type="application/json")


@api_view(["PATCH"])
def update_customer_data(request):
    # if request.method == "PATCH":
    data = request.data
    id = data.get("records")[0].get("id")
    print("datadata   ", data)
    preference = data.get("records")[0].get("fields").get("preference")
    email = data.get("records")[0].get("fields").get("email")
    red_body = data.get("records")[0].get("fields").get("red_body")
    white_body = data.get("records")[0].get("fields").get("white_body")
    acidity = data.get("records")[0].get("fields").get("acidity")
    choice = data.get("records")[0].get("fields").get("choiceinfo")
    bot_id = data.get("records")[0].get("fields").get("bot_id", None)
    print("bot_id     ", preference)
    merchant_filtered = None
    merchant = None
    if bot_id:
        merchant = customUser.objects.get(bot_id=bot_id)
    wine_filtered = Wines.objects.filter(merchant=merchant)
    print("><><><><><   ", wine_filtered)
    resp = {}
    if choice:
        if preference == "I'm easy!":
            totals = int(str(acidity) + str(acidity))
            wine_data = wine_filtered.filter(totals=totals)

            if len(wine_data) >= 6:
                wine_data = wine_data[:6]
            if not wine_data:
                totals1 = totals - 10
                totals2 = totals - 11
                totals3 = totals - 12
                totals4 = totals - 1
                totals5 = totals + 1
                wine_data = wine_filtered.filter(
                    Q(totals=totals1) | Q(totals=totals2) | Q(totals=totals3) | Q(totals=totals4) | Q(totals=totals5))[
                            :6]
                print(":::::::::    ", totals, wine_data)
        else:
            if preference == "Red":
                totals = int(str(red_body) + str(acidity))
                wine_type = "Red Wine"
            else:
                totals = int(str(white_body) + str(acidity))
                wine_type = "White Wine"
            wine_data = wine_filtered.filter(totals=int(totals), wine_type=wine_type)
            if len(wine_data) >= 6:
                wine_data = wine_data[:6]
            if not wine_data:
                totals1 = totals - 10
                totals2 = totals - 11
                totals3 = totals - 12
                totals4 = totals - 1
                totals5 = totals + 1
                wine_data = wine_filtered.filter(wine_type=wine_type).filter(
                    Q(totals=totals1) | Q(totals=totals2) | Q(totals=totals3) | Q(totals=totals4) | Q(totals=totals5))[
                            :6]

        wine_id = list(wine_data)[int(choice)].id
        from api.models import WineRegions
        wine_obj = Wines.objects.get(id=wine_id)
    try:
        obj = Analytics.objects.get(id=id)
        obj.preference = preference
        obj.email = email
        # if bot_id:

        if choice:
            if merchant:
                obj.merchant = merchant
            obj.selected_wines.add(wine_obj)
        obj.save()
        resp = {
            "records": [
                {
                    "id": id,
                    "fields": {
                        "id": obj.cust_id,
                        "name": obj.name,
                        "DOB": obj.dob,
                        "age": obj.age,
                        "preference": obj.preference,
                        "email": obj.email,
                        "red wine score": obj.red_wine_score,
                        "white wine score": obj.white_wine_score,
                        "location": obj.location,
                        "url accessed from": obj.url_accessed_from
                    },
                    "createdTime": obj.created_time
                }
            ]
        }
    except:
        resp = {
            'error': "data does not exists"
        }

    return HttpResponse(json.dumps(resp), content_type="application/json")


@api_view(["GET"])
def update_wines_table(request):
    # csv_path = "wine_table_data_set.csv"
    # print(os.path.exists(csv_path))
    # import csv
    # Wines.objects.all().delete()
    # with open(csv_path) as csv_file:
    #     csv_reader = csv.reader(csv_file, delimiter=',')
    #     line_count = 0
    #     for row in csv_reader:
    #         if line_count == 0:
    #             print(f'Column names are {", ".join(row)}')
    #             line_count += 1
    #         else:
    #             Wines.objects.create(
    #                 url=row[0],
    #                 name=row[1],
    #                 image=row[2],
    #                 price=row[3],
    #                 wine_type=row[4],
    #                 grapes=row[5],
    #                 region=row[6],
    #                 wine_style=row[7],
    #                 body=row[8],
    #                 acidity=row[9],
    #                 totals=row[10]
    #             )
    #             # print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
    #             line_count += 1
    #     print(f'Processed {line_count} lines.')

    merchant_list = list(customUser.objects.filter(email__startswith="merchant"))
    import random
    if merchant_list:
        for wine in Wines.objects.all():
            wine.merchant = random.choice(merchant_list)
            wine.save()

    return HttpResponse("Completed")


@api_view(["POST"])
def store_user_info(request):
    user = customUser.objects.get(id=request.data["user_id"])
    user.role = request.data["role"]
    user.first_name = request.data["name"]
    user.company_name = request.data["company_name"]
    user.favourite_grape = request.data["favourite_grape"]
    user.save()
    return HttpResponse("Completed")


@api_view(["GET"])
def get_user_details(request):
    user = customUser.objects.get(id=request.GET.get("user_id"))
    response = {"name": user.first_name if user.first_name and user.first_name != "null" else "",
                "company_name": user.company_name}
    return HttpResponse(json.dumps(response), content_type="application/json")
