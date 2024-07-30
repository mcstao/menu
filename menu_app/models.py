from django.db import models
from django.urls import reverse


class Menu(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, related_name='items', on_delete=models.CASCADE)
    main_item = models.ForeignKey('self', null=True, blank=True, related_name='sub_items', on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    url = models.CharField(max_length=150, blank=True)
    named_url = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.name

    def get_url(self):
        if self.named_url:
            return reverse(self.named_url)
        return self.url
