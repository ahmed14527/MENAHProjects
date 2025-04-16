from django.contrib import admin
from .models import User, MilkRecord, QRCode, Message, LoginHistory

# Register User model with custom admin configuration
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role', 'email', 'first_name', 'last_name', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'role')
    list_filter = ('role', 'is_active')

admin.site.register(User, UserAdmin)

# Register MilkRecord model with custom admin configuration
class MilkRecordAdmin(admin.ModelAdmin):
    list_display = ('baby_name', 'milk_amount_ml', 'date_given', 'nurse')
    search_fields = ('baby_name', 'nurse__username')
    list_filter = ('date_given', 'nurse')

admin.site.register(MilkRecord, MilkRecordAdmin)

# Register QRCode model with custom admin configuration
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'milk_record', 'created_by', 'created_at', 'is_used')
    search_fields = ('milk_record__baby_name', 'created_by__username')
    list_filter = ('is_used', 'created_at')

admin.site.register(QRCode, QRCodeAdmin)

# Register Message model with custom admin configuration
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'sent_at', 'content')
    search_fields = ('sender__username', 'recipient__username', 'content')
    list_filter = ('sent_at',)

admin.site.register(Message, MessageAdmin)

# Register LoginHistory model with custom admin configuration
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'ip_address')
    search_fields = ('user__username', 'ip_address')
    list_filter = ('timestamp',)

admin.site.register(LoginHistory, LoginHistoryAdmin)
