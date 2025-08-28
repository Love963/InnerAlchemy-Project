from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import SoulNote
from .serializers import SoulNoteSerializer

# Create your views here.
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class SoulNoteViewSet(viewsets.ModelViewSet):
    serializer_class = SoulNoteSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # allow filtering & searching
    filterset_fields = ["mood", "is_private", "solfeggio_frequency"]
    search_fields = ["title", "content", "tags"]
    ordering_fields = ["date_created", "updated_at"]

    def get_queryset(self):
        # Users only see their own notes, 
        # unless explicitly shared/public in future versions.
        return SoulNote.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"], url_path="recent")
    def recent_notes(self, request):
        notes = self.get_queryset().order_by("-date_created")[:5]
        serializer = self.get_serializer(notes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="mood/(?P<mood>[^/.]+)")
    def notes_by_mood(self, request, mood=None):
        notes = self.get_queryset().filter(mood=mood)
        serializer = self.get_serializer(notes, many=True)
        return Response(serializer.data)
