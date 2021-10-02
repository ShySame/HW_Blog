from django.urls import path, include, reverse_lazy
from django.contrib.auth import views as auth_views

from authorization.views import RegisterFormView, UserView, UserEditView

urlpatterns = [
    path("register/", RegisterFormView.as_view(), name="register"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("profile/<int:pk>/", UserView.as_view(), name="profile"),
    path("profile/edit/<int:pk>/", UserEditView.as_view(), name="profile_edit"),
    path('password/change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password/change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password/reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password/reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path(r'password/reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),

    path('password/reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'), ]
