from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib import auth
import time,json
from ops01.models import *
# Create your views here.


#global msg_dic





def login(request):
	return render_to_response('login.html')


@login_required
def index(request):
	return render_to_response('index.html',{'user':request.user})

#@login_required
def login_auth(request):
        username,password = request.POST['username'],request.POST['password']
        user = auth.authenticate(username = username,password = password)
        if user is not None:  #authentications is correct
                auth.login(request,user)
		return HttpResponseRedirect('/')
        else:
                return render_to_response("login.html",{'login_err':"Wrong username or password!"})

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect("/login/")

def getGroupSummary(request):
	group_dic = {'groupSummary':{},
		'serviceSummary':{}
	}
	for group in Group.objects.all():
		ip_list = IP.objects.filter(group__name = group.name)
		group_dic['groupSummary'][group.id] = [group.name,len(ip_list)]	

	return HttpResponse(json.dumps(group_dic))
