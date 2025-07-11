from accounts.views.base import Base
from accounts.auth import Authentication
from accounts.serializers import UserSerializers
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


class Signin(Base):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = Authentication.signin(self, email, password) # Se der erro o método já retorna

        # Pegando TOKEN JWT [ autenticando usuário ]
        token = RefreshToken.for_user(user)

        enterprise = self.get_enterprese_user(user.id) # Função em base

        serializer = UserSerializers(user)

        return Response({
            "user": serializer.data,
            "enterprise": enterprise,
            "refresh": str(token),
            "access": str(token.access_token)
        })


