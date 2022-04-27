from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .models import Post

# This function changes the due_date field to something more readable
# that looks like this '01 January 2022, 11:59'.
def date_fixer(input_posts):
    new_posts = input_posts
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    for post in new_posts:
        try:
            date_time_list = post.due_date.split("T")
            date_list = date_time_list[0].split("-")

            month_int = int(date_list[1])
            month = months[month_int-1]

            date_string = date_list[2] + " " + month + " " + date_list[0] + ", " + date_time_list[1]
            post.due_date = date_string
        except:
            post.due_date = "Invalid Date"

    return new_posts

#posts from the database we are passing to the view.
#posts = date_fixer()

# Create your views here.
# def home(request):
#     context = {
#         'title':'wyatt',
#         'posts':posts
#     }

#   return render(request, 'tracker/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'tracker/home.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        if self.request.user.is_authenticated:
            posts = Post.objects.filter(author=self.request.user).order_by('due_date')
            posts = date_fixer(posts)
            return posts
        else:
            return []

class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'description', 'due_date']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'description', 'due_date']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()

        if self.request.user == post.author:
            return True
        else:
            return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()

        if self.request.user == post.author:
            return True
        else:
            return False


def about(request):
    return render(request, 'tracker/about.html')