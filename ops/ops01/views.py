from django.contrib.auth.models import User, Group
from rest_framework import viewsets,serializers
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib import auth
import time,json,datetime
from ops01.models import *
from runScripts import runCmd
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


def groupDetail(request,group_id):
	group_obj = Group.objects.get(id = group_id);
	ip_list = IP.objects.filter(group__name = group_obj.name)
	return render_to_response('groupDetail.html',{'group_obj':group_obj,'ip_list':ip_list})


def host_list(request):
	group_id = request.GET.get('group_id')
	ip_list = IP.objects.filter(group__id = group_id)
	ip_dic = {}
	for host in ip_list:
		ip_dic[host.id] = [host.display_name,host.ip]
	return HttpResponse(json.dumps(ip_dic))


def host_detail(request,host_id):
	hostObj = IP.objects.get(id = host_id)
	return render_to_response('host_detail.html',{'hostObj':hostObj})

def getGraph(request):
	print '--------------------',request.GET.get('host_id')
	g_data = {
		'load_1': [2,3,4,6,34,5,6],
		'load_5': [6,3,5,6,4,9,7],
		'load_15': [7,5,4,9,14,5,8],
		'time': ['10:10','10:11','10:12','10:13','10:14','10:15','10:16']

	}
	return HttpResponse(json.dumps(g_data))


def hostManager(request):
	group_dic = {}
	for g in Group.objects.all():
		host_list = IP.objects.filter(group__id = g.id)
		group_dic[g.name] = []
		for h in host_list:
			group_dic[g.name].append(h.display_name)
	return render_to_response('host_manage.html',{'user':request.user,'group_dic':group_dic})

def runCMD(request):
	print '-------------',request.GET.getlist('host_name')
	hostList = request.GET.getlist('host_name')
	latest_track_mark = OpsLog.objects.order_by('-track_mark')[0] 
	track_mark = latest_track_mark.track_mark + 1
	runHost = {}
	for host in hostList:
		getHostInfo = IP.objects.get(display_name = host)
		runHost[host] = getHostInfo.ip 
	executeInstance = runCmd.execute()
	username = "root"
        password = "www.eegoo"
	command = request.GET.get('cmd')
	executeInstance.run(command,runHost,username,password,track_mark)

	successNum = len(OpsLogTemp.objects.filter(track_mark=track_mark))
	OpsLog.objects.create(
	#	finish_date = datetime.datetime.now(),
		log_type='cmd',   
		tri_user='root',
		run_user='root',
		cmd=command,
		total_task = len(hostList),
		success_num = successNum,
		failed_num = 0,
		track_mark = track_mark)
	while True:
		successNum = len(OpsLogTemp.objects.filter(track_mark=track_mark))
		print 'num----------------',successNum
		print 'hostlist----------------',len(hostList)
		if successNum == len(hostList):
			 modify_success = OpsLog.objects.get(track_mark=track_mark)
			 modify_success.success_num = successNum
			 modify_success.save()
			 break
		time.sleep(10)
	return HttpResponse(json.dumps({'track_mark':track_mark}))


def getCmdResult(request):
	track_id = request.GET.get('track_mark')
	#print "----------",type(track_id)
	result_dic ={ 'result_detail':[] }
	result_summary = OpsLog.objects.get(track_mark = track_id)
	success_num = result_summary.success_num
	failed_num = result_summary.failed_num
	total_num = result_summary.total_task
	result_dic['result_summary'] = [total_num,success_num,failed_num]
	#get detail result
	for h in OpsLogTemp.objects.filter(track_mark = track_id):
		result_dic['result_detail'].append([h.ip,h.event_log,h.result])

	return HttpResponse(json.dumps(result_dic))




def test(request):
	print request.POST
	return HttpResponse('from 172.16.20.210')



