from django.urls import path

from . import views

urlpatterns = [
    path('add_word/', views.AddWord.as_view()),
    path('get_random_word/', views.RandomWord.as_view()),
    path('cats/', views.CategoryList.as_view()),
    path('cats/<int:cat_id>/', views.CategoryDetails.as_view(), name='show_category'),
    path('cats/<int:cat_id>/ex/', views.ExerciseList.as_view(), name='choose_exercise'),

    path('cats/<int:cat_id>/ex/<slug:ex_slug>/lang/', views.LangList.as_view(), name='choose_lang'),

    path('cats/<int:cat_id>/ex/<slug:ex_slug>/<slug:lang_slug>/<int:word_id>/', views.CheckWord.as_view(), name='check_word'),

    path('cats/<int:cat_id>/ex/<slug:ex_slug>/<int:word_id>/', views.ExerciseDetail.as_view(), name='exercise_datail'),
    path('cats/<int:cat_id>/words/', views.WordList.as_view(), name='show_words'),
    path('cats/<int:cat_id>/<int:word_id>/', views.WordDetails.as_view(), name='show_word'),

]