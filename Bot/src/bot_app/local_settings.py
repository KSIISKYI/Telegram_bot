from . import controllers

SHOW_CATEGORIES_URL = 'http://127.0.0.1:8000/api/v1/cats/'
ADD_WORD = 'http://127.0.0.1:8000/api/v1/add_word/'


URLS = {
    r'api/v1/cats/$': [controllers.show_categories, 'get'],
    r'api/v1/cats/(?P<category_slug>[^/]+)/$': [controllers.show_category_detail, 'get'],
    r'api/v1/cats/(?P<category_slug>[^/]+)/words/$': [controllers.show_words, 'get'],
    r'api/v1/add_word/$': [controllers.add_word, 'post'],
    r'api/v1/cats/(?P<category_slug>[^/]+)/ex/$': [controllers.show_exercise, 'get'],
    r'api/v1/cats/(?P<category_slug>[^/]+)/ex/(?P<ex_slug>[^/]+)/lang/$': [controllers.show_lang, 'get'],
    r'api/v1/cats/(?P<category_slug>[^/]+)/ex/(?P<ex_slug>[^/]+)/(?P<lang_slug>[^/]+)/(?P<word_id>[^/]+)/$':
        [controllers.check_word, 'get'],
}