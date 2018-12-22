from rest_framework import viewsets, status
from rest_framework.views import APIView, Response
from .models import Panel, OneHourElectricity
from .serializers import PanelSerializer, OneHourElectricitySerializer
from django.db.models.functions import TruncDay
from django.db.models import Sum, Avg, Max, Min


class PanelViewSet(viewsets.ModelViewSet):
    serializer_class = PanelSerializer
    queryset = Panel.objects.all()


class HourAnalyticsView(APIView):
    serializer_class = OneHourElectricitySerializer

    def get(self, request,  panelid):
        panelid = int(self.kwargs.get('panelid', 0))
        queryset = OneHourElectricity.objects.filter(panel_id=panelid)
        items = OneHourElectricitySerializer(queryset, many=True)
        return Response(items.data)

    def post(self, request, panelid):
        serializer = OneHourElectricitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DayAnalyticsView(APIView):
    def get(self, request, panelid):
        panelid = int(self.kwargs.get('panelid', 0))
        result = OneHourElectricity.objects \
            .filter(panel_id=panelid) \
            .annotate(date=TruncDay('date_time')) \
            .values('date') \
            .annotate(sum=Sum('kilo_watt')) \
            .annotate(average=Avg('kilo_watt')) \
            .annotate(maximum=Max('kilo_watt')) \
            .annotate(minimum=Min('kilo_watt')) \
            .values('date', 'sum', 'average', 'maximum', 'minimum') \
            .order_by('date')

        return Response(result)
