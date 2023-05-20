from django.urls import path
from .views import (EmployeeListAPIView, PositionListAPIView, DepartmentListAPIView, EmployeeDataView, APIRootView,
                    EmployeeListView, EmployeeCreateView)

urlpatterns = [
    path('', APIRootView.as_view(), name='api-root'),
    path('employees/', EmployeeListAPIView.as_view(), name='employee_list'),
    path('employees/<int:employee_id>/', EmployeeDataView.as_view(), name='employee_data'),
    path('employees/all/', EmployeeListView.as_view(), name='employee_data_all'),
    path('employees/create/', EmployeeCreateView.as_view(), name='employee_create'),
    path('positions/', PositionListAPIView.as_view(), name='position_list'),
    path('departments/', DepartmentListAPIView.as_view(), name='department_list'),
]
