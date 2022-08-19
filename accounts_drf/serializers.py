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
    class Meta:
        model = Answer
        fields = ['body','id', 'created_at', 'likes_count']
        read_only_fields = [
            'created_at',
            'id',
            'likes_count'
        ]

class AnswererListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'birth_date', 'town', 'answer_count']
        read_only_fields = ['answer_count']

class AnswerDetailSerializer(serializers.ModelSerializer):
    # question = serializers.SlugRelatedField(
    #     many=True, read_only=True, slug_field='body'
    # )
    # author = serializers.StringRelatedField(
    #     many=True
    # )
    class Meta:
        model = Answer
        fields = [ 'id', 'body', 
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