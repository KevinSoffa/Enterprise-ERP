from rest_framework import permissions
from accounts.models import User_Groups, Group_Permissions
from django.contrib.auth.models import Permission


# Função para checar as permissões
def check_permission(user, method, permission_to): # user -> vem da requisição | method -> Tipo da requisição | permission_to -> Tipo de permissão de acesso
    if not user.is_authenticated:
        return False
    
    if user.is_owner:
        return True
    
    required_permission = 'view_' + permission_to
    if method == 'POST':
        required_permission = 'add_'+permission_to
    elif method == 'PUT':
        required_permission = 'change_'+permission_to
    elif method == 'DELETE':
        required_permission = 'delete_'+permission_to

    # Verificando Grupo de usuário
    groups = User_Groups.objects.values('group_id').filter(user_id=user.id).all() # Pegando id do groups

    for group in groups:
        permissions = Group_Permissions.objects.values('permission_id').filter(group_id=group['group_id']).all()

        # Verificando qual required
        for permission in permissions:
            if Permission.objects.filter(id=permission['permission_id'], codename=required_permission).exists():
                return True

class EmployeesPermission(permissions.BasePermission):
    message = 'O funcionário não tem permissão para gerenciar outros...'

    def has_permission(self, request, _view):
        return check_permission(request.user, request.method, permission_to='employee')
    
class GroupsPermission(permissions.BasePermission):
    message = 'O funcionário não tem permissão para gerenciar os Grupos...'

    def has_permission(self, request, _view):
        return check_permission(request.user, request.method, permission_to='group')
    
class GroupPermissionsPermission(permissions.BasePermission):
    message = 'O funcionário não tem permissão para gerenciar as Permissões...'
    def has_permission(self, request, _view):
        return check_permission(request.user, request.method, permission_to='permission')
    
class TaskPermission(permissions.BasePermission):
    message = 'O funcionário não tem permissão para gerenciar Tarefas de outros funcionários...'
    def has_permission(self, request, _view):
        return check_permission(request.user, request.method, permission_to='task')