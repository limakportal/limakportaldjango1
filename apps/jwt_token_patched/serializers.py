from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from ..person.models import Person
from ..userrole.models import UserRole
from ..authority.models import Authority
from ..permission.models import Permission

from ..permission.serializer import PermissionSerializer

from ..businessrules.views import IsManager

class TokenObtainPairPatchedSerializer(TokenObtainPairSerializer):
     def to_representation(self, instance):
         r = super(TokenObtainPairPatchedSerializer, self).to_representation(instance)
         r.update({'user': self.user.username})
         return r

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # The default result (access/refresh tokens)
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        # Custom data you want to include

        # data.update({'email': self.user.email})
        # data.update({'id': self.user.id})

        request = {}
        userRequest = {}
        userRequest['id'] = self.user.id
        userRequest['Email'] = self.user.email
        request['User'] = userRequest       
        try:
            person = Person.objects.get(Email = self.user.email)
            personRequest = {}
            personRequest['id'] = person.id
            personRequest['Name'] = person.Name
            personRequest['Surname'] = person.Surname
            request['Person'] = personRequest
        except :
            request['Person'] = None
        permissionRequest = {}
        allPermissions = []
        userRoles = UserRole.objects.filter(Account_id = self.user.id)
        for userRole in userRoles:
            authorityes = Authority.objects.filter(Role_id = userRole.Role_id , Active = True)
            for authority in authorityes:
                permissions = Permission.objects.filter(id = authority.Permission_id)
                for permission in permissions:
                    allPermissions.append(permission);    

        request['permissions'] = PermissionSerializer(allPermissions, many=True).data
        if request['Person'] != None:
            request['IsManager'] = IsManager(person.id)
        else:
            request['IsManager'] = None

        data.update(request)
        # data.update({'Person': responsePerson})
        # and everything else you want to send in the response
        return data