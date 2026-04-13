from django.contrib import admin
from django.urls import path
from mailapp import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index),
    path("login/", views.logins),
    path("register/", views.register),
    path("userHome/", views.userHome),
    path("userHeader/", views.userHeader),
    path("adminHome/", views.adminHome),
    path("adminHeader/", views.adminHeader),
    path("viewUsers/", views.viewUsers),
    path("manageUser/", views.manageUser),
    path("viewProfile/", views.viewProfile),
    path("updateProfile/", views.updateProfile),
    path("compose/", views.compose),
    path("inbox/", views.inbox),
    path("readMail/", views.readMail),
    path("outBox/", views.outBox),
    path("deleteMail/", views.deleteMail),
    path("drafts/", views.drafts),
    path("readDraft/", views.readDraft),
    path("addFeedback/", views.addFeedback),
    path("viewFeedbacks/", views.viewFeedbacks),
    path("blockUser/", views.blockUser),

    path("adminBlockedUsers/", views.adminBlockedUsers),
    path("restrictUser/", views.restrictUser),
    path("allowUser/", views.allowUser),

    path("unblockUser/", views.unblockUser),
    path("blockedUsers/", views.blockedUsers),
]