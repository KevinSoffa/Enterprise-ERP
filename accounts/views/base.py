from rest_framework.views import APIView
from companies.models import Enterprise, Employee
from rest_framework.exceptions import APIException
from ..models import User_Groups, Group_Permissions


class Base(APIView):
    # Método para obter uma empresa baseada em um usuário
    def get_enterprese_user(self, user_id):
        enterprise = {
            "is_owner": False,
            "permissions": []
        }

        enterprise["is_owner"] = Enterprise.objects.filter(user_id=user_id).exists()

        if enterprise["is_owner"]: return enterprise

        # Permissions, GET Employee
        employee = Employee.objects.filter(user_id=user_id).filter()

        if not employee:
            raise APIException("Este usuário não é um funcionário.")
        
        groups = User_Groups.objects.filter(user_id=user_id).all()

        #Pegando todos os Grupos
        for g in groups:
            group = g.group

            permissions = Group_Permissions.objects.filter(group_id=group.id).all()
            for p in permissions:
                enterprise["permissions"].append({
                    "id": p.permission.id,
                    "label": p.permission.name,
                    "codename": p.permission.codename
                })
        
        return enterprise
