from core.models import Answer, Comment
from django.http import Http404, JsonResponse
from accounts.models import User
from rest_framework import status 
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import CommentSerializer, AnswerListSerializer, AnswerDetailSerializer, AnswererListSerializer

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

    def partial_update(self, request, pk, *args, **kwargs):
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
            return Response(status=status.HTTP_403_FORBIDDEN, data={'content': 'no permission'})
       

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
    
    @action(methods=['post'], detail=True)
    def make_like(self, request, pk=None):
        answer = self.get_object()
        if answer.likes.filter(id=request.user.id).exists():
            answer.likes.remove(request.user)
        else:
            answer.likes.add(request.user)
            answer.save()
        serializer = self.get_serializer(answer)
        return Response(serializer.data)
    
    @action(methods=['post'], detail=True)
    def make_comment(self, request, pk=None):
        serializer = CommentSerializer(data=request.data, context={'request': request.user, 'pk': self.get_object().pk})
        if serializer.is_valid():
            serializer.save(author=serializer.context['request'], answer_id=serializer.context['pk'])
        return Response(serializer.data)