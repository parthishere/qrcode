# from rest_framework.response import Response
# from rest_framework.generics import ListCreateAPIView,

# class EventListCreateAPI(ListCreateAPIView):
#     queryset = FestModel.objects.all()
#     serializer_class = EventSerializer
#     permission_classes = [IsAuthenticated,]
#     lookup_field = ['pk']
#     lookup_url_kwarg = ['pk']
    
#     def perform_create(self, serializer):
#         serializer.save(created_by=self.request.user)
    
#     def list(self, request):
#         eventqueryset = self.get_queryset().filter(created_by=request.user, fest=None).exclude(removed=True)
#         e_serializer = EventSerializer(eventqueryset, many=True).data
        
#         fest_queryset = FestModel.objects.filter(user=request.user)
#         f_serializer = FestListSerializer(fest_queryset, many=True).data
        
#         return Response({"events": e_serializer, "fest":f_serializer})