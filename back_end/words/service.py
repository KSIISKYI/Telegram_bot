import datetime
import random

from django.utils import timezone
from django.urls import reverse

from .models import Word

LEVELS = {
    0: 0,
    1: 2,
    2: 5,
    3: 12,
    4: 24
}


def get_random_word(queryset, current_word=None):
    """Повертає рандомне слово з доступних слів для перевірки"""

    result = []
    today = timezone.now()

    for k, w in LEVELS.items():
        min_last_answer = today - datetime.timedelta(hours=w)
        words = queryset.filter(correct_answers=k, last_answer__lt=min_last_answer)
        result += words

    if result := [w for w in result if w != current_word]:
        return random.choice(result)


def check_word(word, request, url_kwargs):
    """Повертає статус відповіді, True - якщо відповідь правильна, False - якщо відповідь не правильна"""

    answer = request.GET.get('answer')
    translated_word = word.eng_word if url_kwargs.get('lang_slug') == 'ukr' else word.ukr_word
    return translated_word == answer


def change_correct_answers(word, status_answer: bool):
    """Звінює кількість правильних відповідей вибраного слова, відповідно до статусу відповіді"""

    if status_answer:
        word.correct_answers += 1
    else:
        if word.correct_answers != 0:
            word.correct_answers -= 1
        else:
            word.correct_answers = 0
    word.save()


def generate_data_response_for_write(request, url_kwargs):
    """Повертає сгенерований дані для вправи на письмо"""

    queryset = Word.objects.filter(category__pk=url_kwargs.get('cat_id'))
    current_word = queryset.get(pk=url_kwargs.get('word_id'))
    response_data = {}

    if next_random_word := get_random_word(queryset):
        if request.GET.get('answer'):
            if status := check_word(current_word, request, url_kwargs):
                response_data['Result'] = 'Правильно'
            else:
                response_data['Result'] = 'Неправильно'
            if next_random_word := get_random_word(queryset, current_word):
                response_data['button_next'] = {'text': 'Наступне слово',
                                                'link': [request.build_absolute_uri(reverse('check_word', kwargs={
                                                    'cat_id': url_kwargs['cat_id'], 'ex_slug': url_kwargs['ex_slug'],
                                                    'lang_slug': url_kwargs['lang_slug'],
                                                    'word_id': next_random_word.pk
                                                })), 'get']}
                change_correct_answers(current_word, status)
            else:
                response_data['button'] = {'text': 'На даний момент слів для повторення не залишилося',
                                           'link': ['http://127.0.0.1:8000/api/v1/categories/', 'get']}
                change_correct_answers(current_word, status)
                return response_data

        else:
            response_data['button_check'] = {'text': 'Перевірити',
                                             'link': [request.build_absolute_uri(reverse('check_word', kwargs={
                                                 'cat_id': url_kwargs['cat_id'], 'ex_slug': url_kwargs['ex_slug'],
                                                 'lang_slug': url_kwargs['lang_slug'],
                                                 'word_id': current_word.pk
                                             })), 'get']}
        response_data['word'] = current_word.eng_word if url_kwargs['lang_slug'] == 'eng' else current_word.ukr_word
        response_data['translated_word'] = current_word.eng_word if url_kwargs[
                                                                        'lang_slug'] == 'ukr' else current_word.ukr_word

    else:

        if request.GET.get('answer'):
            if status := check_word(current_word, request, url_kwargs):
                response_data['Result'] = 'Правильно'
            else:
                response_data['Result'] = 'Неправильно'
            change_correct_answers(current_word, status)

        response_data['button'] = {'text': 'На даний момент слів для повторення не залишилося',
                                   'link': ['http://127.0.0.1:8000/api/v1/categories/', 'get']}
    return response_data
