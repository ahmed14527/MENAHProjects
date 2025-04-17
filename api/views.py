from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Baby, FacePhoto, FootPrint, RetinaPrint, MotherID, Mother, Nurse, Parent
from .serializers import BabySerializer, FacePhotoSerializer, FootPrintSerializer, RetinaPrintSerializer, MotherIDSerializer, MotherSerializer, NurseSerializer, ParentSerializer
from .models import QRCode
from .serializers import QRCodeSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from accounts.permissions import IsNurseOrReadOnly,IsAdmin,IsNurse,IsParent

# --- Baby Views ---


@permission_classes([IsNurse])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def create_baby(request):
    if request.method == 'POST':
        serializer = BabySerializer(data=request.data)
        if serializer.is_valid():
            new_baby = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --- FacePhoto Views ---
@permission_classes([IsNurse])
@api_view(['POST'])
def upload_face_photo(request):
    if request.method == 'POST':
        serializer = FacePhotoSerializer(data=request.data)
        if serializer.is_valid():
            new_photo = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@permission_classes([IsNurse])
@api_view(['GET'])
def get_all_face_photos(request):
    if request.method == 'GET':
        photos = FacePhoto.objects.all()
        serializer = FacePhotoSerializer(photos, many=True)
        return Response(serializer.data)
    
    
@permission_classes([IsNurse])
@api_view(['GET'])
def get_face_photo(request, photo_id):
    try:
        photo = FacePhoto.objects.get(id=photo_id)
    except FacePhoto.DoesNotExist:
        return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = FacePhotoSerializer(photo)
        return Response(serializer.data)
@permission_classes([IsNurse])
@api_view(['DELETE'])
def delete_face_photo(request, photo_id):
    try:
        photo = FacePhoto.objects.get(id=photo_id)
    except FacePhoto.DoesNotExist:
        return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        photo.delete()
        return Response({"message": "Deleted successfully"})


# --- FootPrint Views ---
@permission_classes([IsNurse])
@api_view(['POST'])
def upload_foot_print(request):
    if request.method == 'POST':
        serializer = FootPrintSerializer(data=request.data)
        if serializer.is_valid():
            new_record = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --- RetinaPrint Views ---
@permission_classes([IsNurse])
@api_view(['POST'])
def upload_retina_print(request):
    if request.method == 'POST':
        serializer = RetinaPrintSerializer(data=request.data)
        if serializer.is_valid():
            new_record = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --- MotherID Views ---
@permission_classes([IsNurse])
@api_view(['POST'])
def upload_mother_id(request):
    if request.method == 'POST':
        serializer = MotherIDSerializer(data=request.data)
        if serializer.is_valid():
            new_id = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --- Mother Views ---
@permission_classes([IsNurse])
@api_view(['POST'])
def create_mother(request):
    if request.method == 'POST':
        serializer = MotherSerializer(data=request.data)
        if serializer.is_valid():
            new_mother = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@permission_classes([IsNurse])
@api_view(['GET'])
def get_all_mothers(request):
    if request.method == 'GET':
        mothers = Mother.objects.all()
        serializer = MotherSerializer(mothers, many=True)
        return Response(serializer.data)
    
@permission_classes([IsNurse])
@api_view(['GET'])
def get_mother_by_id(request, pk):
    try:
        mother = Mother.objects.get(pk=pk)
    except Mother.DoesNotExist:
        return Response({"message": "Mother not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MotherSerializer(mother)
        return Response(serializer.data)
    
    
@permission_classes([IsNurse])
@api_view(['PUT'])
def update_mother(request, pk):
    try:
        mother = Mother.objects.get(pk=pk)
    except Mother.DoesNotExist:
        return Response({"message": "Mother not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = MotherSerializer(mother, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@permission_classes([IsNurse])
@api_view(['DELETE'])
def delete_mother(request, pk):
    try:
        mother = Mother.objects.get(pk=pk)
    except Mother.DoesNotExist:
        return Response({"message": "Mother not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        mother.delete()
        return Response({"message": "Mother deleted"}, status=status.HTTP_204_NO_CONTENT)


# --- Nurse Views ---
@permission_classes([IsNurse])
@api_view(['POST'])
def create_nurse(request):
    if request.method == 'POST':
        serializer = NurseSerializer(data=request.data)
        if serializer.is_valid():
            nurse = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@permission_classes([IsNurse])
@api_view(['GET'])
def get_all_nurses(request):
    if request.method == 'GET':
        nurses = Nurse.objects.all()
        serializer = NurseSerializer(nurses, many=True)
        return Response(serializer.data)
    
@permission_classes([IsNurse])
@api_view(['PATCH'])
def approve_nurse(request, pk):
    try:
        nurse = Nurse.objects.get(pk=pk)
    except Nurse.DoesNotExist:
        return Response({"message": "Nurse not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        nurse.approved = True
        nurse.save()
        serializer = NurseSerializer(nurse)
        return Response(serializer.data)
    
@permission_classes([IsNurse])
@api_view(['DELETE'])
def delete_nurse(request, pk):
    try:
        nurse = Nurse.objects.get(pk=pk)
    except Nurse.DoesNotExist:
        return Response({"message": "Nurse not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        nurse.delete()
        return Response({"message": "Nurse deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# --- Parent Views ---
@permission_classes([IsNurse])
@api_view(['POST'])
def create_parent(request):
    if request.method == 'POST':
        serializer = ParentSerializer(data=request.data)
        if serializer.is_valid():
            parent = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@permission_classes([IsNurse])
@api_view(['GET'])
def get_all_parents(request):
    if request.method == 'GET':
        parents = Parent.objects.all()
        serializer = ParentSerializer(parents, many=True)
        return Response(serializer.data)
    
    
@permission_classes([IsNurse])
@api_view(['GET'])
def get_parent_by_id(request, pk):
    try:
        parent = Parent.objects.get(pk=pk)
    except Parent.DoesNotExist:
        return Response({"error": "Parent not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ParentSerializer(parent)
        return Response(serializer.data)
    
@permission_classes([IsNurse])
@api_view(['PUT'])
def update_parent(request, pk):
    try:
        parent = Parent.objects.get(pk=pk)
    except Parent.DoesNotExist:
        return Response({"error": "Parent not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ParentSerializer(parent, data=request.data)
        if serializer.is_valid():
            updated_parent = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@permission_classes([IsNurse])
@api_view(['DELETE'])
def delete_parent(request, pk):
    try:
        parent = Parent.objects.get(pk=pk)
    except Parent.DoesNotExist:
        return Response({"error": "Parent not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        parent.delete()
        return Response({"message": "Parent profile deleted"}, status=status.HTTP_204_NO_CONTENT)



@permission_classes([IsNurse])
@api_view(['POST'])
def create_qr_code(request):
    serializer = QRCodeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@permission_classes([IsNurse,IsAdmin])
@api_view(['GET'])
def get_all_qr_codes(request):
    qr_codes = QRCode.objects.all()
    serializer = QRCodeSerializer(qr_codes, many=True)
    return Response(serializer.data)

@permission_classes([IsNurse,IsAdmin])
@api_view(['GET'])
def get_qr_code_by_id(request, pk):
    try:
        qr_code = QRCode.objects.get(pk=pk)
    except QRCode.DoesNotExist:
        return Response({"error": "QR Code not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = QRCodeSerializer(qr_code)
    return Response(serializer.data)

@permission_classes([IsNurse])
@api_view(['DELETE'])
def delete_qr_code(request, pk):
    try:
        qr_code = QRCode.objects.get(pk=pk)
    except QRCode.DoesNotExist:
        return Response({"error": "QR Code not found"}, status=status.HTTP_404_NOT_FOUND)

    qr_code.delete()
    return Response({"message": "QR Code deleted"}, status=status.HTTP_204_NO_CONTENT)
