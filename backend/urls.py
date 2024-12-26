from django.contrib import admin
from django.urls import path
from myapp import views
from myapp.views import CreateSessionView, QuestionsView, SubmitAnswersView, AnswersView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/session/create/', CreateSessionView.as_view(), name='create_session'),
    path('api/questions/', QuestionsView.as_view(), name='questions'),
    path('api/session/<uuid:session_id>/submit_answers/', SubmitAnswersView.as_view(), name='submit_answers'),
    path('api/session/<uuid:session_id>/answers/', AnswersView.as_view(), name='answers'),
    path('', views.index, name='index'),
]
