from accounts.views.base import Base
from rest_framework.permissions import IsAuthenticated
from accounts.models import User
from accounts.serializers import UserSerializers
from rest_framework.response import Response


class GetUser(Base):
    permission_classes=[IsAuthenticated]

    def get(self, request):
        user = User.objects.filter(id=request.user.id).first()
        enterprise = self.get_enterprese_user(user)

        serializer = UserSerializers(user)

        return Response({
            "user": serializer.data,
            "enterprise": enterprise
        })