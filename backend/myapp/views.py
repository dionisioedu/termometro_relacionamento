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
        
        origin_session_id = request.data.get('origin_session_id')

        try:
            # Se origin_session_id não for nulo, obtenha a sessão de origem
            origin_session = None
            if origin_session_id:
                origin_session = Session.objects.filter(id=origin_session_id).first()
                if not origin_session:
                    return Response(
                        {"error": f"Sessão de origem com ID {origin_session_id} não encontrada."},
                        status=status.HTTP_404_NOT_FOUND,
                    )

            # Crie uma nova sessão e associe a sessão de origem, se aplicável
            session = Session.objects.create(name=name, origin_session=origin_session)

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
            question = Question.objects.filter(id=answer_data['question_id']).first()
            if not question:
                return Response(
                    {"error": f"Pergunta {answer_data['question_id']} não encontrada."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Atualizar ou criar a resposta
            Answer.objects.update_or_create(
                session=session,
                question=question,
                defaults={"response": answer_data['response']}
            )

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

        new_session = Session.objects.filter(origin_session=origin_session).last()
        answers_submitted = Answer.objects.filter(session=new_session).exists() if new_session else False

        logger.info(f"Sessão derivada: {new_session.id if new_session else 'Nova'}")

        return Response({
            "session_id": origin_session.id,
            "derived_session_id": new_session.id if new_session else None,
            "origin_creator_name": origin_session.name,
            "answers_submitted": answers_submitted,
        }, status=status.HTTP_200_OK)

class ResultsView(APIView):
    def get(self, request, derivedSessionId):

        logger.info(f"Relatório de comparação para sessão derivada: {derivedSessionId}")
        derived_session = Session.objects.filter(id=derivedSessionId).first()
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

        return Response({
            "report": report
        }, status=status.HTTP_200_OK)
