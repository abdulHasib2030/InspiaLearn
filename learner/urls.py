from django.urls import path
from learner.views import cartDataView, deleteCartItem, deleteWishItem, learningPageView, courseWathingView, wishListView, searchResultViews, get_short_videos, video_detail

urlpatterns =[
    path('cart/', cartDataView, name='cart'),
    path('cart/delete/<int:id>/', deleteCartItem, name='cart-delete'),
    path('cart/delete/wishlist/<int:id>/', deleteWishItem, name='wish-delete'),
    path('course/my-learning/learning/', learningPageView, name='learning-page'),
    path('course/my-learning/learning/<slug:slug>/', courseWathingView, name='watching_page'),
    path('course/my-learning/learning/<slug:slug>/<slug:slug_>/', courseWathingView, name='watching_page_video'),
    path('course/my-learning/wishlist/', wishListView, name='wishlist'),
    path('courses/search/', searchResultViews, name='search'),
    path('videos/', get_short_videos, name="short_videos"),
     path('video/<int:video_id>/', video_detail, name='video_detail'),
     path('related-videos/<int:video_id>/', video_detail, name='video_scroll'),
]
