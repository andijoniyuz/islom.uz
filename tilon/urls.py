from django.urls import path

from .views import NamozView, SearchQuestView, QuestView, HomeView, NamozRegionsView

urlpatterns = [
    path('', HomeView, name='Home'),
    path('api/', HomeView, name='Home'),
    path('api/namoz/', NamozRegionsView, name='namaz'),
    path('api/namoz/<int:region_id>', NamozView, name='namaz'),
    path('api/savol/', SearchQuestView, name='savol'),
    path('api/savol/<int:quest_id>', QuestView, name='savol'),
]
