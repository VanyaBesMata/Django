from rest_framework import generics, status
from .models import Employee, Position, Department
from .serializers import (EmployeeSerializer, PositionSerializer, DepartmentSerializer,
                          EmployeeDataSerializer, EmployeeListSerializer)

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from rest_framework import views
from rest_framework.response import Response
from rest_framework.reverse import reverse


# Представление всех методов на главной странице.
class APIRootView(views.APIView):
    def get(self, request, format=None):
        data = {
            'employees': reverse('employee_list', request=request, format=format),
            'employee-data': reverse('employee_data', args=[1], request=request, format=format),
            'employees-data-all': reverse('employee_data_all', request=request, format=format),
            'employee-create': reverse('employee_create', request=request, format=format),
            'positions': reverse('position_list', request=request, format=format),
            'departments': reverse('department_list', request=request, format=format),
        }
        return Response(data)


# Показывает все данные из модели Employee.
class EmployeeListAPIView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


# Показывает все данных из модели Position.
class PositionListAPIView(generics.ListAPIView):
    queryset = Position.objects.order_by('position').distinct('position')
    serializer_class = PositionSerializer


# Показывает все данные из модели Department.
class DepartmentListAPIView(generics.ListAPIView):
    queryset = Department.objects.order_by('department').distinct('department')
    serializer_class = DepartmentSerializer


# Показывает все данные по одному сотруднику, по id.
class EmployeeDataView(APIView):
    def get(self, request, employee_id):
        employee = get_object_or_404(Employee, id=employee_id)

        position = Position.objects.filter(employee=employee_id).first()
        department = Department.objects.filter(last_name=employee.last_name).first()

        serializer = EmployeeDataSerializer({
            'id': employee.id,
            'first_name': employee.first_name,
            'last_name': employee.last_name,
            'position': position.position if position else None,
            'department': department.department if department else None,
        })

        return Response(serializer.data)


# Показывает все данные по все сотрудника.
class EmployeeListView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeListSerializer


# Создает нового сотрудника на существующие должности.
class EmployeeCreateView(APIView):
    def get(self, request, format=None):
        positions = Position.objects.order_by('position').distinct('position')
        departments = Department.objects.order_by('department').distinct('department')
        return Response({
            'positions': [{'id': position.id, 'position': position.position} for position in positions],
            'departments': [{'id': department.id, 'department': department.department} for department in departments]
        })

    def post(self, request, format=None):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            employee = serializer.save()

            position_id = request.data.get('position_id')
            department_id = request.data.get('department_id')

            try:
                position = Position.objects.get(id=position_id)
                department = Department.objects.get(id=department_id)

                Position.objects.create(position=position.position, employee=employee.id)
                Department.objects.create(department=department.department, position=position.position,
                                          last_name=employee.last_name, id=employee.id)
            except Position.DoesNotExist:
                return Response({'error': 'Invalid position id'}, status=400)
            except Department.DoesNotExist:
                return Response({'error': 'Invalid department id'}, status=400)

            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)



