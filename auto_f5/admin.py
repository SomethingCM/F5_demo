from django.contrib import admin
from models import Monitor_Association,Pool,Node,VirtualServer
#Register your models here.
class Monitor_AssociationAdmin(admin.ModelAdmin):
    list_display=('monitor_association_name',)
class PoolAdmin(admin.ModelAdmin):
    model=Pool
    filter_horizontal = ('node',) 
    list_display=('vip','pool_name','monitor_association')
class NodeAdmin(admin.ModelAdmin):
    list_display=('node_ip','port','status')
class VirtualServerAdmin(admin.ModelAdmin):
    list_display=('vs_ip','vs_name','vs_port')
admin.site.register(Monitor_Association, Monitor_AssociationAdmin)
admin.site.register(Pool, PoolAdmin)
admin.site.register(Node, NodeAdmin)
admin.site.register(VirtualServer, VirtualServerAdmin)

