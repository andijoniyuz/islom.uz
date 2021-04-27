from django.urls import path

from .views import NamazView, SearchQuestView, QuestView

urlpatterns = [
    path('namoz/', NamazView, name='namaz'),
    path('savol/', SearchQuestView, name='savol'),
    path('savol/<int:quest_id>', QuestView, name='savol'),
]
