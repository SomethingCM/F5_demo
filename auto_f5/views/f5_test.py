#!/usr/bin/env
#-*- coding:utf-8 -*-

# import f5
import bigsuds
#f5操作
class hc_f5(object):
	def __init__(self,node_ip=None,pool_name=None,s_port=None,status=None,monitor_templates=None,vs_name=None,vs_ip=None,vs_port=None):
		self.node_ip = node_ip
		self.pool_name = pool_name
		self.s_port = s_port
		self.status = status
		self.monitor_templates = monitor_templates
		self.vs_name = vs_name
		self.vs_ip = vs_ip
		self.vs_port = vs_port
		self.host = '123.103.77.7'
		self.my_username = 'admin'
		self.my_passwd = 'HC2k05bigip8ip'
#		self.b = bigsuds.BIGIP(hostname = '123.103.77.7',username = 'admin',,password = 'admin')
	#启停node
	def f5_node_control(self):
		#登录F5，密码保密。
		#lb = f5.Lb('123.103.77.7', 'admin', 'admin')
		try:
			b = bigsuds.BIGIP(hostname = self.host,username=self.my_username,password=self.my_passwd)
			#创建node操作对象
		#	pm = f5.PoolMember(node= node_ip, port=80, pool=pool_name, lb=lb)
			b.LocalLB.PoolMember.set_session_enabled_state(['/Common/'+self.pool_name], [[{'member': {'address': self.node_ip, 'port': self.s_port}, 'session_state': self.status}]])
			#控制节点、enabled/disabled
		#	pm.enabled = select1
			#提交操作
		#	pm.save()
			return "ok"
		except:
			return "error..."
	#附件健康检查到应用池中
	def f5_monitor_ass(self):
		b = bigsuds.BIGIP(hostname = self.host,username=self.my_username,password=self.my_passwd)
		print self.pool_name
		print self.monitor_templates
		b.LocalLB.Pool.set_monitor_association(monitor_associations = [{'pool_name': self.pool_name,'monitor_rule':{'type': 'MONITOR_RULE_TYPE_SINGLE','quorum': '2','monitor_templates': [self.monitor_templates]}}])
		#b.LocalLB.Pool.set_monitor_association(monitor_associations = [{'pool_name': 'pool-03','monitor_rule':{'type': 'MONITOR_RULE_TYPE_SINGLE','quorum': '2','monitor_templates': ['newmonitor']}}])
	#创建应用池
	def f5_pool_create(self):
		print '++++++++++++++++++'
		print self.pool_name
		print self.node_ip
		print self.s_port
		b = bigsuds.BIGIP(hostname = self.host,username=self.my_username,password=self.my_passwd)
		b.LocalLB.Pool.create_v2(pool_names = [self.pool_name],lb_methods = ['LB_METHOD_ROUND_ROBIN'],members = [[{'address': self.node_ip, 'port': self.s_port},]])
	#创建负载均衡服务
	def f5_lb_create(self):
		print self.vs_ip
		print self.vs_name
		print self.pool_name
		print self.vs_port
		print type(self.vs_ip)
		print type(self.vs_name)
		print type(self.pool_name)
		b = bigsuds.BIGIP(hostname = self.host,username=self.my_username,password=self.my_passwd)
		b.LocalLB.VirtualServer.create(definitions = [{'name': [self.vs_name], 'address': [self.vs_ip], 'port': [self.vs_port], 'protocol': 'PROTOCOL_TCP'}],wildmasks = ['255.255.255.255'],resources = [{'type': 'RESOURCE_TYPE_POOL', 'default_pool_name': [self.pool_name]}],profiles = [[{'profile_context': 'PROFILE_CONTEXT_TYPE_ALL', 'profile_name': 'tcp'}]])
#		b.LocalLB.VirtualServer.set_snat_automap(virtual_servers = ['creatnew_vs'])

#	node_control(node_ip,pool_name,select1)

#pool = f5.Pool(name='/Common/pool-01', lbmethod='ratio_member', members=[pm], lb=lb)

if __name__ == '__main__':
	#判断用户操作
	select2 = raw_input("请输入你进行的操作：\n1.启、停节点\n2.创建pool\n3.附加健康检查到pool\n4.创建VS应用\n")
	if select2 == '1':
		node_ip = raw_input("请输入node ip： ")
		print node_ip
		pool_name = raw_input("请输入pool name： ")
		print pool_name
		s_port = raw_input("请输入Service Port： ")
		print s_port
		status = raw_input("请输入enabled or disabled： ")
		if status == 'enabled':
			status = 'STATE_ENABLED'
		else:
			status = 'STATE_DISABLED'
		print status
		p = hc_f5(node_ip,pool_name,s_port,status)
		resoult = p.f5_node_control()
		print resoult
	if select2 == '2':
		node_ip = raw_input("请输入node ip： ")
		print node_ip
		pool_name = raw_input("请输入pool name： ")
		print pool_name
		s_port = raw_input("请输入Service Port： ")
		print s_port

		p = hc_f5(node_ip,pool_name,s_port)
		resoult = p.f5_pool_create()
		print resoult

	if select2 == '3':
		pool_name = raw_input("请输入pool name： ")
		print pool_name
		monitor_templates = raw_input("请输入monitor_templates_name： ")
		print monitor_templates
		node_ip=None
		s_port=None
		status=None
		p = hc_f5(node_ip,pool_name,s_port,status,monitor_templates)
		resoult =p.f5_monitor_ass()
		print resoult

	if select2 == '4':
		vs_name = raw_input("请输入vs nanme： ")
		print vs_name
		vs_ip = raw_input("请输入vs ip： ")
		print vs_ip
		print type(vs_ip)
		pool_name = raw_input("请输入pool name： ")
		print pool_name
		vs_port = raw_input("请输入vs port： ")
		print vs_port
		node_ip=None
		s_port=None
		status=None
		monitor_templates=None
		p = hc_f5(node_ip,pool_name,s_port,status,monitor_templates,vs_name,vs_ip,vs_port)
		resoult =p.f5_lb_create()
		print resoult
