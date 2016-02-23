# -*- coding: UTF-8 -*-
#!/usr/bin/env python
import django
import sys,os,time,traceback

platform=sys.platform
if platform.startswith('win'):
    cur_dir = os.path.split(os.path.realpath(sys.argv[0]))[0].split('\\')
else:
    cur_dir = os.path.split(os.path.realpath(sys.argv[0]))[0].split('/')[:-1]
    # print cur_dir
base_dir = '/'.join(cur_dir)
print base_dir
sys.path.append(base_dir)
os.environ['DJANGO_SETTINGS_MODULE'] ='automation.settings'
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "automation.settings")
django.setup()
from auto_f5 import models
import bigsuds
def insert_vip(vip_info):
    try:
        if vips_info:
            if vips_info['vs_ip']:
                vs_ip = vips_info['vs_ip']
            else:
                vs_ip = ''
            if vips_info['vs_name']:
                vs_name = vips_info['vs_name']
            else:
                vs_name = ''
            try:
                if vips_info['vs_port']:
                    vs_port = vips_info['vs_port']
                elif vips_info['vs_port'] == 0:
                    vs_port = 0
            except:
                print traceback.format_exc()
            if vips_info['pool_name']:
                pool_name = vips_info['pool_name']
            else:
                pool_name = ''
            if vips_info['monitor_association']:
                monitor_association = vips_info['monitor_association']
            else:
                monitor_association = ''
            if vs_ip and vs_port >= 0 and vs_name:
                vip = models.VirtualServer.objects.filter(vs_ip=vs_ip).filter(vs_port= vs_port)
                try:
                    if vip:
                        if vip[0].vs_name != vs_name:
                            vip[0].vs_name = vs_name
                            vip[0].save()
                        vip_info = vip[0]
                    else:
                        print vs_ip,vs_name,vs_port
                        vip = models.VirtualServer.objects.create(vs_ip=vs_ip,vs_name=vs_name,vs_port=vs_port)
                        vip_info = vip
                except:
                    print traceback.format_exc()
            else:
                vip_info = ''
            if monitor_association:
                mon_ass = models.Monitor_Association.objects.filter(monitor_association_name=monitor_association)
                try:
                    if not mon_ass:
                        print monitor_association
                        mon_as = models.Monitor_Association.objects.create(monitor_association_name=monitor_association)
                        mon = mon_as
                    else:
                        mon = mon_ass[0]
                except:
                    print traceback.format_exc()
            else:
                mon = ''
            if pool_name:
                pool = models.Pool.objects.filter(pool_name=pool_name)
                if vip_info and mon:
                    try:
                        if pool:
                            if pool[0].vip != vip_info:
                                pool[0].vip = vip_info
                            if pool[0].monitor_association != mon:
                                pool[0].monitor_association = mon
                            pool[0].save()
                            pool_info = pool[0]
                        else:
                            print pool_name,vip_info,mon
                            poo = models.Pool(pool_name=pool_name,vip=vip_info,monitor_association=mon)
                            poo.save()
                            pool_info = poo
                    except:
                        print traceback.format_exc()
                elif vip_info and not mon:
                    try:
                        if pool:
                            if pool[0].vip != vip_info:
                                pool[0].vip = vip_info
                            pool[0].save()
                            pool_info = pool[0]
                        else:
                            print pool_name,vip_info,mon
                            poo = models.Pool(pool_name=pool_name,vip=vip_info)
                            poo.save()
                            pool_info = poo
                    except:
                        print traceback.format_exc()
                elif not vip_info and mon:
                    try:
                        if pool:
                            if pool[0].monitor_association != mon:
                                pool[0].monitor_association = mon
                            pool[0].save()
                            pool_info = pool[0]
                        else:
                            print pool_name,vip_info,mon
                            poo = models.Pool(pool_name=pool_name,monitor_association=mon)
                            poo.save()
                            pool_info = poo
                    except:
                        print traceback.format_exc()
                else:
                    try:
                        if not pool:
                            print pool_name,vip_info,mon
                            poo = models.Pool(pool_name=pool_name)
                            poo.save()
                            pool_info = poo
                    except:
                        print traceback.format_exc()
            else:
                pool_info = ''
            if vips_info['nodes']:
                # print "$$$"
                if pool_info:
                    for j in vips_info['nodes']:
                        # print "##"
                        if j['node_ip']:
                            # print "&&&"
                            try:
                                node = pool_info.node.filter(node_ip=j['node_ip']).filter(port=j['node_port'])
                                if node:
                                    if node[0].status != j['node_status']:
                                        node[0].status = j['node_status']
                                        node[0].save()
                                else:
                                    print j['node_ip'],j['node_port'],j['node_status']
                                    nod = models.Node.objects.filter(node_ip=j['node_ip']).filter(port=j['node_port'])
                                    if nod:
                                        if nod[0].status != j['node_status']:
                                            nod[0].status = j['node_status']
                                            pool_info.node.add(nod[0])
                                            pool_info.save()
                                        else:
                                            pool_info.node.add(nod[0])
                                            pool_info.save()
                                    else:
                                        pool_info.node.add(models.Node.objects.create(node_ip=j['node_ip'],port=j['node_port'],status=j['node_status']))
                                        pool_info.save()
                            except:
                                print traceback.format_exc()
                else:
                    try:
                        node = models.Node.objects.filter(node_ip=j['node_ip']).filter(port=j['node_port'])
                        if node:
                            if node[0].status != j['node_status']:
                                node[0].status = j['node_status']
                                node[0].save()
                        else:
                            models.Node.objects.create(node_ip=j['node_ip'],port=j['node_port'],status=j['node_status'])
                    except:
                        print traceback.format_exc()
    except:
        pass
#{'pool_name': ['/Common/pool_BI_2_pool'], 'monitor_association': ['/Common/tcp_30sec'], 'vs_ip': '123.103.77.173', 'vs_port': 80, 'vs_name': '/Common/vs_BI_2_vip', 'nodes': [{'node_status': 'SESSION_STATUS_ENABLED', 'node_port': 80, 'node_ip': '192.168.60.178'}]}
def get_mem():
    #登录F5
    b = bigsuds.BIGIP(hostname = '123.103.77.7',username='admin',password='HC2k05bigip8ip')
    #获取vs_name
    vs_names_list = b.LocalLB.VirtualServer.get_list()
    #print 'vs_names_list:',vs_names_list
    #['/Common/anyipforward', '/Common/vs_BI_2_vip', '/Common/vs_BI_vip', '/Common/vs_activityb2b_vip', '/Common/vs_alarmorg_vip', '/Common/vs_ask_vip', ]
    #创建一个空字典，存储vs_name':vs_name,'vs_ip':vs_ip,'vs_port':vs_port,'pool_name':pool_name,'monitor_association':monitor_association
    
    
    if vs_names_list:
        for vs_name in vs_names_list:
            pool_mem_vip_dict = {}
            print vs_name
            pool_mem_vip_dict['vs_name'] = vs_name.split('/')[2]
            vip_port = b.LocalLB.VirtualServer.get_destination([vs_name])
            pool_mem_vip_dict['vs_ip'] = vip_port[0]['address']
            pool_mem_vip_dict['vs_port'] = vip_port[0]['port']
            #通过vs_name获取poolname
            poolname = b.LocalLB.VirtualServer.get_default_pool_name([vs_name])
            print 'pool name:',poolname
            if poolname[0]:
                pool_mem_vip_dict['pool_name'] = poolname[0].split('/')[2]
            else:
                pool_mem_vip_dict['pool_name'] = ''
            
            #通过vs_name获取健康检查
            try:
                monitor_association = b.LocalLB.PoolMember.get_monitor_association(poolname)
                pool_mem_vip_dict['monitor_association'] = monitor_association[0][0]['monitor_rule']['monitor_templates'][0].split('/')[2]
            except:
                pool_mem_vip_dict['monitor_association'] = ""

            #通过poolname获取node_ip，node_port,node_status
            nodelist_list = []
            
            nodelist = b.LocalLB.PoolMember.get_session_status([poolname])
            #[[{'member': {'port': 80, 'address': '192.168.60.124'}, 'session_status': 'SESSION_STATUS_FORCED_DISABLED'}, {'member': {'port': 80, 'address': '192.168.60.135'}, 'session_status': 'SESSION_STATUS_FORCED_DISABLED'}, {'member': {'port': 80, 'address': '192.168.60.172'}, 'session_status': 'SESSION_STATUS_ENABLED'}]]
            if nodelist[0]:
                for ele in nodelist[0]:
                    nodelist_dict = {}
                    nodelist_dict['node_ip'] = ele['member']['address']
                    nodelist_dict['node_port'] = ele['member']['port']
                    nodelist_dict['node_status'] = ele['session_status']
                    print nodelist_dict
                    nodelist_list.append(nodelist_dict)
                pool_mem_vip_dict['nodes'] = nodelist_list
            else:
                pool_mem_vip_dict['nodes'] = []
            print pool_mem_vip_dict

            insert_vip(pool_mem_vip_dict)


#[{'vs_name':vs_name,'vs_ip':vs_ip,'vs_port':vs_port,'pool_name':pool_name,'monitor_association':monitor_association,nodes:[{'node_ip':ip,'node_port':port,'status':status},{'node_ip':ip,'node_port':port,'status':status},]},]


if __name__ == '__main__':
    get_mem()