from django.urls import path
from learner.views import cartDataView, deleteCartItem, deleteWishItem, learningPageView, courseWathingView, wishListView, searchResultViews

urlpatterns =[
    path('cart/', cartDataView, name='cart'),
    path('cart/delete/<int:id>/', deleteCartItem, name='cart-delete'),
    path('cart/delete/wishlist/<int:id>/', deleteWishItem, name='wish-delete'),
    path('course/my-learning/learning/', learningPageView, name='learning-page'),
    path('course/my-learning/learning/<slug:slug>/', courseWathingView, name='watching_page'),
    path('course/my-learning/learning/<slug:slug>/<slug:slug_>/', courseWathingView, name='watching_page_video'),
    path('course/my-learning/wishlist/', wishListView, name='wishlist'),
    path('courses/search/', searchResultViews, name='search'),
    
]
