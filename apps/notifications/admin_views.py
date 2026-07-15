from django.shortcuts import render, redirect
from django.contrib import messages

from apps.users.models import User
from .models import Notification


def send_notification(request):

    if request.method == "POST":

        title = request.POST["title"]
        body = request.POST["body"]

        send_to = request.POST["send_to"]

        if send_to == "all":

            notifications = []

            for user in User.objects.all():

                notifications.append(

                    Notification(

                        user=user,

                        title=title,

                        body=body,

                        type=request.POST["type"],

                        priority=request.POST["priority"],

                        category=request.POST["category"],

                        status="active",

                        created_by=request.user,

                        updated_by=request.user,
                    )
                )

            Notification.objects.bulk_create(notifications)

        else:

            user = User.objects.get(
                id=request.POST["user"]
            )

            Notification.objects.create(

                user=user,

                title=title,

                body=body,

                type=request.POST["type"],

                priority=request.POST["priority"],

                category=request.POST["category"],

                status="active",

                created_by=request.user,

                updated_by=request.user,
            )

        messages.success(
            request,
            "Notification sent successfully."
        )

        return redirect("../")

    users = User.objects.all()

    return render(
        request,
        "admin/send_notification.html",
        {
            "users": users,
        },
    )