from rest_framework import viewsets
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .models import CustomUser
from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import generics, permissions
from .models import LoginHistory
from .serializers import LoginHistorySerializer ,UserProfileSerializer
from api.permissions import IsNurseUser,IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]




class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        token['role'] = user.role
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class LoginHistoryListView(generics.ListAPIView):
    serializer_class = LoginHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return LoginHistory.objects.filter(user=self.request.user)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_object(self):
        return self.request.user
    
    
    

class AllUserProfilesView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    permission_classes = [IsAdminUser]
    
    
class UserProfileDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    permission_classes = [IsAdminUser]
    permission_classes = [IsNurseUser]

    lookup_field = 'id'
    
    
    


class ApproveRejectNurseEmailView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, nurse_id):
        try:
            nurse = CustomUser.objects.get(id=nurse_id, role='Nurse')
        except CustomUser.DoesNotExist:
            return Response({"detail": "Nurse not found."}, status=status.HTTP_404_NOT_FOUND)

        action = request.data.get('action')

        if action not in ['approve', 'reject']:
            return Response({"detail": "Invalid action. Use 'approve' or 'reject'."}, status=status.HTTP_400_BAD_REQUEST)

        if action == 'approve':
            nurse.is_email_approved = True
            nurse.save()
            return Response({"detail": "Email approved successfully."}, status=status.HTTP_200_OK)
        elif action == 'reject':
            nurse.is_email_approved = False
            nurse.save()
            return Response({"detail": "Email rejected successfully."}, status=status.HTTP_200_OK)
