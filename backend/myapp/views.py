from rest_framework.viewsets import ModelViewSet
from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer
from django.http import HttpResponse

def index(request):
    return HttpResponse("Termômetro de Relacionamentos!")

class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class AnswerViewSet(ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
