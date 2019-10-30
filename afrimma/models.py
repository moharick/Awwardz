from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime as dt

# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='profiles/')
    bio = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)

    class Meta:
        ordering = ('user',)



    def save_profile(self):
        self.save()


class Project(models.Model):
    title = models.CharField(max_length=150)
    home = models.ImageField(upload_to='photos')
    description = models.CharField(max_length=255)
    live_link = models.URLField(max_length=250)
    design = models.IntegerField(blank=True,default=0)
    usability = models.IntegerField(blank=True,default=0)
    content = models.IntegerField(blank=True,default=0)
    overall = models.IntegerField(blank=True,default=0)
    posted  = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        ordering = ('title',)

    @classmethod
    def search_project(cls, search_term):
        projects = cls.objects.filter(title__icontains=search_term)
        return projects

    def save_project(self):
        self.save()


    def __str__(self):
        return self.title

class Review(models.Model):
    CHOICES = (1, 1),(2, 2),(3, 3),(4, 4),(5, 5),(6, 6),(7, 7),(8, 8),(9, 9),(10, 10)

    design = models.IntegerField(choices=CHOICES,default=0)
    usability= models.IntegerField(choices=CHOICES,default=0)
    content =  models.IntegerField(choices=CHOICES,default=0)
    overall_score = models.IntegerField(blank=True,default=0)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)

    def __str__(self):
        return self.design

    class Meta:
        ordering = ['-id']

    def save_review(self):
        self.save()

    @classmethod
    def get_review(cls, profile):
        review = Review.objects.filter(Profile__pk = profile)
        return review

    @classmethod
    def get_all_reviews(cls):
        reviews = Review.objects.all()
        return reviews

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


