from django.db import models

class Question(models.Model):
    text = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=[
        ('profile', 'Profile'),
        ('relationship', 'Relationship'),
        ('preferences', 'Preferences'),
    ],
    default='profile')  # Categoriza perguntas
    required = models.BooleanField(default=True)  # Indica se a pergunta é obrigatória

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_id = models.IntegerField()  # Ligado ao usuário
    text = models.TextField()  # Resposta do usuário

    def __str__(self):
        return f"Answer to: {self.question.text}"
