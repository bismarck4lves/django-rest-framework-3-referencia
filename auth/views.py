from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from auth.serializer import UserSerializer


class LoginViewSet(ObtainAuthToken):

    queryset = Token.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'id': user.pk,
            'username': user.username,
            'email': user.email,
            'is_staff': user.is_staff,
            'token': token.key

        }, status=status.HTTP_200_OK)

    
class CreateUserViewSet(viewsets.ModelViewSet):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class LogoutViewSet(APIView):
    
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request, format=None):
        request.user.auth_token.delete()
        return Response('Deslogado', status=status.HTTP_200_OK)
