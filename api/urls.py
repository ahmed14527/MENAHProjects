# In api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # --- Baby URLs ---
    path('api/baby/', views.create_baby, name='create_baby'),
    
    # --- FacePhoto URLs ---
    path('api/face-photo/', views.upload_face_photo, name='upload_face_photo'),
    path('api/face-photo/all/', views.get_all_face_photos, name='get_all_face_photos'),
    path('api/face-photo/<int:photo_id>/', views.get_face_photo, name='get_face_photo'),
    path('api/face-photo/delete/<int:photo_id>/', views.delete_face_photo, name='delete_face_photo'),
    
    # --- FootPrint URLs ---
    path('api/foot-print/', views.upload_foot_print, name='upload_foot_print'),
    
    # --- RetinaPrint URLs ---
    path('api/retina-print/', views.upload_retina_print, name='upload_retina_print'),
    
    # --- MotherID URLs ---
    path('api/mother-id/', views.upload_mother_id, name='upload_mother_id'),
    
    # --- Mother URLs ---
    path('api/mother/', views.create_mother, name='create_mother'),
    path('api/mother/all/', views.get_all_mothers, name='get_all_mothers'),
    path('api/mother/<int:pk>/', views.get_mother_by_id, name='get_mother_by_id'),
    path('api/mother/update/<int:pk>/', views.update_mother, name='update_mother'),
    path('api/mother/delete/<int:pk>/', views.delete_mother, name='delete_mother'),
    
    # --- Nurse URLs ---
    path('api/nurse/', views.create_nurse, name='create_nurse'),
    path('api/nurse/all/', views.get_all_nurses, name='get_all_nurses'),
    path('api/nurse/approve/<int:pk>/', views.approve_nurse, name='approve_nurse'),
    path('api/nurse/delete/<int:pk>/', views.delete_nurse, name='delete_nurse'),
    
    # --- Parent URLs ---
    path('api/parent/', views.create_parent, name='create_parent'),
    path('api/parent/all/', views.get_all_parents, name='get_all_parents'),
    path('api/parent/<int:pk>/', views.get_parent_by_id, name='get_parent_by_id'),
    path('api/parent/update/<int:pk>/', views.update_parent, name='update_parent'),
    path('api/parent/delete/<int:pk>/', views.delete_parent, name='delete_parent'),
    path('qr-codes/', views.get_all_qr_codes, name='get_all_qr_codes'),
    path('qr-codes/create/', views.create_qr_code, name='create_qr_code'),
    path('qr-codes/<int:pk>/', views.get_qr_code_by_id, name='get_qr_code_by_id'),
    path('qr-codes/<int:pk>/delete/', views.delete_qr_code, name='delete_qr_code'),
]
