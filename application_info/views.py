# Create your views here.
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from application_info.models import Department
from application_info.serializers import DepartmentSerializer


class ValuesAPIView(APIView):
    def get(self, request):
        departments = DepartmentSerializer(Department.objects.all(),
                                           many=True).data

        return Response(data=departments, status=status.HTTP_200_OK)
