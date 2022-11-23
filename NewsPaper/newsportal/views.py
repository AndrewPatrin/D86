from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class PostsList(LoginRequiredMixin, ListView):

    model = Post
    ordering = '-published_date'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class NewsList(PostsList):
    template_name = 'news.html'
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs.filter(type="NW")
class ArticlesList(PostsList):
    template_name = 'articles.html'
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs.filter(type="AR")


class PostDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
class NewsDetail(PostDetail):
    model = Post
    template_name = 'new.html'
    context_object_name = 'post'
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs.filter(type="NW")
class ArticleDetail(PostDetail):
    model = Post
    template_name = 'article.html'
    context_object_name = 'post'
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs.filter(type="AR")


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('newsportal.add_post')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
class NewsCreate(PostCreate):
    template_name = 'news_create.html'
    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'NW'
        post.author = self.request.user.author
        return super().form_valid(form)
class ArticleCreate(PostCreate):
    template_name = 'article_create.html'
    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'AR'
        post.author = self.request.user.author
        return super().form_valid(form)


class PostSearch(PostsList):
    template_name = 'post_search.html'
class NewsSearch(PostSearch):
    template_name = 'news_search.html'
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs.filter(type="NW")
class ArticleSearch(PostSearch):
    template_name = 'article_search.html'
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs.filter(type="AR")


class PostEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('newsportal.change_post')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
class NewsEdit(PostEdit):
    template_name = 'news_edit.html'
class ArticleEdit(PostEdit):
    template_name = 'article_edit.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('newsportal.delete_post')
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
class NewsDelete(PostDelete):
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')
class ArticleDelete(PostDelete):
    template_name = 'article_delete.html'
    success_url = reverse_lazy('articles_list')