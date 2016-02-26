#!/usr/bin/env
#-*- coding:utf-8 -*-
import f5
class get_pool_mem(object):
	def __init__(self,node_ip=None,pool_name=None,s_port=None,status=None,monitor_templates=None,vs_name=None,vs_ip=None,vs_port=None):
		
		self.host = 'ip'
		self.my_username = 'admin'
		self.my_passwd = 'admin'
	
	def get_mem(self):
		print self.host
		print self.my_username
		print self.my_passwd
		lb = f5.Lb(self.host, self.my_username, self.my_passwd)
		pools = lb.pools_get()
		pool_mem_list = []
		for m in pools:
			pms = lb.pms_get(pools=m)
#			print pms
#			pool_mem_list.append(m)
			pool_mem_list.append(pms)
		for m in pool_mem_list:
			print m
		
		
		
		
		
if __name__ == '__main__':

	p = get_pool_mem()
	p.get_mem()
