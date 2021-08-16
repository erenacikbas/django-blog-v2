# Imports
from django.shortcuts import render
from django.views import generic
# Importing Models
from .models import Post, BlogAuthor, Configuration, PostComment
# Imports for Authentication Views
from django.shortcuts import render, redirect
from .forms import NewUserForm, UserLoginForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, \
    PasswordChangeForm  # add this
#
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse, reverse_lazy


# Create your views here.

# Home View
def index(request):
    posts = Post.objects.all()
    index = Configuration.objects.all()[0]
    """
    View function for home page of site.
    """
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    context = {'posts': posts, 'num_visits': num_visits, 'index': index}
    # Render the HTML template index.html
    return render(request, 'index.html', context=context)


# About Page View
def about(request):
    about = Configuration.objects.all()[0]
    """
    View function for about page of site.
    """
    context = {'about': about}
    return render(request, 'about.html', context=context)


# Contact Page View
def contact(request):
    contact = Configuration.objects.all()[0]
    """
    View function for about page of site.
    """
    context = {'contact': contact}
    return render(request, 'contact.html', context=context)


# Authentication Views
def register_request(request):
    bg = Configuration.objects.all()[0]
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("/")
    else:
        form = NewUserForm()

    return render(request=request,
                  template_name="registration/register.html",
                  context={
                      "register_form": form,
                      "bg": bg
                  })


def login_request(request):
    bg = Configuration.objects.all()[0]
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("/")
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = UserLoginForm()
    return render(request=request,
                  template_name="registration/login.html",
                  context={
                      "login_form": form,
                      "bg": bg
                  })


def logout_request(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect("/")


from django.contrib.auth.views import PasswordChangeView


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('index')
    template_name = "registration/change_password.html"


# --------

# Post Detail View
class PostDetailView(generic.DetailView):
    """
    Generic class-based detail view for a blog.
    """
    model = Post


# Post by Author View
from django.shortcuts import get_object_or_404


class PostListbyAuthorView(generic.ListView):
    """
    Generic class-based view for a list of blogs posted by a particular BlogAuthor.
    """
    model = Post
    paginate_by = 5
    template_name = 'blog/post/post_list_by_author.html'

    def get_queryset(self):
        """
        Return list of Blog objects created by BlogAuthor (author id specified in URL)
        """
        id = self.kwargs['pk']
        target_author = get_object_or_404(BlogAuthor, pk=id)
        return Post.objects.filter(author=target_author)

    def get_context_data(self, **kwargs):
        """
        Add BlogAuthor to context so they can be displayed in the template
        """
        # Call the base implementation first to get a context
        context = super(PostListbyAuthorView, self).get_context_data(**kwargs)
        # Get the blogger object from the "pk" URL parameter and add it to the context
        context['blogger'] = get_object_or_404(BlogAuthor,
                                               pk=self.kwargs['pk'])
        return context


# Post Comment Create View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView


class PostCommentCreate(LoginRequiredMixin, CreateView):
    """
    Form for adding a blog comment. Requires login.
    """
    model = PostComment
    fields = [
        'comment',
    ]

    def get_context_data(self, **kwargs):
        """
        Add associated blog to form template so can display its title in HTML.
        """
        # Call the base implementation first to get a context
        context = super(PostCommentCreate, self).get_context_data(**kwargs)
        # Get the blog from id and add it to the context
        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        """
        Add author and associated blog to form data before setting it as valid (so it is saved to model)
        """
        # Add logged-in user as author of comment
        form.instance.author = self.request.user
        # Associate comment with blog based on passed id
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        # Call super-class form validation behaviour
        return super(PostCommentCreate, self).form_valid(form)

    def get_success_url(self):
        """
        After posting comment return to associated blog.
        """
        return reverse('post-detail', kwargs={
            'pk': self.kwargs['pk'],
        })
