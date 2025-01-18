from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Session, Question, Answer
from .serializers import SessionSerializer, QuestionSerializer, AnswerSerializer
from django.http import HttpResponse
from django.shortcuts import redirect
import logging

logger = logging.getLogger(__name__)

frontend_base_url = "http://localhost:8080"  # URL do frontend

def index(request):
    return HttpResponse("Termômetro de Relacionamentos!")

class CreateSessionView(APIView):
    def post(self, request):
        name = request.data.get('name')
        if not name:
            return Response({"error": "Nome é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            session = Session.objects.create(name=name)

        except Session.DoesNotExist:
            return Response(
                {"error": "A tabela 'Session' não foi encontrada. Verifique se as migrações foram aplicadas."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        except Exception as e:
            # Capturar quaisquer outros erros inesperados
            return Response(
                {"error": f"Ocorreu um erro inesperado: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response({"session_id": session.id}, status=status.HTTP_201_CREATED)

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
            if 'question_id' not in answer_data or 'response' not in answer_data:
                return Response({"error": "Dados da resposta incompletos."}, status=status.HTTP_400_BAD_REQUEST)

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

        answers = Answer.objects.filter(session=session).select_related('question').order_by('question__id')

        data = [
            {
                "question": answer.question.text,
                "response": answer.response
            }
            for answer in answers
        ]

        return Response(data, status=status.HTTP_200_OK)

class DerivedSessionView(APIView):
    def get(self, request, session_id):
        origin_session = Session.objects.filter(id=session_id).first()
        if not origin_session:
            return Response({"error": "Sessão de origem não encontrada."}, status=status.HTTP_404_NOT_FOUND)

        logger.info(f"Sessão de origem: {origin_session.id}")
        new_session = Session.objects.create(origin_session=origin_session)
        logger.info(f"Sessão derivada: {new_session.id}")
        return redirect(f"{frontend_base_url}/derived_session/{new_session.id}")

class ResultsView(APIView):
    def get(self, request, session_id):
        derived_session = Session.objects.filter(id=session_id).first()
        if not derived_session:
            return Response({"error": "Sessão derivada não encontrada."}, status=status.HTTP_404_NOT_FOUND)

        origin_session = derived_session.origin_session
        if not origin_session:
            return Response({"error": "Sessão de origem não vinculada à sessão derivada."}, status=status.HTTP_400_BAD_REQUEST)

        answers_origin = Answer.objects.filter(session=origin_session)
        answers_derived = Answer.objects.filter(session=derived_session)

        report = []
        for origin_answer in answers_origin:
            derived_answer = answers_derived.filter(question=origin_answer.question).first()
            if derived_answer:
                similarity = "igual" if origin_answer.response == derived_answer.response else "diferente"
                report.append({
                    "question": origin_answer.question.text,
                    "origin_response": origin_answer.response,
                    "derived_response": derived_answer.response,
                    "similarity": similarity,
                })

        results_link = f"{frontend_base_url}/results/{session_id}"
        return Response({
            "report": report,
            "results_link": results_link
        }, status=status.HTTP_200_OK)
