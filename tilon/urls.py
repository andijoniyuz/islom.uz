from django.urls import path

from .views import NamazView, SearchQuestView, QuestView, HomeView

urlpatterns = [
    path('/', HomeView(), name='Home'),
    path('namoz/', NamazView, name='namaz'),
    path('savol/', SearchQuestView, name='savol'),
    path('savol/<int:quest_id>', QuestView, name='savol'),
]
