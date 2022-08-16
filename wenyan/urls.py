from django.urls import path

from . import views

app_name='wenyan'
urlpatterns = [
    path('', views.index, name='index'),
    path('search_result/',views.search_result,name='search_result'),
    path('word/<str:word>/',views.word,name='word'),
    path('edit_explanation/<str:word>/',views.edit_explanation,name='edit_explanation'),
    path('submit_explanation/<int:word_id>',views.submit_explanation,name='submit_explanation'),
    path('edit_sentence/<int:explanation_id>',views.edit_sentence,name="edit_sentence"),
    path('submit_sentence/<int:explanation_id>',views.submit_sentence,name="submit_sentence"),
    path('index_tips/',views.index_tips,name="index_tips"),
]