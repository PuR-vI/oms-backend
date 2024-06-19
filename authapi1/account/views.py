from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from account.serializers import UserChangePasswordSerializer, UserRegistrationSerializer,UserLoginSerializer,UserProfileSerializer
from account.renderers import UserRenderer


#Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)

  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

class UserRegistrationView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            token=get_tokens_for_user(user) 
            return Response ({'token':token,'msg':'Registration Successful'},
            status=status.HTTP_201_CREATED)
        return Response (serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
           email=serializer.data.get('email')
           password=serializer.data.get('password')
           user=authenticate(email=email,password=password)
           if user is not None:
               token=get_tokens_for_user(user)
               return Response({'token':token,'msg':'Login Success'},status=status.HTTP_200_OK)
           else:
               return Response({'errors':{'non_field_errors':['Email or Password is not valid']}},status=status.HTTP_404_NOT_FOUND)  

class UserLogoutView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTTokenUserAuthentication,)

    def post(self, request):
        try:
            # Extract refresh token from request
            refresh_token = request.data.get("refresh", None)

            if not refresh_token:
                return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

            # Blacklist refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()

            # Return a success response with a message
            return Response({"detail": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"detail": "Token is invalid or expired."}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
        serializer=UserProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class UserChangePasswordView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
       serializer=UserChangePasswordSerializer(data=request.data,context={'user':request.user})
       if serializer.is_valid(raise_exception=True):
        return Response({'msg':'Password Changed Successfully'},status=status.HTTP_200_OK)
       return Response(serializer.errors,status==status.HTTP_400_BAD_REQUEST)
