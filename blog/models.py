from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible
from django.utils.html import strip_tags
import markdown

class Category(models.Model):
    # 分类
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Tag(models.Model):
    # 标签
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Post(models.Model):
    # 文章
    title = models.CharField(max_length=70)

    body = models.TextField()
    
    # 文章创建时间和最后一次修改时间
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()

    # 摘要（可以没有）
    excerpt = models.CharField(max_length=200, blank=True)

    # 将分类和标签与文章关联，分别为一对多和多对多的关系
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)

    views = models.PositiveIntegerField(default=0)

    author = models.ForeignKey(User)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-created_time', 'title']

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        if not self.excerpt:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                ])
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        super(Post, self).save(*args, **kwargs)
