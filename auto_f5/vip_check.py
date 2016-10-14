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


vips_info = [{}]
try:
    for i in vips_info:
        if i['vs_ip']:
            vs_ip = i['vs_ip']
        else:
            vs_ip=''
        if i['vs_name']:
            vs_name = i['vs_name'].split('/')[2]
        else:
            vs_name=''
        try:
            if i['vs_port'] :
                vs_port = i['vs_port']
            elif i['vs_port'] == 0:
                vs_port = 0
            # else:
                # vs_port =''
        except:
            print traceback.format_exc()

        
        if i['pool_name'][0]:
            # print "$$$$",i['pool_name']
            pool_name = i['pool_name'][0].split('/')[2]
        else:
            pool_name=''
        if i['monitor_association']:
            # print '####'
            monitor_association = i['monitor_association'][0].split('/')[2]
        else:
            # print '#@@###'
            monitor_association = ''
        if vs_ip and vs_port >= 0 and vs_name:
            # print vs_ip,vs_name,vs_port
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
                break
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
                break
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
                    break
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
                    break
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
                    break
            else:
                try:
                    if not pool:
                        print pool_name,vip_info,mon
                        poo = models.Pool(pool_name=pool_name)
                        poo.save()
                        pool_info = poo
                except:
                    print traceback.format_exc()
                    break
        else:
            pool_info = ''
        if i['nodes']:
            # print "$$$"
            if pool_info:
                for j in i['nodes']:
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
                                
                                try:
                                    nod = models.Node.objects.filter(node_ip=j['node_ip']).filter(port=j['node_port'])
                                    print nod
                                    print "#$#$#$"
                                    if nod:
                                        if nod[0].status != j['node_status']:
                                            nod[0].status = j['node_status']
                                            print nod
                                            pool_info.node.add(nod[0])
                                            pool_info.save()
                                        else:
                                            pool_info.node.add(nod[0])
                                            pool_info.save()
                                    else:
                                        print j['node_ip'],j['node_port'],j['node_status']
                                        node = models.Node.objects.create(node_ip=j['node_ip'],port=j['node_port'],status=j['node_status'])
                                        pool_info.node.add(node)
                                        pool_info.save()
                                except:
                                    print traceback.format_exc()
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
        # print traceback.format_exc()
