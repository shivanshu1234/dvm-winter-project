from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from PIL import Image

class Post(models.Model):
    heading = models.CharField(max_length = 200)
    text = models.TextField()
    date = models.DateTimeField('date posted')
    user = models.ForeignKey(User, on_delete = models.CASCADE, null = True, default = None)
    objects = models.Manager()

    def __str__(self):
        return self.heading 


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(default = timezone.now)
    objects = models.Manager()
    
    def __str__(self):
        return self.text


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, null = True)
    follows = models.ManyToManyField(User,  related_name = 'followers', symmetrical = False)
    EmailFollows = models.ManyToManyField(User, related_name = 'EmailFollowers', symmetrical = False)
    picture = models.ImageField(upload_to = 'profile_picture', blank = True, default = 'default.jpeg')

    def __str__(self):
        try:
            return "UserProfile object of " + self.user.username
        except:
            return "Unrelated UserProfile object with id = " + str(self.id)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        profile_pic = Image.open(self.picture.path)
        
        if profile_pic.height > 300 or profile_pic.width > 300:
            output_size = (300, 300)
            profile_pic.thumbnail(output_size)
            profile_pic.save(self.picture.path)


def create_profile(sender, **kwargs):
    """
    Creates a new UserProfile object. 
    Recieves the User to be connected to the profile as 'instance'.
    """
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = UserProfile(user=user)
        user_profile.save()

post_save.connect(create_profile, sender=User)
# post_save signal sent after creation of a User object is connected to create_profile.
# This associates every new User object with a UserProfile upon creation.


class Report(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    reported_user = models.ForeignKey(User, on_delete = models.CASCADE)
    reporting_user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'reports_made')

    reason = models.CharField(max_length = 100)
    detailed_reason = models.TextField(blank = True)

    def __str__(self):
        return self.reported_user.username + "_" + self.reason
        




    


        






