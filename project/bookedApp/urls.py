from django.urls import path, include

from . import views

app_name = 'bookedApp'

urlpatterns = [

    path('signup', views.SignUp.as_view(), name = 'signup'),
    path('', views.Home.as_view(), name = 'home'),
    path('NewPost/', views.NewPost, name ='NewPost'),
    path('MyPosts/', views.MyPosts, name = 'MyPosts'),
    path('MyProfile/', views.MyProfile, name = 'MyProfile'),
    path('EditProfile/', views.EditProfile, name = 'EditProfile'),
    path('UserEdited/', views.UserEdited, name = 'UserEdited'),
    path('Followers/', views.Followers, name = 'Followers'),
    path('Following/', views.Following, name = 'Following'),
    path('MyFeed/', views.MyFeed, name = 'MyFeed'),
    path('ChangeProfilePicture/', views.ChangeProfilePicture, name = 'ChangeProfilePicture'),
    path('GenerateExcelSheet/<str:SelectedIDs>', views.GenerateExcelSheet, name = 'GenerateExcelSheet'),
    path('<user_id>/ViewProfile/', views.ViewProfile, name = 'ViewProfile'),
    path('<user_id>/<post_id>/ReportPost/', views.ReportPost, name = 'ReportPost'),
    path('<post_id>/EditPost/', views.EditPost, name = 'EditPost'),
    path('<post_id>/ConfirmDeletePost/', views.ConfirmDeletePost, name = 'ConfirmDeletePost'),  
    path('<post_id>/DeletePost/', views.DeletePost, name = 'DeletePost'),
    path('PostDeleted/', views.PostDeleted, name = 'PostDeleted'),
    path('<post_id>/NewComment', views.NewComment, name = 'NewComment'),
    path('<post_id>/', views.PostDetails, name = 'PostDetails'),
    path('<user_id>/Follow', views.Follow, name = 'Follow'),
    path('<user_id>/UnFollow', views.UnFollow, name = 'UnFollow'),
    path('<user_id>/EmailFollow', views.EmailFollow, name = 'EmailFollow'),
    path('<user_id>/EmailUnFollow', views.EmailUnFollow, name = 'EmailUnFollow'),

] 