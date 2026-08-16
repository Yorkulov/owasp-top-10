from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import SupportMessage


@login_required
def contact(request):
    if request.method == "POST":
        subject = request.POST.get("subject", "")
        body = request.POST.get("body", "")
        SupportMessage.objects.create(user=request.user, subject=subject, body=body)
        messages.success(request, "Xabaringiz yuborildi. Tez orada javob beramiz.")
        return redirect("support:contact")

    my_messages = SupportMessage.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "support/contact.html", {"my_messages": my_messages})
