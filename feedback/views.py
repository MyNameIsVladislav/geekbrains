from django.urls import reverse_lazy
from django.views.generic import CreateView

from feedback.forms import FeedBackForm
from feedback.models import FeedBack


class FeedBackView(CreateView):
    model = FeedBack
    form_class = FeedBackForm
    template_name = 'contacts/contacts.html'
    success_url = reverse_lazy('main:index')
