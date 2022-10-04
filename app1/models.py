from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    # обновляет рейтинг пользователя, переданного в аргумент этого метода
    # три слагаемых: суммарный рейтинг каждой статьи автора умножается на 3
    # суммарный рейтинг всех комментариев автора
    # суммарный рейтирг всех комментариев к статьям автора
    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat * 3 +cRat
        self.save()


# категории публикаций по тематикам - IT, кино, театр, книги, спорт, походы, хобби
class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name.title()


class Post(models.Model):
    author = models.ForeignKey('Author', on_delete=models.CASCADE)

    ARTICLE = 'AR'
    NEWS = 'NW'
    TYPE_CHOICES = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]
    # поле с выбором типа "статья" или "новость"
    categoryType = models.CharField(max_length=2,
                                    choices=TYPE_CHOICES,
                                    default=NEWS)
    dateCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory', related_name='news')

    title = models.CharField(max_length=128)
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    # возвращает начало статьи (предварительный просмотр) длиной 65 символов и
    # добавляет многоточие в конце
    def preview(self):
        return self.text[0:64] + '...'

    def __str__(self):
        return f'{self.title.title()}: {self.text[:256]}'
        # title() -  Python метод строки, делает прописными первые буквы


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()