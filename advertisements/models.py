from django.db import models

from users.models import User


# ----------------------------------------------------------------------------------------------------------------------
# Create advertisement model
class Advertisement(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=1000, null=True)
    image = models.ImageField(upload_to='advertisements/', null=True)
    price = models.PositiveIntegerField()
    title = models.CharField(max_length=200)

    class Meta:
        """
        Meta information for advertisement model
        """
        verbose_name: str = 'Объявление'
        verbose_name_plural: str = 'Объявления'

    def __str__(self):
        return f'Объявление "{self.title}" создано {self.created_at} пользователем {self.author.first_name}'


# ----------------------------------------------------------------------------------------------------------------------
# Create comment model
class Comment(models.Model):
    text = models.CharField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ad = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        Meta information for comment model
        """
        verbose_name: str = 'Комментарий'
        verbose_name_plural: str = 'Комментарии'

    def __str__(self):
        return f'Пользователь {self.author.first_name} оставил комментарий к объявлению "{self.ad.title}"'
