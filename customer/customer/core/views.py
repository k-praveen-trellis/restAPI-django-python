from django.shortcuts import render 
from rest_framework.response import Response
from django.http import Http404
from rest_framework.filters import SearchFilter
from rest_framework import filters
from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser

class UserViewSet(viewsets.ModelViewSet):
    # queryset = Customer.objects.all()
    serializer_class =  CustomerSerializer
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['name', 'address']
    # filter_fields = ('address',)
    ordering_fields = ['name']
    lookup_field = 'name'
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAdminUser]
    def get_queryset(self):
        # id = self.request.query_params.get('id',None)
        # status = True if self.request.query_params['active']==True else False
        # if id is not None:
        #     customer = Customer.objects.filter(id=id,active=status)
        # else:
        #     customer = Customer.objects.filter(active=status)
        # id = self.request.query_params.get('id',None)
        # if self.request.query_params['active']=="True":
        #     status = True 
        # else:
        #     status = False 
        # print(status)

        customer = Customer.objects.all()

        # address = self.request.query_params.get('address')
        # print(address)
        # print(type(address))
        # if address is not None:
        #     customer = Customer.objects.filter(address__icontains=address)
        # else:
        #     customer = Customer.objects.filter(active=False)

        return customer
    
    # def list(self,request,*args,**kwargs):
    #     customer = self.get_queryset()
    #     serializer = CustomerSerializer(customer,many=True)
    #     return Response(serializer.data)

    def retrieve(self,request,*args,**kwargs):
        obj = self.get_object()
        # customer = Customer.objects.filter(id=1)
        serializer = CustomerSerializer(obj)
        return Response(serializer.data)

    def create(self,request,*args,**kwargs):
        data = request.data
        customer = Customer.objects.create(name=data['name'],address = data['address'],datasheet = data['datasheet'])
        profession = Profession.objects.get(id=data['profession'])
        customer.profession.add(profession)
        customer.save()
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def update(self,request,*args,**kwargs):
        customer = self.get_object()
        data=request.data
        customer.name = data['name']
        customer.address = data['address']
        customer.datasheet_id = data['datasheet']
        professions = Profession.objects.get(id=data['profession'])
        customer.profession.add(professions)
        customer.save()
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def partial_update(self,request,*args,**kwargs):
        customer = self.get_object()
        customer.name = request.data.get('name',customer.name)
        customer.address = request.data.get('address',customer.address)
        customer.datasheet_id = request.data.get('datasheet',customer.datasheet_id)
        customer.save()
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)
    
    def destroy(self,request,*args,**kwargs):
        customer = self.get_object()
        customer.delete()
        return Response('Deleted Successfully!')
    
    @action(detail = True)
    def deactivate(self,requst,*args, **kwargs):
        customer = self.get_object()
        customer.active = False
        customer.save()
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    @action(detail = False)
    def deactivate_all(self,requst,*args, **kwargs):
        customer = self.get_queryset()
        customer.update(active=False)
        # customer.save()
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)
    
    @action(detail = False)
    def activate_all(self,requst,*args, **kwargs):
        customer = self.get_queryset()
        customer.update(active=True)
        # customer.save()
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    @action(detail = False,methods = ["POST"])
    def change_status(self,requst,*args, **kwargs):
        status = bool(requst.data['active'])
        customer = self.get_queryset()
        customer.update(active=not status)
        # customer.save()
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

class ProfessionViewSet(viewsets.ModelViewSet):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Documents.objects.all()
    serializer_class = DocumentsSerializer


class DatasheetViewSet(viewsets.ModelViewSet):
    queryset = Datasheet.objects.all()
    serializer_class = DatasheetSerializer