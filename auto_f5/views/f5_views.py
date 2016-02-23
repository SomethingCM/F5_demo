#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext
from django.contrib.auth.decorators import login_required
from automation.common.CommonPaginator import SelfPaginator
from auto_auth.views.permission import PermissionVerify
from auto_f5.models import *
from f5_model import *
import json
from django.shortcuts import redirect

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ParseError
from rest_framework import status

from django.contrib.auth.models import User

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework import parsers
from rest_framework import renderers
from rest_framework.authtoken.serializers import AuthTokenSerializer
import datetime
from django.utils.timezone import utc
from django.utils import timezone
from rest_framework.authtoken.views import ObtainAuthToken


class F5_ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        utc_now = datetime.datetime.utcnow()    
        if not created and token.created < utc_now - datetime.timedelta(hours=24):
            token.delete()
            token = Token.objects.create(user=serializer.object['user'])
            token.created = datetime.datetime.utcnow()
            token.save()
        return Response({'token': token.key})


F5_ObtainAuthToken = ObtainAuthToken.as_view()


class ObtainExpiringAuthToken(ObtainAuthToken):
    def post(self, request):
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            token, created =  Token.objects.get_or_create(user=serializer.object['user'])


            utc_now = datetime.datetime.utcnow()    
            if not created and token.created < utc_now - datetime.timedelta(hours=24):
                token.delete()
                token = Token.objects.create(user=serializer.object['user'])
                token.created = datetime.datetime.utcnow()
                token.save()

            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# Create your views here.


# class AuthView(APIView):
    # """
    # Authentication is needed for this methods
    # """
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    # def get(self, request, format=None):
        # return Response({'detail': "I suppose you are authenticated"})
# class TestView(APIView):
    # """
    # """

    # def get(self, request, format=None):
        # return Response({'detail': "GET Response"})

    # def post(self, request, format=None):
        # try:
            # data = request.DATA
        # except ParseError as error:
            # return Response(
                # 'Invalid JSON - {0}'.format(error.detail),
                # status=status.HTTP_400_BAD_REQUEST
            # )
        # if "user" not in data or "password" not in data:
            # return Response(
                # 'Wrong credentials',
                # status=status.HTTP_401_UNAUTHORIZED
            # )

        # user = User.objects.first()
        # if not user:
            # return Response(
                # 'No default user, please create one',
                # status=status.HTTP_404_NOT_FOUND
            # )

        # token = Token.objects.get_or_create(user=user)

        # return Response({'detail': 'POST answer', 'token': token[0].key})

def get_vip_info(request):
    vip_info = []
    pools = Pool.objects.all()
    if pools:
        for i in pools:
            info = {}
            info['pool_name']=i.pool_name
            info['vs_name']=i.vip.vs_name
            info['vs_ip']=i.vip.vs_ip
            info['vs_port']=i.vip.vs_port
            if i.monitor_association:
                info['monitor_association']=i.monitor_association.monitor_association_name
            else:
                info['monitor_association']=''
            nodes = i.node.all()
            node = []
            if nodes:
                for j in nodes:
                    node.append({'node_ip':j.node_ip,'node_port':j.port,'status':j.status})
            info['nodes']=node
            if info:
                vip_info.append(info)
    # eother_nodes = Node.objects.filter(pool__isnull=True)
    return HttpResponse(json.dumps(vip_info))
def node_control(request):
    if request.method == "POST":
        pool_name = request.POST.get('pool_name').encode('utf-8')
        node_ip = request.POST.get('node_ip').encode('utf-8')
        node_port = request.POST.get('node_port').encode('utf-8')
        statu = request.POST.get('status').encode('utf-8')
        auto_f5 = hc_f5()
        node = Node.objects.get(node_ip=node_ip)
        if statu == 'SESSION_STATUS_ENABLED':
            stat = 'STATE_ENABLED'
        elif statu == 'SESSION_STATUS_FORCED_DISABLED':
            stat = 'STATE_DISABLED'
        print '$$$$$$$$$$$$$$$$$$'
        print pool_name,node_ip,node_port,stat
        print '$$$$$$$$$$$$$$$$$$'
        # return HttpResponse(json.dumps(statu))
        res = auto_f5.f5_node_control(pool_name=pool_name,node_ip=node_ip,node_port=node_port,status=stat)
        if res == 'ok':
            if node.status != statu:
                node.status = statu
                node.save()
            return HttpResponse('ok')
        else:
            return HttpResponse('error')
def search(request):
    user = request.user
    tag = request.GET.get('tag')
    info = Pool.objects.filter(Q(node__node_ip__icontains=tag)|Q(pool_name__icontains=tag)|Q(vip__vs_ip__icontains=tag)|Q(vip__vs_name__icontains=tag))
    return render_to_response('auto_f5/listpool.html',{'lPage':info,'user':user})
@login_required(login_url="/login/")
def listpool(request):
    user = request.user
    pools = Pool.objects.all()
    lst = SelfPaginator(request,pools, 30)
    kwvars = {
        'lPage':lst,
        'request':request,
        'user':user
    }
    return render_to_response('auto_f5/listpool.html',kwvars,RequestContext(request))
@login_required(login_url="/login/")
def node_define(request,pool_id,node_id):
    # print pool_id,node_id
    user = request.user
    pool = Pool.objects.get(id=pool_id)
    node = pool.node.get(id=node_id)
    if request.method == "GET":
        return render_to_response('auto_f5/node.html',{'user':user,'pool_id':pool.id,'node':node})
    elif request.method == "POST":
        statu = request.POST.get('status').encode('utf-8')
        if statu == 'SESSION_STATUS_ENABLED':
            stat = 'STATE_ENABLED'
        elif statu == 'SESSION_STATUS_FORCED_DISABLED':
            stat = 'STATE_DISABLED'
        # print '$$$$$$$$$$$$$$$$$$'
        # print type(statu)
        auto_f5 = hc_f5()
        res = auto_f5.f5_node_control(pool_name=pool.pool_name,node_ip=node.node_ip,node_port=node.port,status=stat)
        # print res
        if res == 'ok':
            if node.status != statu:
                node.status = statu
                node.save()
            return render_to_response('auto_f5/node.html',{'user':user,'pool_id':pool.id,'node':node})
        else:
            return render_to_response('auto_f5/node.html',{'user':user,'pool_id':pool.id,'node':node})
    else:
        return render_to_response('auto_f5/node.html',{'user':user,'pool_id':pool.id,'node':node})