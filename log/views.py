from auditlog.models import LogEntry
from rest_framework import generics
from rest_framework.viewsets import ReadOnlyModelViewSet

from log.filters import AccessLogFilter
from log.models import AccessLog
from log.serializers import AccessLogSerializer, LogEntrySerializer


class AccessLogListView(generics.ListAPIView):
    queryset = AccessLog.objects.all()
    serializer_class = AccessLogSerializer


class AccessLogDetailView(generics.RetrieveAPIView):
    queryset = AccessLog.objects.all()
    serializer_class = AccessLogSerializer


class UserActivityViewSet(ReadOnlyModelViewSet):
    serializer_class = AccessLogSerializer
    filterset_class = AccessLogFilter

    def get_queryset(self):
        return AccessLog.objects.all()


class UserActivityChangesViewSet(ReadOnlyModelViewSet):
    serializer_class = LogEntrySerializer

    def get_queryset(self):
        return LogEntry.objects.all()
