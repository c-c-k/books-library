from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/details', views.QuestionDetails.as_view(), name='details'),
    path('<int:pk>/results', views.QuestionResults.as_view(), name='results'),
    path('<int:pk>/vote', views.vote, name='vote'),
    path('delete_question', views.delete_question, name='delete_question'),
    path('delete_choice', views.delete_choice, name='delete_choice'),
    path('repopulate', views.repopulate, name='repopulate'),
]
