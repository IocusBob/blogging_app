from django.db import models
from django.utils import timezone
from django.urls import reverse


class Post(models.Model):
    # We are using the Authenticated user (admin level users) as a ForeignKey here
    author = models.ForeignKey('auth.User', on_delete = models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    # We want this to reflect a data field that can be activated by the use of a
    # button rather than automatically when a new entry is added.
    published_date = models.DateTimeField(blank=True, null=True)

    # Method that when called, sets the value of the published_date field
    # to be the current time
    def publish(self):
        self.published_date=timezone.now()
        self.save()

    # Redirect method
    def get_absolute_url(self):
        return reverse("post_detail", kwargs={'pk':self.pk})

    # This method returns a list of approved comments
    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    def __str__(self):
        return self.title

class Comments(models.Model):
    post = models.ForeignKey('blog.post',related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    # Below, comments start off as not approved and there is a method to approve
    # them. In the 'Post' class we can filter comments by whether this field is
    # True for each comment.
    approved_comment = models.BooleanField(default=False)

    # Method for making a comment approved
    def approve(self):
        self.approved_comment=True
        self.save()

    def get_absolute_url(self):
        return reverse('post_list')

    def __str__(self):
        return self.text
