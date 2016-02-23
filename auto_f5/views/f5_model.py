#!/usr/bin/env
#-*- coding:utf-8 -*-
import bigsuds
#f5����
class hc_f5(object):
    def __init__(self):
        # self.host = '123.103.77.7'
        self.host = '123.103.77.8'
        self.my_username = 'admin'
        self.my_passwd = 'HC2k05bigip8ip'
    #��ͣnode
    def f5_node_control(self,pool_name,node_ip,node_port,status):
        #��¼F5�����뱣�ܡ�
        try:
            print pool_name,node_ip,node_port,status
            b = bigsuds.BIGIP(hostname = self.host,username=self.my_username,password=self.my_passwd)
            # print "#####"
            b.LocalLB.PoolMember.set_session_enabled_state(['/Common/'+pool_name], [[{'member': {'address': node_ip, 'port': node_port}, 'session_state': status}]])
            #���ƽڵ㡢enabled/disabled
            # print 'ok'
            return "ok"
        except:
            return "error..."
    #����������鵽Ӧ�ó���
    def f5_monitor_ass(self,pool_name,monitor_templates):
        b = bigsuds.BIGIP(hostname = self.host,username=self.my_username,password=self.my_passwd)
        print self.pool_name
        print self.monitor_templates
        b.LocalLB.Pool.set_monitor_association(monitor_associations = [{'pool_name': pool_name,'monitor_rule':{'type': 'MONITOR_RULE_TYPE_SINGLE','quorum': '2','monitor_templates': [monitor_templates]}}])
    #����Ӧ�ó�
    def f5_pool_create(self,pool_name,node_ip,node_port):
        b = bigsuds.BIGIP(hostname = self.host,username=self.my_username,password=self.my_passwd)
        b.LocalLB.Pool.create_v2(pool_names = [pool_name],lb_methods = ['LB_METHOD_ROUND_ROBIN'],members = [[{'address': node_ip, 'port': node_port},]])
    #�������ؾ������
    def f5_lb_create(self,pool_name,vs_name,vs_ip,vs_port):
        b = bigsuds.BIGIP(hostname = self.host,username=self.my_username,password=self.my_passwd)
        b.LocalLB.VirtualServer.create(definitions = [{'name': [vs_name], 'address': [vs_ip], 'port': [vs_port], 'protocol': 'PROTOCOL_TCP'}],wildmasks = ['255.255.255.255'],resources = [{'type': 'RESOURCE_TYPE_POOL', 'default_pool_name': [pool_name]}],profiles = [[{'profile_context': 'PROFILE_CONTEXT_TYPE_ALL', 'profile_name': 'tcp'}]])
# if __name__ == '__main__':
    # �ж��û�����
    # select2 = raw_input("����������еĲ�����\n1.����ͣ�ڵ�\n2.����pool\n3.���ӽ�����鵽pool\n4.����VSӦ��\n")
    # if select2 == '1':
        # node_ip = raw_input("������node ip�� ")
        # print node_ip
        # pool_name = raw_input("������pool name�� ")
        # print pool_name
        # s_port = raw_input("������Service Port�� ")
        # print s_port
        # status = raw_input("������enabled or disabled�� ")
        # if status == 'enabled':
            # status = 'STATE_ENABLED'
        # else:
            # status = 'STATE_DISABLED'
        # print status
        # p = hc_f5(node_ip,pool_name,s_port,status)
        # resoult = p.f5_node_control()
        # print resoult
    # if select2 == '2':
        # node_ip = raw_input("������node ip�� ")
        # print node_ip
        # pool_name = raw_input("������pool name�� ")
        # print pool_name
        # s_port = raw_input("������Service Port�� ")
        # print s_port

        # p = hc_f5(node_ip,pool_name,s_port)
        # resoult = p.f5_pool_create()
        # print resoult

    # if select2 == '3':
        # pool_name = raw_input("������pool name�� ")
        # print pool_name
        # monitor_templates = raw_input("������monitor_templates_name�� "
        # print monitor_templates
        # node_ip=None
        # s_port=None
        # status=None
        # p = hc_f5(node_ip,pool_name,s_port,status,monitor_templates)
        # resoult =p.f5_monitor_ass()
        # print resoult

	# if select2 == '4':
		# vs_name = raw_input("������vs nanme�� ")
		# print vs_name
		# vs_ip = raw_input("������vs ip�� ")
		# print vs_ip
		# print type(vs_ip)
		# pool_name = raw_input("������pool name�� ")
		# print pool_name
		# vs_port = raw_input("������vs port�� ")
		# print vs_port
		# node_ip=None
		# s_port=None
		# status=None
		# monitor_templates=None
		# p = hc_f5(node_ip,pool_name,s_port,status,monitor_templates,vs_name,vs_ip,vs_port)
		# resoult =p.f5_lb_create()
		# print resoult
