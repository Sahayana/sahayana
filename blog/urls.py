from django.urls import path
from .views import *

app_name = 'blog'


urlpatterns = [

    # Post
    path('', post_list, name='post_all'),
    path('<slug:main_category_slug>/<slug:category_slug>/', post_list, name='post_in_category'),  
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('post/<slug:category_slug>/create/', post_create, name='post_create'),
    path('post/<int:post_id>/update/', post_update, name='post_update'),
    path('post/<int:post_id>/delete/', post_delete, name='post_delete'), # delete 기능은 jQuery를 쓸 예정.
    
    # Comment
    path('post/<int:post_id>/comment/create', comment_create, name='comment_create'),
    path('post/comment/<int:comment_id>/update', comment_update, name='comment_update'),
    path('post/comment/<int:comment_id>/delete', comment_delete, name='comment_delete'),

    # recommend
    path('post/<int:post_id>/recommend', post_recommend, name='post_recommend'),
    path('post/comment/<int:comment_id>/recommend', comment_recommend, name='comment_recommend'),
 
]