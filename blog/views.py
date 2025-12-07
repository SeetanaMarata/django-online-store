from django import forms
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .models import BlogPost


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ["title", "content", "preview", "is_published"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите заголовок статьи",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 10,
                    "placeholder": "Напишите содержимое статьи...",
                }
            ),
            "preview": forms.FileInput(attrs={"class": "form-control"}),
            "is_published": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class BlogPostListView(ListView):
    """CBV для списка блоговых записей"""

    model = BlogPost
    template_name = "blog/post_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        # Выводим только опубликованные статьи
        return BlogPost.objects.filter(is_published=True)


class BlogPostDetailView(DetailView):
    """CBV для детального просмотра блоговой записи"""

    model = BlogPost
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        # Получаем объект и увеличиваем счетчик просмотров
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()
        return obj


class BlogPostCreateView(CreateView):
    """CBV для создания блоговой записи"""

    model = BlogPost
    form_class = BlogPostForm
    template_name = "blog/post_form.html"
    success_url = reverse_lazy("blog:post_list")


class BlogPostUpdateView(UpdateView):
    """CBV для редактирования блоговой записи"""

    model = BlogPost
    form_class = BlogPostForm
    template_name = "blog/post_form.html"

    def get_success_url(self):
        # После редактирования перенаправляем на страницу статьи
        return reverse_lazy("blog:post_detail", kwargs={"pk": self.object.pk})


class BlogPostDeleteView(DeleteView):
    """CBV для удаления блоговой записи"""

    model = BlogPost
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("blog:post_list")
