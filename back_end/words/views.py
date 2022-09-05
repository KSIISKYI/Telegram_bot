from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.urls import reverse

from .models import Word, Category
from .serializers import WordSerializer, CategorySerializer
from . import service


class RandomWord(generics.RetrieveAPIView):
    serializer_class = WordSerializer
    queryset = Word.objects.all()


class CategoryList(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def list(self, request, *args, **kwargs):
        categories = self.get_queryset()
        context = self.get_serializer(categories, many=True).data
        for cat in context:
            cat.__setitem__('link',
                            [request.build_absolute_uri(categories.get(pk=cat['id']).get_absolute_url()), 'get'])

        return Response(context)


class CategoryDetails(APIView):
    def get(self, request, *args, **kwargs):
        menu_list = {
            'Вибрати вправу': [
                request.build_absolute_uri(reverse('choose_exercise', kwargs={'cat_id': kwargs['cat_id']})), 'get'],
            'Список слів': [request.build_absolute_uri(reverse('show_words', kwargs={'cat_id': kwargs['cat_id']})),
                            'get'],
        }
        data = {'menu_list': menu_list}
        category = CategorySerializer(Category.objects.get(pk=kwargs['cat_id']))
        data['category'] = category.data
        return Response(data=data)


class ExerciseList(APIView):
    def get(self, request, *args, **kwargs):
        data = {
            'Тести': [request.build_absolute_uri(
                reverse('choose_lang', kwargs={'cat_id': kwargs['cat_id'], 'ex_slug': 't'})), 'get'],
            'Письмо': [request.build_absolute_uri(
                reverse('choose_lang', kwargs={'cat_id': kwargs['cat_id'], 'ex_slug': 'w'})), 'get']
        }

        return Response(data=data)


class LangList(APIView):
    def get(self, request, **kwargs):
        words = Word.objects.filter(category__pk=kwargs['cat_id'])
        if w := service.get_random_word(words):
            data = {
                'З анг на укр': [request.build_absolute_uri(
                    reverse('check_word',
                            kwargs={'cat_id': kwargs['cat_id'],
                                    'ex_slug': kwargs['ex_slug'],
                                    'lang_slug': 'eng',
                                    'word_id': w.pk})),
                    'get'],
                'З укр на англ': [request.build_absolute_uri(
                    reverse('check_word',
                            kwargs={'cat_id': kwargs['cat_id'],
                                    'ex_slug': kwargs['ex_slug'],
                                    'lang_slug': 'ukr',
                                    'word_id': w.pk})),
                    'get'],
            }
        else:
            data = {'text': 'На даний момент слів для повторення не залишилося',
                                   'link': ['http://127.0.0.1:8000/api/v1/cats/', 'get']}
        return Response(data)


class CheckWord(APIView):
    def get(self, request, **kwargs):
        data = service.generate_data_response_for_write(request, kwargs)
        return Response(data)


class ExerciseDetail(APIView):
    def get_queryset(self):
        return Category.objects.get(pk=self.kwargs['cat_id']).words.all()

    def get(self, request, **kwargs):
        queryset = self.get_queryset()
        result = service.get_random_word(queryset)
        if result:
            return Response(
                {'word': WordSerializer(result).data, 'correct_answer': WordSerializer(result).data['urk_word']})
        else:
            return Response('Слів більше не має')

    def post(self, request, **kwargs):
        pass


class WordList(generics.ListAPIView):
    serializer_class = WordSerializer
    queryset = Word.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(category__pk=self.kwargs['cat_id'])
        return queryset

    def list(self, request, *args, **kwargs):
        words = self.get_queryset()
        context = self.get_serializer(words, many=True).data
        for word in context:
            word.__setitem__('link',
                             ['http://127.0.0.1:8000{}'.format(words.get(pk=word['id']).get_absolute_url()), 'get'])

        return Response(context)


class AddWord(generics.CreateAPIView):
    serializer_class = WordSerializer


class WordDetails(generics.RetrieveAPIView):
    serializer_class = WordSerializer
    queryset = Word.objects.all()

    def get_object(self):
        filter_kwargs = {
            'pk': self.kwargs['word_id'],
            'category__pk': self.kwargs['cat_id']
        }
        obj = generics.get_object_or_404(self.get_queryset(), **filter_kwargs)
        self.check_object_permissions(self.request, obj)

        return obj
