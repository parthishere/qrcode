from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.decorators import api_view


from .models import DatePrice, OfflineModel, VirtualModel
# Create your views here.

# class OfflineModelListCreateAPIView(ListCreateAPIView):
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer
#     permission_classes = [IsAuthenticated,]
#     lookup_field = ['pk']
#     lookup_url_kwarg = ['pk']
    
#     def perform_create(self, serializer):
#         serializer.save(created_by=self.request.user)
    
#     def list(self, request):
#         queryset = self.get_queryset().filter(created_by=request.user).exclude(removed=True)
#         serializer = EventSerializer(queryset, many=True)
#         return Response(serializer.data)