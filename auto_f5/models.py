# encoding: utf-8
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
################
##健康检查表
################
class Monitor_Association(models.Model):
	monitor_association_name =  models.CharField(max_length=200,unique=True)
	class Meta:
		verbose_name = '健康检查表'
		verbose_name_plural = "健康检查表"
	def __unicode__(self):
		return self.monitor_association_name

###########
##VirtualServer表
###########
class VirtualServer(models.Model):
    vs_ip = models.CharField(max_length=200)
    vs_name = models.CharField(max_length=100)
    vs_port = models.IntegerField(u'端口')
    
    class Meta:
        unique_together = ("vs_ip", "vs_port")
        verbose_name = '虚拟IP表'
        verbose_name_plural = "虚拟IP表"
    def __unicode__(self):
        return "%s:%s" % (self.vs_ip,self.vs_port) 
########################
##节点表
########################
class Node(models.Model):
    node_ip = models.CharField(max_length=200)
    port = models.IntegerField(u'端口')
    status_choices = (('SESSION_STATUS_ENABLED','enabled'),
                ('SESSION_STATUS_FORCED_DISABLED', 'disabled'),)
    status = models.CharField(u'节点状态',choices=status_choices,max_length=100, default='SESSION_STATUS_FORCED_DISABLED')
    class Meta:
        unique_together = ("node_ip", "port")
        verbose_name = '节点表'
        verbose_name_plural = "节点表"
    def __unicode__(self):
        return "%s:%s" % (self.node_ip,self.port)
################
##池表
################
class Pool(models.Model):
    pool_name =  models.CharField(max_length=200,unique=True)
    monitor_association =  models.ForeignKey(Monitor_Association,blank=True,null=True)
    vip = models.OneToOneField(VirtualServer,blank=True)
    node = models.ManyToManyField(Node,verbose_name=u'节点',blank=True)
    class Meta:
        verbose_name = '池表'
        verbose_name_plural = "池表"
    def __unicode__(self):
        return self.pool_name


