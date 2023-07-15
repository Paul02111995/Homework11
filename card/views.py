from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from .models import Card


class CardsView(View):
    def get(self, request: HttpRequest):
        cards = Card.objects.all()
        json_response = {
            "cards": [
                {
                    "id": str(card.id),
                    "pan": card.pan,
                    "expiry_date": card.expiry_date,
                    "cvv": card.cvv,
                    "issue_date": str(card.issue_date),
                    "owner_id": card.owner_id,
                    "status": card.status,
                }
                for card in cards
            ]
        }
        if request.headers.get("accept") == "application/json":
            return JsonResponse(json_response)
        else:
            context = {
                "cards": cards
            }
            return render(request, "cards/card_list.html", context)

    def post(self, request: HttpRequest):
        pan = request.POST.get("pan")
        expiry_date = request.POST.get("expiry_date")
        cvv = request.POST.get("cvv")
        issue_date = request.POST.get("issue_date")
        owner_id = request.POST.get("owner_id")
        status = request.POST.get("status")

        card = Card.objects.create(
            pan=pan,
            expiry_date=expiry_date,
            cvv=cvv,
            issue_date=issue_date,
            owner_id=owner_id,
            status=status
        )

        return JsonResponse({"id": str(card.id)})


def create_card_view(request):
    if request.method == "GET":
        return render(request, "cards/create_card_form.html")
    elif request.method == "POST":
        pan = request.POST.get("pan")
        expiry_date = request.POST.get("expiry_date")
        cvv = request.POST.get("cvv")
        issue_date = request.POST.get("issue_date")
        owner_id = request.POST.get("owner_id")
        status = request.POST.get("status")

        card = Card.objects.create(
            pan=pan,
            expiry_date=expiry_date,
            cvv=cvv,
            issue_date=issue_date,
            owner_id=owner_id,
            status=status
        )

        return HttpResponseRedirect(reverse("card_list"))

