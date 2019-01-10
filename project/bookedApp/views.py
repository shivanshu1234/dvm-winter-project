from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic 
from .models import Post
from .forms import NewPostForm, NewCommentForm, EditPostForm, UserCreationFormWithEmail, EditUserForm, NewReportForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import datetime
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User

class SignUp(generic.CreateView):
    form_class = UserCreationFormWithEmail
    success_url = reverse_lazy('login') # reverse_lazy : because class attributes are loaded upon import.
    template_name = 'bookedApp/signup.html'


class Home(generic.ListView):
    template_name = 'bookedApp/home.html'
    context_object_name = 'latest_post_list'
    
    def get_queryset(self):
        return Post.objects.order_by('-date')


def PostDetails(request, post_id):    
    post = get_object_or_404(Post, id = post_id)
    current_user = request.user
    reported = False # Has the current user reported this post yet?
    for report in post.report_set.all():
        if report.reporting_user == current_user:
            reported = True
    context = {
        'post':post,
        'reported':reported
        }
    
    return render(request, 'bookedApp/PostDetails.html', context = context)


@login_required
def NewPost(request):
    if request.method == "POST":
        form = NewPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False) # commit=False : Create the instance but don't save it to the database.
            post.user = request.user
            post.date = timezone.now()
            post.save()
            return redirect('bookedApp:home')
    else:
        form = NewPostForm()
    
    return render(request, template_name = 'bookedApp/NewPost.html', context={'form':form})


@login_required
def NewComment(request, post_id):
    post = get_object_or_404(Post, id = post_id)
    if request.method == "POST":
        form = NewCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('bookedApp:PostDetails', post_id = post_id)

    else:
        form  = NewCommentForm()
    
    context={
        'form':form, 
        'post':post
        }
    
    return render(request, template_name = 'bookedApp/NewComment.html', context = context)


@login_required
def MyPosts(request):
    user = request.user
    posts_by_user = Post.objects.filter(user = user).order_by('-date')
    
    context = {
        'user':user, 
        'posts_by_user':posts_by_user
        }
    
    return render(request, template_name = "bookedApp/MyPosts.html", context = context)


@login_required
def EditPost(request, post_id):
    post = get_object_or_404(Post, id = post_id)
    
    if timezone.now() - post.date < datetime.timedelta(minutes = 5): # Posts are editable only till 5 minutes after posting them.
        post_is_editable = True  
        
        if post.user == request.user:
            if request.method == "POST":
                form = EditPostForm(request.POST,)
                if form.is_valid():
                    post = form.save(commit = False)
                    post.id = post_id
                    post.user = request.user
                    post.date = timezone.now()
                    
                    if not post.heading.endswith('(edited)'): # "(edited)" is added only once.
                        post.heading = post.heading + "(edited)"
                    else: 
                        post.heading = post.heading
                    
                    post.save()
                    return redirect('bookedApp:MyPosts')
            else:
                form = EditPostForm(initial={'heading':post.heading, 'text':post.text})
        
        context = {
            'form':form, 
            'post_is_editable':post_is_editable
            }

        return render(request, template_name = 'bookedApp/EditPost.html', context=context)
                
    else: 
        post_is_editable = False 
        context = {'post_is_editable':post_is_editable}               
        return render(request, template_name = 'bookedApp/EditPost.html', context=context)


def ConfirmDeletePost(request, post_id):
    post = get_object_or_404(Post, id = post_id)
    if post.user == request.user:
        
        context = {
            'heading':post.heading, 
            'id':post.id
            }
        
        return render(request, template_name = 'bookedApp/ConfirmDeletePost.html', context=context)
    else:
        raise PermissionDenied


def DeletePost(request, post_id):
    post = get_object_or_404(Post, id = post_id)
    if post.user == request.user:
        post.delete()
        return redirect('bookedApp:PostDeleted')
    else: 
        raise PermissionDenied


def PostDeleted(request):
    return render(request, template_name = 'bookedApp/PostDeleted.html', context = {})


@login_required
def MyProfile(request):
    user = request.user
    return render(request, template_name = 'bookedApp/MyProfile.html', context = {'user':user})


@login_required
def EditProfile(request):
    user = request.user
    if request.method == "POST":
        form = EditUserForm(request.POST, instance=user)
        
        if form.is_valid():
            user.email = request.POST['email']
            user.username = form.clean_username()
            user.save()
            return redirect('bookedApp:UserEdited')

    else:
        form = EditUserForm(initial = {'username':user.username, 'email':user.email})

    context = {'form':form}
    return render(request, template_name = 'bookedApp/EditProfile.html', context = context)


def UserEdited(request):
    return render(request, template_name = 'bookedApp/UserEdited.html', context = {})


def ViewProfile(request, user_id):
    current_user = request.user
    other_user = get_object_or_404(User, id = user_id)
    posts = Post.objects.filter(user = other_user).order_by('-date')

    if current_user == other_user:
        own_profile = True
    else:
        own_profile = False
    
    if other_user in current_user.userprofile.follows.all():
        user_follows_other_user = True
    else:
        user_follows_other_user = False
    
    context = {
        'other_user': other_user, 
        'user_follows_other_user':user_follows_other_user,
        'posts':posts,
        'own_profile':own_profile,
        }

    return render(request, template_name = 'bookedApp/ViewProfile.html', context = context)


@login_required
def Follow(request, user_id):
    user_to_be_followed = get_object_or_404(User, id = user_id)
    current_user = request.user
    current_user.userprofile.follows.add(user_to_be_followed)
    return redirect('ViewProfile/')


@login_required
def UnFollow(request, user_id):
    user_to_be_unfollowed = get_object_or_404(User, id = user_id)
    current_user = request.user
    
    if user_to_be_unfollowed in current_user.userprofile.follows.all():
        current_user.userprofile.follows.remove(user_to_be_unfollowed)
    
    return redirect('ViewProfile/')


@login_required
def Followers(request):
    user = request.user
    followers = user.followers.all()
    context = {'followers':followers}
    return render(request, template_name = 'bookedApp/Followers.html', context = context)


@login_required
def Following(request):
    user = request.user
    following = user.userprofile.follows.all()
    context = {'following':following}
    return render(request, template_name = 'bookedApp/Following.html', context = context)


@login_required
def MyFeed(request):
    user = request.user
    # Posts by all the users that the current user follows.
    posts = Post.objects.filter(user__userprofile__follows__id = user.id)
    context = {'posts':posts}
    return render(request, template_name = 'bookedApp/MyFeed.html', context = context)


@login_required
def ReportPost(request, user_id, post_id):
    post = get_object_or_404(Post, id = post_id)
    if request.method == "POST":
        form = NewReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit = False)
            report.post = post
            report.reported_user = get_object_or_404(User, id = user_id)
            report.reporting_user = request.user
            report.save()

            if post.report_set.all().count() > 2: # If post has more than 2 reports, remove it.
                post.delete()
                return redirect("/bookedApp/")

            return redirect("/bookedApp/"+str(post_id)+"/")  # "/bookedApp/<post_id>/"
    else:
        form = NewReportForm()
    
    context = {
        'form':form,
        'post':post
        }
  
    return render(request, template_name = 'bookedApp/ReportPost.html', context = context)

    