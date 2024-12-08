from rest_framework import serializers
from .models import Session, Question, AnswerOption, Answer

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'name', 'created_at']

class QuestionSerializer(serializers.ModelSerializer):
    options = serializers.StringRelatedField(many=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'category', 'options']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['session', 'question', 'response']
