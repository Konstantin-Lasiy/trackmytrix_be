from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, permissions
from rest_framework.response import Response
from .models import TrickInstance, Run, TrickDefinition
from .serializers import TrickDefinitionSerializer
from django.http import JsonResponse
from django.utils import timezone


@api_view(["GET"])
def hello_world(request):
    return Response({"message": "Greetings from your backend (   )(   ) !"})


@api_view(["GET"])
def get_trick_definitions(request):
    trick_definitions = TrickDefinition.objects.all()
    serializer = TrickDefinitionSerializer(trick_definitions, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def upload_run(request):
    try:
        data = request.data  # Load data from request body
        run = Run.objects.create(
            user=request.user,
            date=timezone.now().date(),
            time=timezone.now().time(),
            wing=data.get("wing", None),
            site=data.get("site", None),
        )
        tricks_data = data["filteredTricks"]
        for trick_data in tricks_data:
            # Create or update the Trick instance
            TrickInstance.objects.update_or_create(
                run=run,
                trick_definition_id=trick_data["id"],
                successful=trick_data.get("successful"),
                right=trick_data.get("right", None),
                reverse=trick_data.get("reverse", None),
                twisted=trick_data.get("twisted", None),
                twisted_exit=trick_data.get("twisted_exit", None),
                flipped=trick_data.get("flipped", None),
                double_flipped=trick_data.get("double_flipped", None),
                devil_twist=trick_data.get("devil_twist", None),
                cab_slide=trick_data.get("cab_slide", None),
            )

        return JsonResponse(
            {"status": "success", "message": "Tricks uploaded successfully"}, status=200
        )
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)


# @api_view(['GET', 'POST'])
# @permission_classes([permissions.IsAuthenticated])
# def weight_entries(request):
#     if request.method == 'GET':
#         entries = DailyWeight.objects.filter(user=request.user)
#         serializer = WeightEntrySerializer(entries, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = WeightEntrySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)  # Set the user to the current user
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# @permission_classes([permissions.IsAuthenticated])
# def weight_entry_detail(request, pk) -> Response | None:
#     try:
#         entry = DailyWeight.objects.get(pk=pk, user=request.user)
#     except DailyWeight.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = WeightEntrySerializer(entry)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = WeightEntrySerializer(entry, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         entry.delete()
# return Response(status=status.HTTP_204_NO_CONTENT)
