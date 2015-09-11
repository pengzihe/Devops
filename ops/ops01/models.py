
from django.db import models
from django import forms
from datetime import datetime

#from django.contrib.auth.models import (User, BaseUserManager, AbstractBaseUser)
from django.contrib.auth.models import User
# Create your models here.


class Idc(models.Model):
    name=models.CharField(max_length=50,unique=True)
    def __unicode__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=50,unique=True)
    display_name = models.CharField(max_length=50)
    template_list = models.ManyToManyField('templates')
    def __unicode__(self):
        return self.display_name

class IP(models.Model):
    hostname=models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=50, unique = True)
    ip = models.IPAddressField(unique=True)
    belongs_to = models.ForeignKey('trunk_servers', null=True,blank=True)
    idc = models.ForeignKey(Idc, null=True, blank=True)
    group = models.ManyToManyField(Group, null=True, blank=True)
    template_list = models.ManyToManyField('templates',null=True,blank=True)
    custom_services = models.ManyToManyField('services',null=True,blank=True)
    port = models.IntegerField(default='22')
    os = models.CharField(max_length=20, default='linux', verbose_name='Operating System')

    """"#snmp related
    status_monitor_on = models.BooleanField(default=True)
    snmp_on = models.BooleanField(default=True)
    snmp_version = models.CharField(max_length=10,default='2c')
    snmp_community_name = models.CharField(max_length=50,default='public')
    snmp_security_level = models.CharField(max_length=50,default='auth')
    snmp_auth_protocol = models.CharField(max_length=50,default='MD5')
    snmp_user = models.CharField(max_length=50,default='triaquae_snmp')
    snmp_pass = models.CharField(max_length=50,default='my_pass')"""

    def __unicode__(self):
        return self.display_name

class RemoteUser(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __unicode__(self):
        return self.name

class TriaquaeUser(models.Model):
    user = models.ForeignKey(User, null=True)
    email = models.EmailField()
    remoteuser = models.ManyToManyField(RemoteUser, null=True, blank=True)
    group = models.ManyToManyField(Group, null=True, blank=True)
    ip = models.ManyToManyField(IP, null=True, blank=True)
    def __unicode__(self):
        return '%s' % self.user

class AuthByIpAndRemoteUser(models.Model):
    password = models.CharField(max_length=1024,verbose_name="Password or SSH_KEY")
    AUTH_CHOICES = (('ssh-password', 'ssh-password'),('ssh-key', 'ssh-key'))
    authtype = models.CharField(max_length=100, choices=AUTH_CHOICES)
    ip = models.ForeignKey(IP, null=True, blank=True)
    remoteUser = models.ForeignKey(RemoteUser, null=True, blank=True)
    def __unicode__(self):
        return '%s\t%s' % (self.ip, self.remoteUser)






class trunk_servers(models.Model):
    name = models.CharField(max_length=50,unique=True)
    description = models.CharField(max_length=150,blank=True)
    ip_address = models.IPAddressField()
    port = models.IntegerField(default = 9998)
    def __unicode__(self):
        return self.name

class templates(models.Model):  #monitor template
    name = models.CharField(max_length=50, unique=True)
    service_list =  models.ManyToManyField('services')
    graph_list = models.ManyToManyField('graphs',blank=True,null=True)
    #groups = models.ManyToManyField('Group',blank=True,null=True)
    
    def __unicode__(self):
        return self.name

class services(models.Model):  #services list
    name = models.CharField(max_length=50,unique=True)
    monitor_type_list = (('agent','TriAgent'),('snmp','SNMP'),('wget','Wget'))
    monitor_type = models.CharField(max_length=50, choices=monitor_type_list)
    plugin = models.CharField(max_length=100) 
    item_list = models.ManyToManyField('items')
    #trigger_list = models.ManyToManyField('triggers',blank=True)
    trigger = models.ForeignKey('triggers', null=True,blank=True)
    check_interval = models.IntegerField(default=300)
    #flexible_intervals = 
    def __unicode__(self):
        return self.name

class items(models.Model): # monitor item
    name = models.CharField(max_length=50, unique=True)
    key = models.CharField(max_length=100,unique=True)
    data_type_option = (('float','Float'),('string','String'),('integer', 'Integer') ) 
    data_type = models.CharField(max_length=50, choices=data_type_option)
    unit = models.CharField(max_length=30,default='%')
    enabled = models.BooleanField(default=True)
    def __unicode__(self):
        return self.name

class triggers(models.Model): 
    name = models.CharField(max_length=50,unique=True)
    expression = models.TextField()
    #expression = models.CharField(max_length=1000)
    description = models.CharField(max_length=100)
    '''
    serverity_list = (('information','Information'),
                       ( 'warning' ,'Warning'),
                       ('critical', 'Critical'),
                       ('urgent','Urgent'),
                       ('disaster','Disaster') )
    serverity = models.CharField(max_length=30, choices=serverity_list)
    '''
    #dependencies 
    def __unicode__(self):
        return self.name

class graphs(models.Model):
    name = models.CharField(max_length=50, unique=True)
    datasets = models.ManyToManyField('items')
    graph_type = models.CharField(max_length=50)
    def __unicode__(self):
        return self.name
    
class actions(models.Model):
    name = models.CharField(max_length=100,unique=True)
    condition_list = models.ManyToManyField('conditions')
    operation_list = models.ManyToManyField('operations')
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=250)
    recovery_notice = models.BooleanField(default=True)
    recovery_subject = models.CharField(max_length=100)
    recovery_message = models.CharField(max_length=250)
    enabled = models.BooleanField(default=True)
    def __unicode__(self):
        return self.name

class conditions(models.Model):
    name = models.CharField(max_length=100,unique=True)
    condition_type = models.CharField(max_length=100)
    operator = models.CharField(max_length=30)
    value = models.CharField(max_length=250)
    def __unicode__(self):
        return self.name

class operations(models.Model):
    send_to_users = models.ManyToManyField('TriaquaeUser')
    send_to_groups = models.ManyToManyField('Group')
    notifier_type = (('email','Email'),('sms','SMS'))
    send_via = models.CharField(max_length=30,choices=notifier_type)
    notice_times = models.IntegerField(default=5)
    notice_interval = models.IntegerField(default=300, verbose_name='notice_interval(sec)')

