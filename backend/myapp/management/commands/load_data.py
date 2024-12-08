from django.core.management.base import BaseCommand
from myapp.models import Question, AnswerOption
from myapp.questions_data import QUESTIONS
from myapp.answers_data import ANSWERS

class Command(BaseCommand):
    help = "Carrega perguntas e respostas no banco de dados."

    def handle(self, *args, **kwargs):
        # Carregar perguntas
        for question_data in QUESTIONS:
            question, created = Question.objects.get_or_create(
                id=question_data["id"],
                defaults={
                    "text": question_data["text"],
                    "category": question_data["category"],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Pergunta adicionada: {question.id} - {question.text}"))
            else:
                self.stdout.write(self.style.WARNING(f"Pergunta já existe: {question.id} - {question.text}"))

        # Carregar respostas
        for question_id, options in ANSWERS.items():
            question = Question.objects.filter(id=question_id).first()
            if question:
                for option_text in options:
                    AnswerOption.objects.get_or_create(question=question, text=option_text)
                    self.stdout.write(self.style.SUCCESS(f"Opção de resposta adicionada: {option_text} para {question_id}"))
