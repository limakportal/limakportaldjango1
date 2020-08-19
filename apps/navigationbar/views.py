from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import NavigationBar
from .serializer import NavigationBarSerializer , NavigationBarItemsSerializer

class NavigationBarAPIView(APIView):
    def get(self,request):
        navigationBar = NavigationBar.objects.all().order_by('id')
        serializer = NavigationBarItemsSerializer(navigationBar , many = True)
        return Response(serializer.data)

    def post(self,request):
        serializer = NavigationBarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data ,status=status.HTTP_201_CREATED)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

class NavigationBarDetails(APIView):
    def get_object(self,obj):
        try:
            return NavigationBar.objects.get(id=id)
        except NavigationBar.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        navigationBar = self.get_object(id)
        serializer = NavigationBarSerializer(navigationBar)
        return Response(serializer.data)

    def put(self, request,id):
        navigationBar = self.get_object(id)
        serializer = NavigationBarSerializer(navigationBar, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        navigationBar = self.get_object(id)
        navigationBar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

