from rest_framework.response import Response
from rest_framework.views import APIView
from fest.models import FestModel
from .serializers import FestSerializer
from rest_framework import status
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateDestroyAPIView

class FestListCreateListAPI(APIView):
    queryset = FestModel.objects.all()
    serializer_class = FestSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['recognized', 'sent_email', "created_by"]
    search_fields = ["user__username", 'name', 'phone_number', 'unique_id', "name"]
    ordering_fields = ['name', 'name', "unique_id"]
    
    def get_queryset(self):
        queryset = FestModel.objects.all()

        # Apply the filters
        queryset = self.filter_queryset(queryset)

        # Apply ordering
        queryset = self.order_queryset(queryset)

        return queryset

    def filter_queryset(self, queryset):
        for backend in self.filter_backends:
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def order_queryset(self, queryset):
        ordering = self.request.query_params.get('ordering', None)
        if ordering:
            fields = [field.strip() for field in ordering.split(',')]
            return queryset.order_by(*fields)
        return queryset
    
    def get(self, request, org_name):
        queryset = self.get_queryset().filter(created_by__username=org_name)

        # Perform search if search query parameter is provided
        search_query = request.query_params.get('search', None)
        if search_query:
            search_backend = filters.SearchFilter()
            queryset = search_backend.filter_queryset(request, queryset, self)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request, org_name):
        serializer = self.serializer_class(data=request.data)
        user = request.user
        fest = FestModel.objects.prefetch_related("created_by").get(pk=org_name)
        if serializer.is_valid() and fest.created_by == user:
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class EventRetriveUpdateAPIView(RetrieveUpdateDestroyAPIView):
    queryset = FestModel.objects.all()
    serializer_class = FestSerializer
    permission_classes = [IsAuthenticated]
    lookup_field= "pk"
    
    
    def perform_update(self, serializer):
        if self.request.user == serializer.created_by:
            instance = serializer.save(created_by=self.request.user)
        
    def perform_destroy(self, instance):
        if self.request.user == instance.created_by:
            instance.removed = True
            instance.save()