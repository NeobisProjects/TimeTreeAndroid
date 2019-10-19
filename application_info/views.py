from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from application_info.models import University, Department
from application_info.serializers import UniversitySerializer, DepartmentSerializer


class ValuesAPIView(APIView):
    def get(self, request):
        universities = UniversitySerializer(University.objects.all(),
                                            many=True).data
        departments = DepartmentSerializer(Department.objects.all(),
                                           many=True).data
        data = {
            "universities": universities,
            "departments": departments,
        }

        return Response(data=data, status=status.HTTP_200_OK)

