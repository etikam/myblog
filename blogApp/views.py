
# from django.contrib import messages
# # Create your views here.
# from django.views import generic
# def index(request):
#     # recover all articles
#     articles = Article.objects.all()
#     form = ArticleForm()
    
#     if request.method == "POST":
#         form = ArticleForm(request.POST,request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request,"Article Ajouté avec succès")
#             return redirect(index)
#         else:
#             messages.error(request,form.errors)
#     context = {
#         'articles':articles,
#         'form':form
#     }
    
#     return render(request,'blogApp/index.html',context)


# def addArticle(request):
#     context = {}
#     if request.method == "POST":
#         form = ArticleForm(request.POST)
#         if form.is_valid():
#             form_data = form.cleaned_data
#             article = Article(**form_data)
#             article.save()
#             messages.success(request,"Article Ajouté avec succès")
#             return redirect(index)
#         else:
#             messages.error(request,form.errors)
#     else:
#         # form = ArticleForm()
#         # context['form']=form
#         messages.error(request,"method not allowed")
#         return redirect(index)
#     return render(request,"blogApp/index.html",context)
        
    
            
# def deleteArticle(request,id):
#     article_to_delete = get_object_or_404(Article,id=id)
#     if article_to_delete:
#         article_to_delete.delete()
#         messages.success(request,"Vous avez supprimé un article")
#         return redirect('home')
#     return render(request,"blogApp/index.html")


# def editArticle(request, id):
#     article_to_edit = get_object_or_404(Article, id=id)

#     # Si la requête est une soumission de formulaire (POST)
#     if request.method == "POST":
#         # Remplir le formulaire avec les données envoyées par la requête POST
#         form = ArticleForm(request.POST, instance=article_to_edit)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Article modifié avec succès")
#             return redirect('home')
#         else:
#             messages.error(request, "Il y a eu une erreur dans la soumission du formulaire")
#     else:
#         # Si la requête est GET, pré-remplir le formulaire avec les données de l'article
#         form = ArticleForm(instance=article_to_edit)

#     context = {
#         'form': form,
#         'article': article_to_edit
#     }
    
#     return render(request, "blogApp/editArticles.html", context)




from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import (
                                    ListView, 
                                    CreateView,
                                    DeleteView,
                                    UpdateView,
                                    View,
                                    DetailView
                                )
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404,reverse
from .models import Article,Comment, Category
from .forms import ArticleForm,CommentForm


class ArticleListCreateView(View):
    template_name = 'blogApp/index.html'
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        articles = Article.objects.all().order_by('-date')
        form = ArticleForm()
        category = Category.objects.all()
        return render(request, self.template_name, {'articles': articles, 
                                                    'form': form,
                                                    'categories':category})

    # def post(self, request, *args, **kwargs):
    #     form = ArticleForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, "Article ajouté avec succès !")
    #         return redirect(self.success_url)
    #     else:
    #         messages.error(request, "Erreur lors de l'ajout de l'article.")
    #         articles = Article.objects.all()
    #         return render(request, self.template_name, {'articles': articles, 'form': form})

class ArticleDeleteView(LoginRequiredMixin,DeleteView):
    model = Article
    success_url = reverse_lazy('home')
    template_name ='blogApp/article_confirm_delete.html'
    def delete(self, request, *args, **kwargs):
        messages.success(request, "Article supprimé avec succès !")
        return super().delete(request, *args, **kwargs)




class ArticleUpdateView(LoginRequiredMixin,UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blogApp/article_form.html' 
    success_url = reverse_lazy('home')
    
    

    
class ArticleCreateView(LoginRequiredMixin,CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blogApp/article_form.html'  # Template à créer
    success_url = reverse_lazy('home')
    
    def post(self, request, *args: str, **kwargs) :
        if not request.user.is_authenticated:
           return redirect('login') 
        else: 
            user= request.user
        
        form = ArticleForm(request.POST,request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = user
            form.save()
            messages.success(request,'Vous avez ajouter un article avec succès')
            return redirect('home')
    
    def get(self, request, *args: str, **kwargs):
        if not request.user.is_authenticated:
           return redirect('login') 
        else:
            return super().get(request, *args, **kwargs)
    
    
    
class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blogApp/article_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.object
        categories = article.category.all()
        related_articles = Article.objects.filter(category__in=categories).exclude(pk=article.pk).distinct()
        
        # Ajouter les commentaires associés à l'article
        comments = Comment.objects.filter(article=article)
        
        # Formulaire de commentaire vide pour l'affichage
        context['comment_form'] = CommentForm()
        context['comments'] = comments
        context['related_articles'] = related_articles
        
        return context

    # Ici je gère la soumission par post du formulaire de soumission des commentaires

    def post(self, request, *args, **kwargs):
        if request.user:
            user = request.user
        else:
            return redirect('account:login')
        article = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.user = user
            comment.save()
            return redirect(reverse('detail-article', kwargs={'pk': article.pk}))
        else:
            return self.get(request, *args, **kwargs)



#  Fonction de traitement des commentaire
class CommentDeleteView(LoginRequiredMixin,DeleteView):
    model = Comment
    template_name = 'blogApp/comment_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        comment = self.get_object()
        article_id = comment.article.id  # Récupère l'ID de l'article lié au commentaire
        messages.success(request, "Commentaire supprimé avec succès !")
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        comment = self.get_object()
        return reverse_lazy('detail-article', kwargs={'pk': comment.article.id})


# Mise à jour du commentaire 
class CommentUpdateView(LoginRequiredMixin,UpdateView):
    model = Comment
    model = Comment
    form_class = CommentForm
    template_name = 'blogApp/comment_form.html'

    def form_valid(self, form):
        messages.success(self.request, "Commentaire modifié avec succès !")
        return super().form_valid(form)

    def get_success_url(self):
        comment = self.get_object()
        return reverse_lazy('detail-article', kwargs={'pk': comment.article.id})
    
