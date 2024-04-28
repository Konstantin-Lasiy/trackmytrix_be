from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from .models import TrickInstance, Run, TrickDefinition
from .serializers import TrickDefinitionSerializer, RunSerializer
from django.http import JsonResponse
from django.utils import timezone


@api_view(["GET"])
def hello_world(request):
    return Response({"message": "Greetings from your backend (   )(   ) !"})


class TrickDefinitionList(generics.ListCreateAPIView):
    queryset = TrickDefinition.objects.all()
    serializer_class = TrickDefinitionSerializer

class TrickDefinitionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=TrickDefinition.objects.all()
    serializer_class = TrickDefinitionSerializer

class RunList(generics.ListCreateAPIView):
    queryset = Run.objects.all()
    serializer_class = RunSerializer

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
        print(tricks_data)
        for trick_data in tricks_data:
            # Create or update the Trick instance
            TrickInstance.objects.create(
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
