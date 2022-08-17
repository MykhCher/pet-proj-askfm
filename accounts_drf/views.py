from askfm.settings import AUTH_USER_MODEL
from core.models import Answer, Comment
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import CommentSerializer, AnswerSerializer

User = AUTH_USER_MODEL

class AnswerGet(ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
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
            serializer.save()
        return Response(serializer.data)