from rest_framework.viewsets import ModelViewSet
from unicloud_users.api.serializers import UserProfileSerializer, UserSerializer, LoginTokenSerializer
from unicloud_users.models import UserProfile
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView

class GetUserProfile(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get_queryset(self):  # added string
        return super().get_queryset().filter(id=self.request.user.id)



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = LoginTokenSerializer

    def get_object(self):
        return self.request.user