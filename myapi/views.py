from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from django.db import transaction
from .models import TrickInstance, Run, TrickDefinition, LastUsedTricks
from .serializers import (
    TrickDefinitionSerializer,
    RunSerializer,
    LastUsedTricksSerializer,
)
from myapi.permissions import IsOwnerOrReadOnly
from django.http import JsonResponse
from django.utils import timezone


@api_view(["GET"])
def hello_world(request):
    return Response({"message": "Greetings from your backend (   )(   ) !"})


class TrickDefinitionList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = TrickDefinition.objects.all()
    serializer_class = TrickDefinitionSerializer

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {"request": self.request}


class TrickDefinitionDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = TrickDefinition.objects.all()
    serializer_class = TrickDefinitionSerializer


class RunList(generics.ListCreateAPIView):
    serializer_class = RunSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        """
        This view should return a list of all the runs
        for the currently authenticated user.
        """
        user = self.request.user
        return Run.objects.filter(user=user)


class RunDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Run.objects.all()
    serializer_class = RunSerializer


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def upload_run(request):
    try:
        data = request.data  # Load data from request body
        with transaction.atomic():
            run = Run.objects.create(
                user=request.user,
                date=timezone.now().date(),
                time=timezone.now().time(),
                wing=data.get("wing", None),
                site=data.get("site", None),
            )
            tricks_data = data["filteredTricks"]
            last_used_tricks_list = []

            for trick_data in tricks_data:
                trick_definition = TrickDefinition.objects.get(id=trick_data["id"])
                TrickInstance.objects.create(
                    run=run,
                    trick_definition=trick_definition,
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

                # Update LastUsedTricks for each trick
                last_used_trick, created = LastUsedTricks.objects.update_or_create(
                    user=request.user,
                    trick=trick_definition,
                    defaults={"last_used": timezone.now()},
                )
                last_used_tricks_list.append(last_used_trick)
            last_used_tricks_serializer = LastUsedTricksSerializer(
                last_used_tricks_list, many=True
            )

        return JsonResponse(
            {
                "status": "success",
                "run_id": run.pk,
                "message": "Tricks uploaded successfully",
                "last_used_tricks": last_used_tricks_serializer.data,
            },
            status=200,
        )
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)


class LastUsedTricksList(generics.GenericAPIView):
    serializer_class = LastUsedTricksSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get(self, request, *args, **kwargs):
        last_used_tricks = LastUsedTricks.objects.filter(user=request.user).order_by(
            "-last_used"
        )
        serializer = LastUsedTricksSerializer(last_used_tricks, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        tricks = request.data.get("tricks")
        if not tricks:
            return Response({"error": "Trick ID is required"}, status=400)

        results = []
        for trick in tricks:
            trick_id = trick.get("trick_id")
            last_used = trick.get("last_used")

            if not trick_id or not last_used:
                continue  # Skip improperly formatted entries

            # Find or create the trick definition (assuming it should exist)
            trick_instance, _ = TrickDefinition.objects.get_or_create(id=trick_id)

            # Update or create the LastUsedTricks record
            last_used_trick, created = LastUsedTricks.objects.update_or_create(
                user=request.user,
                trick=trick_instance,
                defaults={"last_used": last_used},
            )

            # Serialize each updated or created instance
            serializer = LastUsedTricksSerializer(last_used_trick)
            results.append(serializer.data)

        return Response(results, status=status.HTTP_200_OK)
