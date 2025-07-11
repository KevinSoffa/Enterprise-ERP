from accounts.serializers import UserSerializers
from rest_framework.response import Response
from accounts.auth import Authentication
from accounts.views.base import Base


class Signup(Base):
    # Criando Usário
    def post(self, request):
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')

        user = Authentication.signup(
            self, 
            name=name, 
            email=email, 
            password=password
        )

        serializer = UserSerializers(user)

        return Response({
            "user": serializer.data
        })

