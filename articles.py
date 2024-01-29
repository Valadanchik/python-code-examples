from django.db import models
from django.utils.html import format_html

from sorl.thumbnail import get_thumbnail
from ckeditor_uploader.fields import RichTextUploadingField

from parler.models import TranslatableModel, TranslatedFields

from core.models import BaseModel
from core.models import BaseStatusModel
from core.models import BaseTimestampedModel

from ..utils import article_directory_path


class Article(BaseTimestampedModel, BaseStatusModel, BaseModel, TranslatableModel):
    """
        A class used to represent an Article model objects
        ...

        Attributes
        ----------
        title : str;
            string that represent a title for current article
        day_of_week : date;
            Date field that represent a day of week for current article
        content_type : str;
            string that represent a month when current card expires
        week : week;
            week object relation
        week_day_category : week_day;
            week_day_category object relation
        week_day : str;
            week_day object relation
        youtube_link : str;
            string that represent a YouTube link for current card

    """

    class Meta:
        app_label = "articles"
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    week = models.ForeignKey('articles.Week', models.SET_NULL, blank=True, null=True)
    week_day_category = models.ForeignKey('articles.WeekDayCategories', models.SET_NULL, blank=True, null=True)
    week_day = models.ForeignKey('articles.WeekDays', on_delete=models.SET_NULL, blank=True, null=True)
    category = models.ForeignKey('articles.Categories', on_delete=models.SET_NULL, blank=True, null=True)
    day_of_week = models.DateField(null=True)
    content_type = models.IntegerField(null=True, blank=True)
    pdf = models.FileField(upload_to='uploads/% Y/% m/% d/', blank=True, null=True)
    cover_image = models.ImageField(upload_to=article_directory_path, blank=True, null=True)
    # chapter = models.CharField(max_length=255, blank=True, null=True)
    index = models.IntegerField(blank=True, null=True)

    translations = TranslatedFields(
        title=models.CharField(max_length=255),
        chapter=models.CharField(max_length=255, blank=True, null=True),
        text=RichTextUploadingField(blank=True, null=True),
        meta_obj=models.CharField(max_length=255, blank=True, null=True)
    )

    def __str__(self):
        return f"{self.title}"

    @property
    def avatar_preview(self) -> str:
        if self.cover_image:
            _cover_image = get_thumbnail(self.cover_image,
                                         '50x50',
                                         upscale=False,
                                         crop=False,
                                         quality=100)
            return format_html(
                '<img src="{}" width="{}" height="{}">'.format(_cover_image.url, _cover_image.width,
                                                               _cover_image.height))
        return ""

    def get_app_list(self, request, app_label=None):
        app_dict = self._build_app_dict(request)
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())
        return app_list


class WeekDays(BaseTimestampedModel, BaseStatusModel, BaseModel, models.Model):
    """
           A class used to represent an Article model objects
           ...

           Attributes
           ----------
           week : week;
               week object relation
           date : date;
               Date field that represent a date object

            Methods
            -------
            get_all_related_article_objects(self)
                Returns a list of users who have an association with the current level object

       """
    week = models.ForeignKey('articles.Week', models.SET_NULL, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        app_label = "articles"
        verbose_name = 'WeekDay'
        verbose_name_plural = 'WeekDays'

    def get_all_related_article_objects(self) -> list:
        """Returns a list of articles which have an association with the current WeekDay object.

               Parameters
               ----------
                   self : instance
                       Instance of current age object

               Returns
               -------
                   list
                       generated PaymentMethods list
        """
        all_articles_with_week_day = [article for article in
                                      Article.objects.prefetch_related("week_day") if article.week_day]
        return [payment_method for payment_method in all_articles_with_week_day if payment_method.week_day is self]


class Categories(TranslatableModel):
    """
               A class used to represent a Categories model objects
               ...

               Attributes
               ----------
               name : str;
                   string that represent name of current category
           """

    translations = TranslatedFields(
        name=models.CharField(max_length=255, blank=True, null=True),
        created_at=models.DateTimeField(),
        updated_at=models.DateTimeField()
    )

    class Meta:
        app_label = "articles"
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f"{self.name}"


class WeekDayCategories(TranslatableModel):
    """
              A class used to represent an WeekDayCategories model objects
              ...

              Attributes
              ----------
              week_day : WeekDays;
                  week_day object relation
              category : Categories;
                  category object relation

               Methods
               -------
               get_all_related_article_objects(self)
                   Returns a list of users who have an association with the current level object

          """
    week_day = models.ForeignKey('articles.WeekDays', models.SET_NULL, blank=True, null=True)
    category = models.ForeignKey(Categories, models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    protected = models.BooleanField()
    translations = TranslatedFields(
        name=models.CharField(max_length=255, blank=True, null=True),
    )

    class Meta:
        app_label = "articles"
        verbose_name = 'WeekDayCategory'
        verbose_name_plural = 'WeekDayCategories'

    def __str__(self):
        return f"{self.name}"


class DefaultCategories(BaseTimestampedModel, BaseStatusModel, BaseModel, TranslatableModel):
    id = models.BigAutoField(primary_key=True)
    protected = models.BooleanField()

    translations = TranslatedFields(
        name=models.CharField(max_length=255),
    )

    class Meta:
        app_label = "articles"
        verbose_name = 'DefaultCategories'
        verbose_name_plural = 'DefaultCategories'

    def __str__(self):
        return f"{self.name}"


class Week(BaseTimestampedModel, BaseStatusModel, BaseModel, TranslatableModel):
    """
                  A class used to represent an Week model objects
                  ...

                  Attributes
                  ----------
                  title : str;
                      string that represent the title of current week object
                  start_date : DateField;
                      date_field that represent start of the week

                  due_date : DateField;
                      date_field that represent due date of the week

                   Methods
                   -------
                   get_all_related_article_objects(self)
                       Returns a list of users who have an association with the current level object

              """
    start_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    default_category = models.ForeignKey(DefaultCategories, models.SET_NULL, blank=True, null=True)

    translations = TranslatedFields(
        title=models.CharField(max_length=255, blank=True, null=True),
    )

    class Meta:
        app_label = "articles"
        verbose_name = 'Week'
        verbose_name_plural = 'Weeks'

    def __str__(self):
        return f"{self.title}"

    def get_all_related_article_objects(self) -> list:
        """Returns a list of articles which have an association with the current Week object.

               Parameters
               ----------
                   self : instance
                       Instance of current age object

               Returns
               -------
                   list
                       generated PaymentMethods list
        """
        all_articles_with_week = [article for article in
                                  Article.objects.prefetch_related("week") if article.week]
        return [payment_method for payment_method in all_articles_with_week if payment_method.week is self]
