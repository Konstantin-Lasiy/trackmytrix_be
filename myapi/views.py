from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, permissions
from rest_framework.response import Response
from .models import DailyWeight
from .serializers import WeightEntrySerializer

@api_view(['GET'])
def hello_world(request):   
    return Response({'message': 'Greetings from your backend (   )(   ) !'})

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def weight_entries(request):
    if request.method == 'GET':
        entries = DailyWeight.objects.filter(user=request.user)
        serializer = WeightEntrySerializer(entries, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = WeightEntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Set the user to the current user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def weight_entry_detail(request, pk) -> Response | None:
    try:
        entry = DailyWeight.objects.get(pk=pk, user=request.user)
    except DailyWeight.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = WeightEntrySerializer(entry)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = WeightEntrySerializer(entry, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)