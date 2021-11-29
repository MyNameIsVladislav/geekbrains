from django.shortcuts import render, redirect
from django.views import View

from feedback.forms import FeedBackForm


class FeedBackView(View):
    form = FeedBackForm

    def get_context_data(self):
        return {"form": self.form}

    def get(self, request):
        return render(request, 'contacts/contacts.html', self.get_context_data())

    def post(self, request):
        data = self.form(data=request.POST)
        if data.is_valid():
            return redirect('contacts:contact')
