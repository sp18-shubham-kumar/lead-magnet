from django.shortcuts import render
from rest_framework.views import APIView


class HomeView(APIView):
    template_name = "home.html"

    def get(self, request):
        return render(request, self.template_name)
