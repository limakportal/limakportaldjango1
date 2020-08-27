from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view , permission_classes


from .serializer import RegistrationSerializer
from rest_framework.authtoken.models import Token


from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.compat import coreapi, coreschema

from rest_framework.schemas import ManualSchema
from rest_framework.views import APIView

from ..person.models import Person
from ..person.serializer import PersonSerializer
from ..userrole.models import UserRole
from ..authority.models import Authority
from ..permission.models import Permission
from ..permission.serializer import PermissionSerializer



@api_view(['POST', ])
# @permission_classes([IsAuthenticated])
def registration_view(request):
	if request.method == 'POST':
		serializer = RegistrationSerializer(data=request.data)
		data = {}
		if serializer.is_valid():
			account = serializer.save()
			data['response'] = 'successfully registered new user.'
			data['email'] = account.email
			data['username'] = account.username
			token = Token.objects.get(user=account).key
			data['token'] = token
		else:
			data = serializer.errors
		return Response(data)

class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer
    if coreapi is not None and coreschema is not None:
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="username",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Username",
                        description="Valid username for authentication",
                    ),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Password",
                        description="Valid password for authentication",
                    ),
                ),
            ],
            encoding="application/json",
        )

    def get_object(self,id):
        try:
            return Person.objects.get(id=id)
        except Person.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    # permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        response = {}
        response['token'] = token.key

        responseUser = {}
        responseUser['id'] = user.id
        responseUser['Email'] = user.email
        response['User'] = responseUser

        try:
            person = Person.objects.get(Email = user.email)
            responsePerson = {}
            responsePerson['id'] = person.id
            responsePerson['Name'] = person.Name
            responsePerson['Surname'] = person.Surname
            response['Person'] = responsePerson
        except :
            response['Person'] = None
            
        requestPermission = {} 
        allPermissions = []
        userRoles = UserRole.objects.filter(Account_id = user.id)
        for userRole in userRoles:
            authorityes = Authority.objects.filter(Role_id = userRole.Role_id , Active = True)
            for authority in authorityes:
                permissions = Permission.objects.filter(id = authority.Permission_id)
                for permission in permissions:
                    allPermissions.append(permission);    
                    requestPermission = serializer.data
        response['permissions'] = PermissionSerializer(allPermissions, many=True).data
        return Response(response)