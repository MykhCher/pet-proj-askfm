from core.models import Answer, Comment, Question
from django.http import Http404, JsonResponse
from accounts.models import User
from rest_framework import status, filters
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import (CommentSerializer,
                          AnswerListSerializer,
                          AnswerDetailSerializer,
                          AnswererListSerializer, 
                          ProfileSerializer,
                          QuestionCreateSerializer)

class EnablePartialUpdateMixin:
    """Enable partial updates
        
    Override partial kwargs in UpdateModelMixin class,
    parental for viewsets.ModelViewSet class
    """
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

class AnswererList(EnablePartialUpdateMixin, ModelViewSet, ):
    queryset = User.objects.all().exclude(answer__isnull=True)
    serializer_class = AnswererListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.SearchFilter, )
    search_fields = ['first_name', 'last_name']
      
class ProfileView(ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = User.objects.filter()
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return self.retrieve(request, self.request.user.pk)

    def retrieve(self, request, pk):
        if not self.request.user.pk:
            return Response(status=status.HTTP_403_FORBIDDEN, data={
                "status": "403_FORBIDDEN",
                "message": "User id does't match"
            })
        user = self.queryset.get(pk=pk)
        serializer = self.serializer_class(user)
        return Response(serializer.data)
    
    def create(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED,
                        data={
                            "status": "405_METHOD_NOT_ALLOWED",
                            "message": "Cannot provide method 'post'"
                        })

    def update(self, request, pk=None):
        if not self.request.user.pk:
            return Response(status=status.HTTP_403_FORBIDDEN, data={
                "status": "403 FORBIDDEN",
                "message": "User id does't match"
            })
        if not pk:
            pk = self.request.user.pk
        profile = User.objects.get(pk=pk)
        data = self.request.data
        if profile.pk == request.user.pk:
            profile.first_name=data.get('first_name')
            profile.last_name=data.get('last_name')
            profile.birth_date=data.get('birth_date')
            profile.town=data.get('town')
            if not profile.first_name or \
            not profile.last_name or \
            not profile.town or \
            not profile.birth_date:
             return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={
                    "status": "403_FORBIDDEN",
                    "message": "Expected all data provided."
                }
            )
            serializer = self.serializer_class(profile, data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN,
                            data={
                                'status': '403_FORBIDDEN',
                                'message': 'You have no permission on this action'
                                })  

    
    def partial_update(self, request, pk):
        if not self.request.user.pk:
            return Response(status=status.HTTP_403_FORBIDDEN, data={
                "status": "403 FORBIDDEN",
                "message": "User id does't match"
            })
        if not pk:
            pk = self.request.user.pk
        profile = User.objects.get(pk=pk)
        data=request.data
        if profile.pk == request.user.pk:
            profile.first_name=data.get('first_name', profile.first_name)
            profile.last_name=data.get('last_name', profile.last_name)
            profile.birth_date=data.get('birth_date', profile.birth_date)
            profile.town=data.get('town', profile.town)
            profile.save()
            
            serializer = self.serializer_class(profile)

            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN,
                            data={
                                'status': '403_FORBIDDEN',
                                'message': 'You have no permission on this action'
                                })


class AnswerDetail(APIView):
    def get_object(self, pk):
        try:
            return Answer.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, pk ,format=None):
        answer = Answer.objects.get(pk=pk)
        serializer = AnswerDetailSerializer(answer)
        return Response(serializer.data)

class AnswerGet(ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.SearchFilter, )
    search_fields = ['author__first_name', 'author__last_name']

    # def list(self, request, format=None):
    #     pass

    def retrieve(self, request, pk ,format=None):
        answer = Answer.objects.get(pk=pk)
        serializer = AnswerDetailSerializer(answer)
        return Response(serializer.data)
    
    def create(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(methods=['post'], detail=True)
    def make_like(self, request, pk=None):
        answer = self.get_object()
        if answer.likes.filter(id=request.user.id).exists():
            answer.likes.remove(request.user)
        else:
            answer.likes.add(request.user)
            answer.save()
        serializer = AnswerDetailSerializer(answer)
        return Response(serializer.data)
    
    @action(methods=['post'], detail=True)
    def make_comment(self, request, pk=None):
        serializer = CommentSerializer(data=request.data, context={'request': request.user, 'pk': self.get_object().pk})
        if serializer.is_valid():
            serializer.save(author=serializer.context['request'], answer_id=serializer.context['pk'])
        return Response(serializer.data)

class QuestionCreateView(CreateAPIView):
    serializer_class = QuestionCreateSerializer
    queryset = Question.objects.all()
    permission_classes = [IsAuthenticated, ]

    def create(self, request, pk):
        question = self.get_object()
        data = request.data
        if self.request.user.pk != pk:
            question.author = User.objects.get(pk=self.request.user.pk)
            question.body = data['body']
            question.id = Question.objects.all().count() + 1
            question.addressant = User.objects.get(pk=pk)
            serializer = self.serializer_class(question, data)
            serializer.is_valid()
            serializer.save()
        else:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={
                    'status': '403_FORBIDDEN',
                    'message': "Cannot create a question to yourself"
                    
                }
            )
        return Response(serializer.data)
