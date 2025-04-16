from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import MilkRecord, QRCode, Message, LoginHistory
from .serializers import MilkRecordSerializer, QRCodeSerializer, MessageSerializer, LoginHistorySerializer
from .permissions import IsNurse, IsAdmin, IsParent
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import RegisterSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class MilkRecordViewSet(viewsets.ModelViewSet):
    queryset = MilkRecord.objects.all()
    serializer_class = MilkRecordSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['baby_name', 'date_given']
    search_fields = ['baby_name']
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'nurse':
            return MilkRecord.objects.filter(nurse=user)
        elif user.role == 'parent':
            return MilkRecord.objects.all()
        elif user.role == 'admin':
            return MilkRecord.objects.all()
        return MilkRecord.objects.none()

    def perform_create(self, serializer):
        serializer.save(nurse=self.request.user)

class QRCodeViewSet(viewsets.ModelViewSet):
    queryset = QRCode.objects.all()
    serializer_class = QRCodeSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsNurse()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(recipient=user) | Message.objects.filter(sender=user)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class LoginHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LoginHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return LoginHistory.objects.filter(user=self.request.user)


# Authentication Views
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['role'] = self.user.role
        data['username'] = self.user.username
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
