from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('show_category', kwargs={'cat_id': self.pk})


class Word(models.Model):
    eng_word = models.CharField(max_length=30)
    ukr_word = models.CharField(max_length=30)
    correct_answers = models.SmallIntegerField(default=0, verbose_name='Кількість правильних відповідей')
    last_answer = models.DateTimeField(auto_now=True, verbose_name='Час останньої відповіді')
    category = models.ForeignKey('Category', related_name='words', on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = [('eng_word', 'category'), ]

    def __str__(self):
        return self.eng_word

    def get_absolute_url(self):
        return reverse('show_word', kwargs={'word_id': self.pk, 'cat_id': self.category.pk})

