from django.views.generic import TemplateView


class Index(TemplateView):
    template_name = 'index.html'


class InfoView(TemplateView):
    template_name = 'information_page.html'
