from rest_framework import serializers
from .models import Employee, Position, Department


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ('position',)


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('department',)


class EmployeeDataSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    position = serializers.CharField(max_length=50, allow_null=True)
    department = serializers.CharField(max_length=50, allow_null=True)


class EmployeeListSerializer(serializers.ModelSerializer):
    position = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'position', 'department']

    def get_position(self, employee):
        position = Position.objects.filter(employee=employee.id).first()
        return position.position if position else None

    def get_department(self, employee):
        department = Department.objects.filter(last_name=employee.last_name).first()
        return department.department if department else None

