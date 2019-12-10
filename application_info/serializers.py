from rest_framework import serializers

from application_info.models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name')
