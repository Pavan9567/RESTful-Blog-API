from django.shortcuts import render
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import PostSerializer, CommentSerializer, RegisterSerializer, LoginSerializer, UserSerializer
from .models import Post, Comment
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView,CreateAPIView
from rest_framework.permissions import AllowAny, BasePermission, SAFE_METHODS
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate

# Create your views here.

#Authentication view
class IsAuthenticatedForUnsafeMethods(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated
    
#Register View
class Register(CreateAPIView):
    queryset = User.objects.all()
    permission_classes=[AllowAny]
    serializer_class = RegisterSerializer
    
#Login View
class Login(CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request,*args,**kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username,password=password)


        if user is not None:
            refresh = RefreshToken.for_user(user)
            user_serializer = UserSerializer(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user_serializer.data
            })
        else:
            return Response({'detail':'Invalid Credentials'})

#Posts Get and Post View
class PostListCreate(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedForUnsafeMethods]
    authentication_classes = [JWTAuthentication]

    def perform_create(self,serializer):
        serializer.save()

#Posts Get, Update, Delete View
class PostRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedForUnsafeMethods]
    authentication_classes = [JWTAuthentication]

#Comments Get and Post View
class CommentListCreate(ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedForUnsafeMethods]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        post_id = self.request.query_params.get('post_id')

        if post_id:
            return Comment.objects.filter(post_id=post_id)
    
    def perform_create(self, serializer):
        serializer.save()
        
#Comments Get, Update, Delete View
class CommentRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedForUnsafeMethods]
    authentication_classes = [JWTAuthentication]

