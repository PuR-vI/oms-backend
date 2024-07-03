from rest_framework.views import APIView
from .serializers import UserSerializer
from django.http.response import JsonResponse, Http404
from .models import User
from rest_framework.response import Response

class UserView(APIView):

    def get_user(self, pk):
        try:
            user = User.objects.get(userId=pk)
            return user
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        if pk:
            data = self.get_user(pk)
            serializer = UserSerializer(data)
        else:
            data = User.objects.all()
            serializer = UserSerializer(data, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        data = request.data
        employee_id = data.get('employeeId')
        serializer = UserSerializer(data=data)

        if User.objects.filter(employeeId=employee_id).exists():
           return JsonResponse("User with this Employee ID already exists", safe=False)

        serializer = UserSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse("User Created Successfully", safe=False)
        return JsonResponse("Failed to Add User", safe=False)
    
    def put(self,request,pk=None):
        User_to_update= User.objects.get(userId=pk)
        serializer = UserSerializer(instance=User_to_update,data=request.data,partial=True)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse("User Saved Successfully",safe=False)
        return JsonResponse("Failed to Update User")
    
    def delete(self,request,pk=None):
        User_to_delete=User.objects.get(userId=pk)
        User_to_delete.delete()
        return JsonResponse("User Deleted Successfully",safe=False)
