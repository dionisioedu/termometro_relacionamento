from django.core.management.base import BaseCommand
from myapp.models import Question, AnswerOption
from myapp.questions_data import QUESTIONS

class Command(BaseCommand):
    help = "Carrega perguntas e opções no banco de dados."

    def handle(self, *args, **kwargs):
        for question_data in QUESTIONS:
            question, created = Question.objects.get_or_create(
                id=question_data["id"],
                defaults={
                    "text": question_data["text"],
                    "category": question_data["category"],
                }
            )
            if created:
                self.stdout.write(f"Pergunta adicionada: {question.id} - {question.text}")
            else:
                self.stdout.write(f"Pergunta já existente: {question.id} - {question.text}")

            # Adicionar opções de resposta
            for option_text in question_data.get("options", []):
                AnswerOption.objects.get_or_create(question=question, text=option_text)
                self.stdout.write(f"  Opção de resposta adicionada: {option_text}")
