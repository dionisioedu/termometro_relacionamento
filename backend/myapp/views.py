from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Session, Question, Answer
from .serializers import SessionSerializer, QuestionSerializer, AnswerSerializer
from django.http import HttpResponse

def index(request):
    return HttpResponse("Termômetro de Relacionamentos!")

class CreateSessionView(APIView):
    def post(self, request):
        name = request.data.get('name')
        if not name:
            return Response({"error": "Nome é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

        session = Session.objects.create(name=name)
        link = f"http://localhost:8000/session/{session.id}"
        return Response({"session_id": session.id, "link": link}, status=status.HTTP_201_CREATED)

class QuestionsView(APIView):
    def get(self, request):
        questions = Question.objects.prefetch_related('options').all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SubmitAnswersView(APIView):
    def post(self, request, session_id):
        session = Session.objects.filter(id=session_id).first()
        if not session:
            return Response({"error": "Sessão não encontrada."}, status=status.HTTP_404_NOT_FOUND)

        answers_data = request.data.get('answers', [])
        for answer_data in answers_data:
            question = Question.objects.filter(id=answer_data['question_id']).first()
            if not question:
                return Response({"error": f"Pergunta {answer_data['question_id']} não encontrada."}, status=status.HTTP_400_BAD_REQUEST)

            Answer.objects.create(session=session, question=question, response=answer_data['response'])

        return Response({"message": "Respostas salvas com sucesso!"}, status=status.HTTP_201_CREATED)

class AnswersView(APIView):
    def get(self, request, session_id):
        session = Session.objects.filter(id=session_id).first()
        if not session:
            return Response({"error": "Sessão não encontrada!"}, status=status.HTTP_404_NOT_FOUND)

        answers = Answer.objects.filter(session=session).select_related('question')

        data = [
            {
                "question": answer.question.text,
                "response": answer.response
            }
            for answer in answers
        ]

        return Response(data, status=status.HTTP_200_OK)