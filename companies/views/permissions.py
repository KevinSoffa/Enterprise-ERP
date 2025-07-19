from companies.views.base import Base
from companies.utils.permissions import GroupPermissionsPermission
from companies.serializers import PermissionsSerializers
from rest_framework.response import Response
from django.contrib.auth.models import Permission


class PermissionDetail(Base):
    permission_classes = [GroupPermissionsPermission]

    def get(self, request):
        permissions = Permission.objects.filter(content_type_id__in=[2, 7, 11, 13]).all()

        serializer = PermissionsSerializers(permissions, many=True)

        return Response({"permissions": serializer.data})