from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect
from django.urls import reverse,reverse_lazy
from django.views.generic import ListView,DetailView,CreateView,DeleteView,UpdateView
##from django.contrib.auth import logout
from .models import Book , Review
from .consts import ITEMS_PER_PAGE
from django.db.models import Avg

class ListBookView(LoginRequiredMixin,ListView):
  template_name = "book/index.html"
  model = Book
  paginate_by = ITEMS_PER_PAGE

class DetailBookView(LoginRequiredMixin,DetailView):
  template_name = "book/book_detail.html"
  model = Book

class CreateBookView(LoginRequiredMixin,CreateView):
  template_name = "book/book_create.html"
  model = Book
  fields = {"title","text","category","thumbnail"}
  success_url = reverse_lazy("list-book")

  def from_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DeleteBookView(LoginRequiredMixin,DeleteView):
  template_name = "book/book_delete.html"
  model = Book
  success_url = reverse_lazy("list-book")
  def get_object(self, queryset=None):
    obj = super().get_object(queryset)
    if obj.user != self.request.user:
      raise PermissionDenied
    return obj
  
class UpdateBookView(LoginRequiredMixin,UpdateView):
  template_name = "book/book_update.html"
  model = Book
  fields = {"title","text","category","thumbnail"}
  success_url = reverse_lazy("list-book")
  def get_object(self, queryset=None):
    obj = super().get_object(queryset)
    if obj.user != self.request.user:
       raise PermissionDenied
    return obj
  def get_success_url(self):
    return reverse('detail-book', kwargs={'pk': self.object.id})

def index_view(reqest):
  object_list = Book.objects.order_by("-id")
  ranking_list = Review.objects.annotate(avg_rating=Avg('rate')).order_by("-avg_rating")
  paginator = Paginator(object_list,ITEMS_PER_PAGE)
  page_number = reqest.GET.get("page",1)
  page_obj = paginator.get_page(page_number)
  return render(reqest,"book/index.html",{"object_list":object_list,"ranking_list":ranking_list,"page_obj":page_obj})

class CreateReviewView(LoginRequiredMixin,CreateView):
  model = Review
  fields = {'book','title','text','rate'}
  template_name = "book/review_form.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['book'] = Book.objects.get(pk=self.kwargs['book_id'])
    return context

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)
  
  def get_success_url(self):
    return reverse('detail-book', kwargs={'pk': self.object.book_id})


# def logout_view(request):
#   logout(request)
#   return redirect("index")
