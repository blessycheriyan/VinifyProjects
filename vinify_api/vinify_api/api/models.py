from django.db import models
#from django.contrib.auth.models import User
# Create your models here.





import requests
import json
from django.db import models
import jsonfield
from django.contrib.auth.models import AbstractUser

from django.conf import settings


# Create your models here.


"""lass User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    location = models.TextField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)



"""
from django.contrib.auth.models import (AbstractBaseUser,PermissionsMixin,BaseUserManager)
from django.utils.translation import ugettext_lazy as _

from authemail.models import EmailAbstractUser, EmailUserManager

class website(models.Model):
    #user        = models.ForeignKey(User, null=True,on_delete=models.SET_NULL)
    url = models.TextField(null=True)
    name= models.TextField(null=True)
    xml_url = models.TextField(max_length=200)
    xpath_title = models.TextField(null=True)
    xpath_description = models.TextField(null=True)
    xpath_image = models.TextField(null=True)# seprated by ;
    xpath_grapes = models.TextField(null=True)# seprated by ;
    xpath_region = models.TextField(null=True)
    other_xpaths = jsonfield.JSONField(default={"name_of_data_of_the_scraping_xpath":"the_xpath_itself"})
    proceaded= models.BooleanField(default=False)
    def __str__(self):
        return self.name #+" region: "+self.region
    def get_other_xpaths(self,product_url=None,request=None):
        from lxml import html
        page=request if request else requests.get(product_url).content
        doc=html.fromstring(page)
        data={}
        for key in self.other_xpaths.keys():
            value=doc.xpath(self.other_xpaths[key])
            data[key]=value if type(value)==str else  " ".join(value)
        return data
    def check_fi_url_in_product_url(self,pro_url):
        if self.url[6:] in pro_url:
            return pro_url
        else:
            return self.url
    def check_if_url_contains_http(self):
        if not "http" in self.url:
            return "https://"+self.url
        return self.url



class UserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, email, username, password):
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, username, password):
        user = self.create_user(
            email=email,
            password=password,        
            username=username,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=email,
            password=password,
            username= username,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

        
from datetime import datetime    
from django.utils import timezone

class customUser(EmailAbstractUser):
    date_of_birth= models.DateTimeField(null=True,blank=True)
    phone = models.TextField(null=True,blank=True)
    email = models.EmailField(default="",unique=True)

    phone = models.TextField(null=True,blank=True)
    country = models.TextField(null=True,blank=True)
    state = models.TextField(null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    zip_code = models.TextField(null=True,blank=True)
    website = models.ForeignKey(website, null=True,on_delete=models.SET_NULL)

    username = models.CharField(max_length=25, unique=True)
    first_name = models.CharField(max_length=40,default='null')
    last_name = models.CharField(max_length=140,default='null')
    date_joined = models.DateTimeField(default=timezone.now(), editable = True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    company_name = models.CharField(max_length=140,null=True,blank=True)
    role = models.CharField(max_length=140,null=True,blank=True)
    favourite_grape = models.CharField(max_length=140,null=True,blank=True)
    is_superuser = models.BooleanField(default=False)
    bot_id = models.CharField(max_length=150,null=True,blank=True)
    REQUIRED_FIELDS = []#['username']
    USERNAME_FIELD= 'email'
    objects = EmailUserManager()


from django.db.models.signals import pre_save
from django.dispatch import receiver
import uuid
@receiver(pre_save, sender=customUser)
def my_callback(sender, instance, *args, **kwargs):
    x = uuid.uuid4()
    instance.username = str(x)[:8]

class VerifiedUserManager(EmailUserManager):
    def get_queryset(self):
        return super(VerifiedUserManager, self).get_queryset().filter(
            is_verified=True)


class VerifiedUser(customUser):
    objects = VerifiedUserManager()
    class Meta:
        proxy = True

User=customUser



class winerie(models.Model):
    name= models.TextField(null=True,blank=True)
    user= models.ForeignKey(User, null=True,on_delete=models.SET_NULL)
    website=models.ForeignKey(website, null=True,on_delete=models.SET_NULL)


class Flavours(models.Model):
    flavour = models.TextField(null=True,blank=True)



class wine(models.Model):
    wine_data = jsonfield.JSONField()
    wine_title= models.TextField(null=True,blank=True)
    wine_url= models.TextField(null=True,blank=True)
    grape= models.TextField(null=True,blank=True)
    region= models.TextField(null=True,blank=True)
    image= models.TextField(null=True,blank=True)
    wine_image= models.TextField(null=True,blank=True)
    wine_acidity=models.FloatField( default=None,blank=True, null=True)
    wine_boldness=models.FloatField( default=None,blank=True, null=True)
    wine_tanic=models.FloatField( default=None,blank=True, null=True)
    wine_suitness=models.FloatField( default=None,blank=True, null=True)
    wine_acidity_rounded=models.FloatField( default=None,blank=True, null=True)
    wine_boldness_rounded=models.FloatField( default=None,blank=True, null=True)
    wine_tanic_rounded=models.FloatField( default=None,blank=True, null=True)
    wine_suitness_rounded=models.FloatField( default=None,blank=True, null=True)
    the_other_data = jsonfield.JSONField()
    user= models.ForeignKey(User, null=True,on_delete=models.SET_NULL)
    winerie= models.ForeignKey(winerie, null=True,on_delete=models.SET_NULL)
    website= models.ForeignKey(website, null=True,on_delete=models.SET_NULL)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    update_defaults = models.BooleanField(default=False)
    recommendations = jsonfield.JSONField() #models.PositiveIntegerField( default=None,blank=True, null=True)
    visitors =models.PositiveIntegerField( default=None,blank=True, null=True)
    visitors_by_age = jsonfield.JSONField(default={ "1834":0,"3554":0,"55over":0,})
    visitors_by_gender = jsonfield.JSONField(default={"male":0,"female":0})
    price = models.TextField(null=True,blank=True)
    wine_type = models.TextField(null=True,blank=True)
    wine_style = models.TextField(null=True,blank=True)
    intensity = models.TextField(null=True,blank=True)
    totals = models.TextField(null=True,blank=True)
    flavours = models.ForeignKey(Flavours,related_name='wine_flavour',on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return self.wine_title # "grape: "+self.grape +" region: "+self.region
    #visitors_by_colours = jsonfield.JSONField(default={"white":0,"red":0,"total":0,})
    def get_acidityandenxtrafromApi(self):
        dict_of_data= {}#SearchApi(key).get(self.wine_title,extraparametres)
        region , grape=dict_of_data["region"],dict_of_data["grape"]
        self.set_wine_data(region,grape)
    def set_wine_data(self,region,grape):
        self.acidiyt=self.get_wine_data(region, grape)["acidity"]
        self.boldness=self.get_wine_data(region, grape)["boldness"]
        self.tanin=self.get_wine_data(region, grape)["tanin"]
    def get_wine_data(self,region,grape):
        results=grape_region.objects.filter(region__icontains=region,grape__icontains=grape)
        data={}
        if results:
            return results.last().model_to_dict()
        else :
            return {}
    def saveA(self, *args, **kwargs):
        querryset=grape_region.objects.all()
        querryset_region=None
        querryset_grape=None
        if self.region :
            querryset_region=None if not querryset.filter(region__icontains=self.region) else querryset.filter(region__icontains=self.region) #.filter(region__icontains=self.region)
        elif self.grape:
            querryset_region=querryset
        #print(self.grape.split("/")[0])
        if self.grape:
            querryset_grape=querryset_region.filter(grape__icontains=self.grape.split("/")[0])
            if len(self.grape.split("/"))>1 and not querryset_region.filter(grape__icontains=self.grape.split("/")[0]) :
                querryset_grape=querryset_region.filter(grape__icontains=self.grape.split("/")[1])
        else:
            super(wine, self).save(*args, **kwargs)
        #querryset_grape=querryset_grape if not querryset_region.filter(grape__icontains=self.grape.split("/")[1] ) else None
        grape_and_region=querryset_region if not querryset_grape else querryset_grape
        if grape_and_region:
            grape_and_region=grape_and_region.last()
            self.wine_acidity=grape_and_region.acidity
            self.wine_boldness=grape_and_region.boldness
            self.wine_tanic=grape_and_region.tanic
            self.change_round()
        super(wine, self).save(*args, **kwargs)
    def change_round(self):
        values=[0.5,1,1.5,2,2.5,3,3.5,4]
        self.wine_acidity_rounded =min(values,key=lambda x:abs(x-self.wine_acidity)) if self.wine_acidity else None
        self.wine_boldness_rounded=min(values,key=lambda x:abs(x-self.wine_boldness)) if self.wine_boldness else None
        self.wine_tanic_rounded=min(values,key=lambda x:abs(x-self.wine_tanic)) if self.wine_tanic else None
        #wine_suitness_rounded=min(values,key=lambda x:abs(x-self.wine_acidity)) if self.wine_acidity else None
        self.save()





##
class grape_region(models.Model):
    region= models.TextField(null=True,blank=True)
    region_location= models.TextField(null=True,blank=True)
    grape= models.TextField(null=True,blank=True)
    acidity=models.FloatField( default=None,blank=True, null=True)
    boldness=models.FloatField( default=None,blank=True, null=True)
    tanic=models.FloatField( default=None,blank=True, null=True)
    suitness=models.FloatField( default=None,blank=True, null=True)
    region_weather=models.FloatField( default=None,blank=True, null=True)
    def __str__(self):
        return "grape: "+self.grape +" region: "+self.region




class user_extra_data(models.Model):
    winerie=models.ForeignKey(winerie, null=True,on_delete=models.SET_NULL)
    user_ip= models.TextField(null=True,blank=True)
    location= jsonfield.JSONField()
    session=jsonfield.JSONField()
    cash=jsonfield.JSONField()
    user= models.ForeignKey(User, null=True,on_delete=models.SET_NULL)




#website data like the data of  google analytics
# updated daily instantly
class website_analytics(models.Model):
    winerie=models.ForeignKey(winerie, null=True,on_delete=models.SET_NULL)
    user= models.ForeignKey(User, null=True,on_delete=models.SET_NULL)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    update_defaults = models.BooleanField(default=False)
    extra_json_data = jsonfield.JSONField()
    recommendations =models.PositiveIntegerField( default=None,blank=True, null=True)
    visitors =models.PositiveIntegerField( default=None,blank=True, null=True)
    visitors_full_data =jsonfield.JSONField()# {"visit_bydata":{"12/12/2021":21,}}#models.PositiveIntegerField( default=None,blank=True, null=True)
    purchases =models.PositiveIntegerField( default=None,blank=True, null=True)
    purchases_full_data =jsonfield.JSONField()## {"purchases_bydata":{"12/12/2021":21,}} =models.PositiveIntegerField( default=None,blank=True, null=True)
    purchases_by_bot =models.PositiveIntegerField( default=None,blank=True, null=True)
    purchases_by_bot_full_data =jsonfield.JSONField()## {"purchases_by_bot_bydata":{"12/12/2021":21,}}  =models.PositiveIntegerField( default=None,blank=True, null=True)
    email_list = jsonfield.JSONField() #models.PositiveIntegerField( default=None,blank=True, null=True)
    helper = jsonfield.JSONField(default={"step1":False,"step2":False,"step2":False,})
    wine_by_age = jsonfield.JSONField(default={ "1834":0,"3554":0,"55over":0,})
    wines_by_gender = jsonfield.JSONField(default={"male":0,"female":0})
    wines_by_colours = jsonfield.JSONField(default={"white":0,"red":0,"total":0,})
    total_of_wines=models.PositiveIntegerField( default=0)
    #wine=models.ForeignKey(wine, null=True,on_delete=models.SET_NULL)
    id_bot= models.PositiveIntegerField( unique=True)
    def get_chart_conversion_rates_by_date(self):
        import numpy as np
        dates=self.visitors_full_data["visit_bydata"].keys()
        visits=self.visitors_full_data["visit_bydata"].values()
        #dates=self.purchases_full_data["purchases_bydata"].keys()
        purchases=[self.purchases_full_data["purchases_bydata"][date] for date in dates]
        conversion_rates=np.true_divide(np.asarray(purchases), visits).tolist()
        return conversion_rates
    def get_chart_conversion_rates_by_bot_by_date(self):
        import numpy as np
        dates=self.visitors_full_data["visit_bydata"].keys()
        purchases_by_bot=self.purchases_by_bot_full_data["purchases_by_bot_bydata"].values()
        #dates=self.purchases_full_data["purchases_bydata"].keys()
        purchases=[self.purchases_full_data["purchases_bydata"][date] for date in dates]
        conversion_rates_by_bot=np.true_divide(np.asarray(purchases_by_bot),np.asarray(purchases)).tolist()
        return  {"dates":dates,"conversion_rates_by_bot":conversion_rates_by_bot}
    def get_email_list(self):
        return self.email_list["email_list"]
    def set_email_list(self,email_list):
        self.email_list={"email_list":email_list}
    def Conversion_Rate(self):
        return 0 if not self.purchases or not self.visitors else self.purchases / self.visitors
    def Conversion_affect_by_bot(self):
        return "%"+str(self.Conversion_Rate()/(self.recommendations/self.purchases_by_bot)) if (self.purchases_by_bot and self.Conversion_Rate()) else  "0%"
    def get_all_data(self):
        import numpy
        import datetime
        conversion_rate=numpy.random.random(size=30),
        { "1834":0,"3554":0,"55over":0,}
        {"male":0,"female":0}
        data= {
        "conversionData": list(self.get_chart_conversion_rates_by_date())  ,
        "returnData": list(self.get_chart_conversion_rates_by_bot_by_date())  ,
        "botData": self.get_botData(),# "winerielondon123" ,
        "wineColour":self.get_wine_by_clours(), #{"white":60,"red":40,"total":100,}  ,
        "customerGender": self.get_customerGender(),#{"male":35,"female":65}  ,
        "customerAge":  self.get_customerAge(),#{ "1834":10,"3554":60,"55over":30,} ,
        "featuredLocationA": self.get_featuredLocation("A"),
        "featuredLocationB":  self.get_featuredLocation("B"),
        "featuredLocationC":   self.get_featuredLocation("C"),
        "featuredLocationD":   self.get_featuredLocation("D"),
        "wine":"None",#toBeChanged
        "customer":   "winerielondon123",
        "username":  "winerielondon123" ,
        "helper": self.get_helper_situation(),#  {"step1":False,"step2":False,"step2":False,},
        "botId": self.get_bot_id(),         "Company_name": self.get_Company_name()     }

# every time user come to the client website we shoul set info and create guest user  to save data


#Guest_User()
class guestUser(models.Model):
    date_of_birth= models.DateTimeField(null=True,blank=True)
    phone = models.TextField(null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    gender= models.TextField(null=True,blank=True)
    ip= models.TextField(null=True,blank=True)
    #passwrod = models.PasswordField()
    phone = models.TextField(null=True,blank=True)
    country = models.TextField(null=True,blank=True)
    state = models.TextField(null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    zip_code = models.TextField(null=True,blank=True)
    username = models.CharField(max_length=40,default='null')
    first_name = models.CharField(max_length=40,default='null')
    last_name = models.CharField(max_length=140,default='null')
    website=models.ForeignKey(website, null=True,on_delete=models.SET_NULL)
    objects = EmailUserManager()










from bs4 import BeautifulSoup

from lxml import etree
from requests_html import HTMLSession
import time
from threading import Thread
from lxml import html
import requests

# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render
SiteInfo=website
Products=wine

def tasks():
    objs=SiteInfo.objects.filter(proceaded=False,name="cheerswinemerchants")
    for obj in objs:
        get_all_urls(obj.url+obj.xml_url,obj)

def tasks():
    objs=SiteInfo.objects.filter(proceaded=False)
    for obj in objs:
        get_all_urls(obj.url+obj.xml_url,obj)

from django.contrib.auth.models import User
from django.db.models.signals import post_save

def save_website(sender, instance, **kwargs):
    objs=[instance]#SiteInfo.objects.filter(proceaded=False)
    for obj in objs:
        get_all_urls(obj.url+obj.xml_url,obj)



post_save.connect(save_website, sender=website)
'''./manage.py shell
from django_q.models import Schedule
Schedule.objects.create(
    func='scraper.tasks.tasks',
    minutes=2,
    repeats=-1
)
'''
def get_all_urls(urls_sitemap_xml,obj):
    with requests.Session() as s:
        soup = BeautifulSoup(s.get(urls_sitemap_xml).text,'lxml')
        list_of_urls=[]
        try:
            for url in soup.select('loc'):
                list_of_urls.append(url.text)
                #print(url.text)
        except:
            print("pass1")
    disc_of_new_url={}
    for url in list_of_urls[:10]:
        disc_of_new_url[url]=[]
        if '.xml' in url:
            try:
                with requests.Session() as s:
                    soup_url=BeautifulSoup(requests.get(url).text,'lxml')
                    #print("am la",soup_url)
                    for loc in soup_url.select('loc'):
                        disc_of_new_url[url].append(loc.text)
            except:
                print("pass2")
        else:
            disc_of_new_url[url].append(url)
    for key in disc_of_new_url.keys():
        print("i am here")
        for link in disc_of_new_url[key]:
            print("am here")
            try:
                with HTMLSession() as ss:
                    r = ss.get(link)
                    r.html.render(sleep=5)
                    #print("kkk",r)
                    doc=html.fromstring(r.content)
                    #time.sleep(6)

                    #print("dom.xpath(obj.xpath_title)[0].text", dom.xpath(obj.xpath_title)[0].text )
                    if doc.xpath(obj.xpath_title):
                        obj_product=Products()
                        obj_product.wine_url=link
                        #print(obj_product.url,"obj_product.product_url")
                        obj_product.wine_title=" ".join(doc.xpath(obj.xpath_title))
                        obj_product.grape=" ".join(doc.xpath(obj.xpath_grapes))
                        obj_product.region=" ".join(doc.xpath(obj.xpath_region))

                        #print(obj_product.product_title,"obj_product.product_title")
                        data=obj.get_other_xpaths(obj_product.wine_url)
                        try:
                            #dom.xpath(obj.xpath_image)[0].text
                            data["product_image_url"]=";".join(doc.xpath(obj.xpath_image))
                            #print(obj_product.product_image_url,"obj_product.product_image_url")
                        except:
                            pass
                        try:
                            #doc.xpath(obj.xpath_description)[0].text
                            #obj_product.product_description=dom.xpath(obj.xpath_description)[0].src
                            data["product_description"] = ";".join(doc.xpath(obj.xpath_description))
                            #print(obj_product.product_description,obj_product.product_description)
                        except:
                            pass
                        obj_product.website=obj
                        obj_product.wine_data=data
                        obj_product.get_other_xpaths(request=r.content)
                        #print(doc.xpath(obj.xpath_grapes),doc.xpath(obj.xpath_region))
                        obj_product.saveA()
                        #doc.xpath()
            except:
                #print(doc.xpath(obj.xpath_grapes),doc.xpath(obj.xpath_region))
                try:
                    obj_product.saveA()
                except:
                    pass
                pass




def get_all_urls(urls_sitemap_xml,obj):
    with requests.Session() as s:
        soup = BeautifulSoup(s.get(urls_sitemap_xml).text,'lxml')
        list_of_urls=[]
        try:
            for url in soup.select('loc'):
                list_of_urls.append(url.text)
                #print(url.text)
        except:
            print("pass1")
    disc_of_new_url={}
    for url in list_of_urls[:10]:
        disc_of_new_url[url]=[]
        if '.xml' in url:
            try:
                with requests.Session() as s:
                    soup_url=BeautifulSoup(requests.get(url).text,'lxml')
                    #print("am la",soup_url)
                    for loc in soup_url.select('loc'):
                        disc_of_new_url[url].append(loc.text)
            except:
                print("pass2")
        else:
            disc_of_new_url[url].append(url)
    for key in disc_of_new_url.keys():
        print("i am here")
        for link in disc_of_new_url[key]:
            print("am here")
            try:
                with HTMLSession() as ss:
                    r = ss.get(link)
                    r.html.render(sleep=5)
                    #print("kkk",r)
                    doc=html.fromstring(r.content)

                    #print("dom.xpath(obj.xpath_title)[0].text", dom.xpath(obj.xpath_title)[0].text )
                    if doc.xpath(obj.xpath_title):
                        obj_product=Products()
                        obj_product.wine_url=link
                        #print(obj_product.url,"obj_product.product_url")
                        obj_product.wine_title=" ".join(doc.xpath(obj.xpath_title))
                        obj_product.grape=" ".join(doc.xpath(obj.xpath_grapes)) if len(" ".join(doc.xpath(obj.xpath_grapes)))>1 else None
                        obj_product.region=" ".join(doc.xpath(obj.xpath_region)) if not len(" ".join(doc.xpath(obj.xpath_grapes)))<2 else None
                        #print(obj_product.product_title,"obj_product.product_title")
                        data=obj.get_other_xpaths(obj_product.wine_url)
                        try:
                            #dom.xpath(obj.xpath_image)[0].text
                            data["product_image_url"]=";".join(doc.xpath(obj.xpath_image))
                            #print(obj_product.product_image_url,"obj_product.product_image_url")
                        except:
                            pass
                        try:
                            #doc.xpath(obj.xpath_description)[0].text
                            #obj_product.product_description=dom.xpath(obj.xpath_description)[0].src
                            data["product_description"] = ";".join(doc.xpath(obj.xpath_description))
                            #print(obj_product.product_description,obj_product.product_description)
                        except:
                            pass
                        obj_product.website=obj
                        obj_product.wine_data=data
                        obj_product.get_other_xpaths(request=r.content)
                        #print(doc.xpath(obj.xpath_grapes),doc.xpath(obj.xpath_region))
                        obj_product.change_round()
                        obj_product.saveA()
                        #doc.xpath()
            except:
                #print(doc.xpath(obj.xpath_grapes),doc.xpath(obj.xpath_region))
                try:
                    obj_product.change_round()
                    obj_product.saveA()
                except:
                    pass
                pass


class WineRegions(models.Model):
    wine_id = models.TextField(null=True,blank=True)

    

class Wines(models.Model):
    name = models.TextField(null=True,blank=True)
    url = models.TextField(null=True,blank=True)
    image = models.TextField(null=True,blank=True)
    price = models.TextField(null=True,blank=True)
    wine_type = models.TextField(null=True,blank=True)
    grapes = models.TextField(null=True,blank=True)
    region = models.TextField(null=True,blank=True)
    wine_style = models.TextField(null=True,blank=True)
    body = models.TextField(null=True,blank=True)
    acidity = models.TextField(null=True,blank=True)
    totals = models.TextField(null=True,blank=True)
    intensity = models.TextField(default=0,null=True,blank=True)
    created = models.DateTimeField(default=datetime.now(),null=True,blank=True)
    merchant = models.ForeignKey(customUser,related_name="merchant_wine_rel",on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return str(self.name)+"  >>>  "+str(self.wine_type)+"  >>>  "+str(self.totals)




class Analytics(models.Model):
    cust_id = models.TextField(null=True,blank=True)
    request_IP = models.CharField(max_length=20,null=True,blank=True)
    name = models.TextField(null=True,blank=True)
    login_count = models.PositiveIntegerField(default=0)
    age = models.TextField(null=True,blank=True)
    red_wine_score = models.TextField(null=True,blank=True)
    white_wine_score = models.TextField(null=True,blank=True)
    url_accessed_from = models.TextField(null=True,blank=True)
    location = models.TextField(null=True,blank=True)
    dob = models.TextField(null=True,blank=True)
    email = models.TextField(null=True,blank=True)
    preference = models.TextField(null=True,blank=True)
    created_time = models.DateTimeField(null=True,blank=True)
    selected_wines = models.ManyToManyField(Wines)
    merchant = models.ForeignKey(customUser,related_name="merchant_name",on_delete=models.SET_NULL,null=True,blank=True)

