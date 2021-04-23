from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from accounts.models import Society, ValidVisitor
from .serializers import RegistrationSerializer, SocietySerializer, ValidVisitorSerializer

class ObtainAuthTokenView(APIView):

	authentication_classes = []
	permission_classes = []

	def post(self, request):
		context = {}
        
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user:
			try:
				token = Token.objects.get(user=user)
			except Token.DoesNotExist:
				token = Token.objects.create(user=user)
			context['response'] = 'Successfully authenticated.'
			context['pk'] = user.id
			context['username'] = username
			context['token'] = token.key
		else:
			context['response'] = 'Error'
			context['error_message'] = 'Invalid credentials'

		return Response(context)

@api_view(['POST', ])
def register_view(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        user = serializer.save()
        data['response'] = 'User registration Success.'
        data['username'] = user.username
        data['email'] = user.email
        token = Token.objects.get(user=user).key
        data['token'] = token
    else:
        data = serializer.errors
    return Response(data)


@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def api_society_detail_view(request, pk):
    try:
        society = Society.objects.get(id=pk)
    except Society.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = SocietySerializer(society)
    return Response(serializer.data)


@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def api_visitor_detail_view(request, name):
    try:
        vistor = ValidVisitor.objects.get(name__contains=name)
    except ValidVisitor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = ValidVisitorSerializer(vistor)
    return Response(serializer.data)


@api_view(['POST', ])
@permission_classes([IsAuthenticated])
def api_add_visitor_view(request):
    user = request.user

    society = Society.objects.get(user=user)
    visitor = ValidVisitor(soc_name_id=society.id)
    serializer = ValidVisitorSerializer(visitor, data=request.data)
    data = {}
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)