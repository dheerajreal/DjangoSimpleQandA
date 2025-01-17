from django.contrib.auth import views
from django.urls import path

from .views import SignUp, UserEmailEdit, UserProfileUpdate, dark_mode_toggle

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('password_change/', views.PasswordChangeView.as_view(),
         name='password_change'),
    path('password_change/done/', views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),

    path('password_reset/', views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]


urlpatterns += [
    path('signup/', SignUp.as_view(), name='signup'),
    path('profile_update/', UserProfileUpdate.as_view(),
         name='user_profile_update'),
    path('email_update/', UserEmailEdit.as_view(), name='user_email_update'),
    path('darkmode/', dark_mode_toggle, name='dark_mode_toggle'),

]
