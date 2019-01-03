# Winter Project

So here it is. This is __Booked__. I named it so because my initial plan was to make a place for discussions about books, a place for bibliophiles to rejoice. But I haven't actually added any features which justify that claim, so let's just ignore the name for now.

### For Security

Since the SECRET_KEY and the DATABASES have to be kept confidential, you will have to enter your own values for them in `project/booked/template_local_settings.py`, and rename the file to `local_settings.py`.

### User Authentication

Django's built in auth system has been used. A User is associated with a UserProfile as soon as it is created, using a OneToOneField. A User's UserProfile is used to handle the follower system, which is based on ManyToManyField. 

### Posts and comments

Users can create posts, edit them and delete them. Users can also comment on others posts, but comments cannot be modified once posted. ForeignKey has been used to associate Users, Posts and Comments.

### Preventing Cyber-crime

The ability to edit and delete posts can be used in a not so good way. Therefore, posts can be edited only within 5 minutes of being posted, which is enough time to fix any typos, but not enough to launch a cyber attack. Also, users have been given the power to report posts, and any post with more than 2 reports is removed from the sites. This number has been kept small for ease of testing.

This is all for now.
I'll be waiting for your feedback.

Shivanshu.

