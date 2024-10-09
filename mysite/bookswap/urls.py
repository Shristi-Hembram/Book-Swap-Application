from django.urls import path
#from .views import index,login_view,signup_view,logout_view
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/',views.login_view, name='login'),
    path('signup/', views.signup_view, name = 'signup'),
    path('logout/', views.logout_view, name = 'logout'),

    path('book/add/', views.add_book, name = 'add_book'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),

    path('book/<int:book_id>/review/add/', views.add_review, name='add_review'),
    path('book/<int:book_id>/reviews/', views.book_reviews,name='book_reviews'),

    path('book/<int:book_id>/swap/',views.send_swap_request,name='send_swap_request'),
    path('swap/requests/',views.view_swap_requests, name='view_swap_requests'),
    path('swap/request/<int:request_id>/<str:action>/',views.manage_swap_request,name='manage_swap_request'),
    path('swaprequest/',views.my_swap_request,name='my_swap_request'),

]