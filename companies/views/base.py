from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404
from companies.utils.exceptions import (
    NotFoundEmployee,
    NotFoundGroup,
    NotFoundTask,
    NotFoundTaskStatus,
)
from companies.models import Employee, Enterprise, Task, TaskStatus
from accounts.models import Group


class Base(APIView):
    def get_employee(self, employee_id, user_id):
        enterprise_id = self.get_enterprise_id(user_id)
        return get_object_or_404(Employee, id=employee_id, enterprise_id=enterprise_id)
    
    # def get_employee(self, employee_id, user_id):
    #     enterprise_id = self.get_enterprise_id(user_id)

    #     employee = Employee.objects.filter(id=employee_id, enterprise_id=enterprise_id)

    #     if not employee:
    #         raise NotFoundEmployee
        
    #     return employee
    
    def get_group(self, group_id, enterprise_id):
        group = Group.objects.values('name').filter(id+group_id, enterprise_id=enterprise_id).first()

        if not group:
            raise NotFoundGroup
        
        return group
    
    def get_status(self, status_id):
        status = TaskStatus.objects.filter(id=status_id).first()

        if not status:
            raise NotFoundTaskStatus
        
        return status
    
    def get_task(self, task_id, enteprise_id):
        task = Task.objects.filter(id=task_id, enteprise_id=enteprise_id).first()

        if not task:
            raise NotFoundTask
        
        return task
    
    def get_enterprise_id(self, user_id):
        enterprise = Enterprise.objects.filter(user_id=user_id).first()
        if enterprise:
            return enterprise.id
        else:
            # pode lançar exceção, retornar None, ou tratar
            raise NotFound("Empresa não encontrada para o usuário")