from django.db import models
import uuid

class Session(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    origin_session = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='derived_sessions')

    def __str__(self):
        return f"Session({self.name})"

class Question(models.Model):
    CATEGORY_CHOICES = [
        ('profile', 'Perfil'),
        ('relationship', 'Relacionamento'),
        ('preferences', 'Preferências'),
    ]
    id = models.CharField(max_length=50, primary_key=True)  # ID personalizado
    text = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f"{self.id}: {self.text}"


class AnswerOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    text = models.TextField()

    def __str__(self):
        return self.text

class Answer(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="answers", default='')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    response = models.TextField(default='')

    def __str__(self):
        return f"Answer({self.session.name} - {self.question.text})"
    
    class Meta:
        unique_together = ('session', 'question')
