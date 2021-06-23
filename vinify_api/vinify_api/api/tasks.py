
import requests
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
from .models import website as SiteInfo
from .models import  wine as Products

def tasks():
	objs=SiteInfo.objects.filter(proceaded=False)
	for obj in objs:
		get_all_urls(obj.url+"/sitemap.xml",obj)



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

def covert_data():
	with open("Imported table-Grid view.json","r") as file:
		import json
		file_js=json.loads(file.read())
		for elem in file_js:
			wb=website.objects.filter(url__icontains=elem["url_1"].split(".")[1])
			wb= None if not wb else wb

			instance=wine(wine_title=elem["name"],wine_url=elem["url_1"],website=wb,wine_acidity=elem["Acidity"],wine_boldness=elem["Intensity"],wine_data=elem)
			instance.change_round()
			instance.save()


covert_data()
