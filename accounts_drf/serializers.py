from rest_framework import serializers
from accounts.models import User
from core.models import Comment, Answer, Question

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {
            'password' : {'write_only': True}
        }
class AnswerListSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        many=False, read_only=True
    )
    question = serializers.SlugRelatedField(
         many=False, read_only=True, slug_field='body'
     )
    
    class Meta:
        model = Answer
        fields = ['question', 'body', 'author']

class AnswererListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'birth_date', 'town', 'answer_count']
        read_only_fields = ['answer_count']

class AnswerDetailSerializer(serializers.ModelSerializer):
    question = serializers.SlugRelatedField(
         many=False, read_only=True, slug_field='body'
     )
    comments = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='body'
    )
    author = serializers.StringRelatedField(
        many=False, read_only=True
    )
    class Meta:
        model = Answer
        fields = [ 'id', 'author', 'question', 'body', 'comments',
                 'comments_count', 'likes_count']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields=['body']

        def create(self, validated_data):
            author=self.context['request']
            answer_id = self.context['pk']
            body = validated_data['body']
            comment = Comment(author=author, answer_id=answer_id, body=body)
            comment.save()
            return validated_data

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'birth_date', 'town']
        read_only_fields = ['first_name', 'last_name', 'birth_date', 'town']

class QuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Question
        fields = ['body', 'id']