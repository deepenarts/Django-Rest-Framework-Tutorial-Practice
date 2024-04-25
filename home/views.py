from rest_framework.decorators import api_view
from rest_framework.response import Response
from home.serializers import PeopleSerializer, LoginSerializer, RegisterSerializer
from home.models import Person
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.core.paginator import Paginator
from rest_framework.decorators import action



class RegisterAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)

        if not serializer.is_valid():
            return Response({'status':False, 'message': serializer.errors}, status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'status':True, 'message': 'user created successfully'}, status.HTTP_201_CREATED)


class LoginAPI(APIView):
    def post(self, request):
        data= request.data
        serializer= LoginSerializer(data=data)
        
        if not serializer.is_valid():
            return Response({'status':False, 'message': serializer.errors}, status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=serializer.data['username'], password= serializer.data['password'])

        if not user:
            return Response({'status':False, 'message': 'invalid credentials'}, status.HTTP_400_BAD_REQUEST)
        
        token,_ = Token.objects.get_or_create(user=user)
        return Response({'status':True, 'message': 'User Loged in', 'token':str(token)}, status.HTTP_201_CREATED)




@api_view(['GET','POST','PUT'])
def index(request):
    coursers={
        'course_name': 'python',
        'learn': ['flask', 'Django', 'Tornado','fastapi'],
        'course_Provider': 'Scaler'
    }
    if request.method == "GET":
        data = request.GET.get('search')
        print(data)
        print("You hit the Get method")
        return Response(coursers)
    
    elif request.method == "POST":
        data= request.data
        print(data)
        print("You hit the POST method")
        return Response(coursers)
    
    elif request.method == "PUT":
        print("You hit the PUT method")
        return Response(coursers)
    
    return Response(coursers)



@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def person(request):
    if request.method == "GET":
        objs = Person.objects.filter(color__isnull = False)
        serializer = PeopleSerializer(objs, many = True)
        return Response(serializer.data)
    
    elif request.method == "POST":
        data = request.data
        serializer= PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    elif request.method == "PUT":
        data = request.data
        obj = Person.objects.get(id=data['id'])
        serializer = PeopleSerializer(obj, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    elif request.method == "PATCH":
        data= request.data
        obj = Person.objects.get(id= data['id'])
        serializer= PeopleSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    else:
        data= request.data
        obj= Person.objects.get(id=data['id'])
        obj.delete()
        return Response({"message": "Person is deleted!"})
    

@api_view(["POST"])
def login(request):
    data = request.data
    serializer = LoginSerializer(data=data)

    if serializer.is_valid():
        data = serializer.data
        print(data)
        return Response({'message': 'success'})
    
    return Response(serializer.errors)



#Pagination #Permission Authentication
class PersonAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        try:
            objs= Person.objects.all()
            page = request.GET.get('page', 1)
            page_size =3
            paginator = Paginator(objs, page_size)
            serializer = PeopleSerializer(paginator.page(page), many = True)
            return Response(serializer.data)
        
        except Exception as e:
            return Response ({'status': False, 'message': 'invalid page'})

    
    def post(self, request):
        data = request.data
        serializer= PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    def put(self, request):
        data = request.data
        obj = Person.objects.get(id=data['id'])
        serializer = PeopleSerializer(obj, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    def patch(self, request):
        data= request.data
        obj = Person.objects.get(id= data['id'])
        serializer= PeopleSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    def delete(self, request):
        data= request.data
        obj= Person.objects.get(id=data['id'])
        obj.delete()
        return Response({"message": "Person is deleted!"})
    


class PeopleViewSet(viewsets.ModelViewSet):
    serializer_class = PeopleSerializer
    queryset= Person.objects.all()
    
    def list(self, request):
        search = request.GET.get('search')
        queryset= self.queryset
        if search:
            queryset= queryset.filter(name__startswith=search)
            serializer = PeopleSerializer(queryset, many=True)
            return Response({'status':200, 'data': serializer.data})
        
    @action(detail=False, methods=['post'])
    def send_mail_to_person(self, request):
        return Response({
            'status': True,
            'message': 'email sent successfully'
        })
