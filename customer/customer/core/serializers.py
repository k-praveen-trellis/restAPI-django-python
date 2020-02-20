from rest_framework import serializers
from .models import *

class CustomerSerializer(serializers.ModelSerializer):
    num_professions = serializers.SerializerMethodField()
    datasheet = serializers.StringRelatedField()

    class Meta:
        model = Customer
        fields = ('id','name','address','profession','datasheet','active','num_professions')

    def get_num_professions(self,obj):
        return obj.num_professions()


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ('id','description')

class DocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = ('id','dtype','doc_number','customer')

class DatasheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Datasheet
        fields = ('id','description','historical_data')

