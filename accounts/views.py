from django.shortcuts import render
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import SignUpForm

class SignupView(CreateView):
  model = User
  form_class = SignUpForm
  template_name = "accounts/signup.html"
  success_url = reverse_lazy("index")