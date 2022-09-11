from django.urls import path

from . import views,newviews

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
    path('sentence_tips/',views.sentence_tips,name="sentence_tips"),
    path('id2info/',views.id2info,name="id2info"),
    path('chuchu_tips/',views.chuchu_tips,name="chuchu_tips"),
    path('delete_example/',views.delete_example,name="delete_example"),
    path('delete_explanation/',views.delete_explanation,name="delete_explanation"),

    path('contest/',newviews.Mainpage,name="contest_mp"),
    path('contest_hy/',newviews.Mainpage_hy,name="contest_hy_mp"),
    path('contest/exercise/',newviews.ExercisePage, name="contest_ep"),
    path('contest/test/',newviews.TestPage,name="contest_tp"),
    path('contest/answer/',newviews.AnswerPage,name="contest_ap"),
]
