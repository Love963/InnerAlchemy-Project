from django.shortcuts import render
from rest_framework import generics, permissions, viewsets, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from sleep.models import SleepLog
from breathwork.models import BreathworkSession
from gratitude.models import GratitudeEntry
from soulnotes.models import SoulNote
from .serializers import DashboardSerializer, UserActivitySerializer
from .models import UserActivity

from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from .models import SummaryReport
from .serializers import SummaryReportSerializer, SummaryComputeSerializer
from .utils import compute_metrics_for_user, period_bounds
from django.shortcuts import get_object_or_404

# Create your views here.


User = get_user_model()

class UserActivityListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = UserActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserActivity.objects.filter(user=self.request.user).order_by('-timestamp')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DashboardAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DashboardSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        sleep_logs = SleepLog.objects.filter(user=user)
        breathwork_sessions = BreathworkSession.objects.filter(user=user)
        gratitude_entries = GratitudeEntry.objects.filter(user=user)
        soulnotes = SoulNote.objects.filter(user=user)

        data = {
            'user': user,
            'sleep_logs': sleep_logs,
            'breathwork_sessions': breathwork_sessions,
            'gratitude_entries': gratitude_entries,
            'soulnotes': soulnotes,
        }
        serializer = self.serializer_class(data)
        return Response(serializer.data)



class SummaryReportViewSet(viewsets.ModelViewSet):
    serializer_class = SummaryReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SummaryReport.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["post"], url_path="compute", url_name="compute")
    def compute(self, request):
        """
        Compute a summary on-demand. Accepts:
          - period: 'weekly' or 'monthly' (required)
          - start_date: optional date to determine window
          - persist: boolean (default False). If True, store the computed SummaryReport.
        Returns computed metrics and optionally saved object.
        """
        serializer = SummaryComputeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        period = serializer.validated_data["period"]
        start_date = serializer.validated_data.get("start_date")
        persist = serializer.validated_data.get("persist", False)

        # compute metrics
        data = compute_metrics_for_user(request.user, period=period, start_date=start_date)

        if persist:
            # create/update SummaryReport unique by user/period/start/end
            start = data["start_date"]
            end = data["end_date"]
            # create persisted SummaryReport
            rep, created = SummaryReport.objects.update_or_create(
                user=request.user,
                period=period,
                start_date=start,
                end_date=end,
                defaults={"metrics": data["metrics"]},
            )
            out = SummaryReportSerializer(rep, context={"request": request}).data
            return Response(out, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

        # not persisted: return computed payload
        return Response(data, status=status.HTTP_200_OK)

class DashboardAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        period = request.query_params.get("period", "weekly")
        start_date = request.query_params.get("start_date", None)
        if start_date:
            # let utils parse date string when passed (we can rely on serializer but keep simple)
            import datetime
            start_date = datetime.date.fromisoformat(start_date)
        data = compute_metrics_for_user(request.user, period=period, start_date=start_date)
        return Response(data)
