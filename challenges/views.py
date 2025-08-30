from django.db.models import Count, Sum
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Challenge, ChallengeMembership, ChallengeProgress
from .serializers import ChallengeSerializer, ChallengeProgressSerializer
from .permissions import IsOwnerOrReadOnly

# Create your views here.
class ChallengeViewSet(viewsets.ModelViewSet):
    serializer_class = ChallengeSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        # Show:
        # - public challenges
        # - private challenges created by user
        # - private challenges joined by user
        base = Challenge.objects.all()
        public_qs = base.filter(visibility="public")
        created_qs = base.filter(created_by=user)
        joined_qs = base.filter(memberships__user=user, memberships__status="joined")
        return (public_qs | created_qs | joined_qs).distinct()

    @action(methods=["post"], detail=True, url_path="join")
    def join(self, request, pk=None):
        challenge = self.get_object()
        membership, created = ChallengeMembership.objects.get_or_create(
            challenge=challenge, user=request.user,
            defaults={"status": "joined"}
        )
        if not created and membership.status == "joined":
            return Response({"detail": "Already joined."}, status=status.HTTP_200_OK)
        membership.status = "joined"
        membership.left_at = None
        membership.save()
        return Response({"detail": "Joined the challenge."}, status=status.HTTP_200_OK)

    @action(methods=["post"], detail=True, url_path="leave")
    def leave(self, request, pk=None):
        challenge = self.get_object()
        try:
            membership = ChallengeMembership.objects.get(challenge=challenge, user=request.user)
        except ChallengeMembership.DoesNotExist:
            return Response({"detail": "Not a participant."}, status=status.HTTP_400_BAD_REQUEST)
        membership.status = "left"
        membership.left_at = timezone.now()
        membership.save()
        return Response({"detail": "Left the challenge."}, status=status.HTTP_200_OK)

    @action(methods=["get"], detail=True, url_path="leaderboard")
    def leaderboard(self, request, pk=None):
        # Simple leaderboard by sum of `value` across progress entries.
        # For streak challenges, users can log value=1 per day they complete.
        challenge = self.get_object()
        qs = (
            ChallengeProgress.objects
            .filter(challenge=challenge)
            .values("user__id", "user__username")
            .annotate(total=Sum("value"))
            .order_by("-total")
        )
        # total can be None if no values—normalize
        data = [
            {"user_id": row["user__id"], "username": row["user__username"], "total": row["total"] or 0}
            for row in qs
        ]
        return Response(data, status=status.HTTP_200_OK)


class ChallengeProgressViewSet(viewsets.ModelViewSet):
    serializer_class = ChallengeProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = ChallengeProgress.objects.filter(user=self.request.user)
        challenge_id = self.request.query_params.get("challenge")
        if challenge_id:
            qs = qs.filter(challenge_id=challenge_id)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
