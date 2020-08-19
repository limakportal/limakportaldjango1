from .models import Authority
from .serializer import AuthoritySerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class AuthorityAPIView(APIView):
    def get(self,request):
        authorities = Authority.objects.all().order_by('id')
        serializer = AuthoritySerializer(authorities,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = AuthoritySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AuthorityDetails(APIView):

    def get_object(self,id):
        try:
            return Authority.objects.get(id=id)
        except Authority.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        authority = self.get_object(id)
        serializer = AuthoritySerializer(authority)
        return Response(serializer.data)


    def put(self, request,id):
        authority = self.get_object(id)
        serializer = AuthoritySerializer(authority, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        authority = self.get_object(id)
        authority.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
