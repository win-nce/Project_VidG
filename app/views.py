from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from app.models import Game, Studio, Reaction, Review
from app.forms import ReportForm, CustomUserCreationForm

# Главняа
class GameListView(ListView):
    model = Game
    template_name = "app/game_list.html"
    context_object_name = "games" # Задали перемную для next usage in templates
    ordering = ["-id"] # по убыванию
    paginate_by = 10


# Каталог с выбором разделов
class CatalogueView(ListView):
    template_name = "app/catalogue.html"
    model = Game
    context_object_name = 'games'
    
    
# Поиск
def search(request):
    query = request.GET.get('q')  # параметр который мы забираем из /search/?q=doom
    games = Game.objects.filter(name__icontains=query) if query else [] # если нашел (name__icontains=query) то выведет
    studios = Studio.objects.filter(name__icontains=query) if query else [] # если не нашел то пустой список (if query else []) 

    return render(request, 'app/search_results.html', {
        'query': query,
        'games': games,
        'studios': studios
    })

#------------------------------------------------------------------------------------------------------------------------
# Просмотр инфы студий и разрабов
class StudioListView(ListView):
    model = Studio
    template_name = "app/studio_list.html"
    context_object_name = "studios"
    ordering = ["name"]
    paginate_by = 10

class StudioDetailView(DetailView):
    model = Studio
    template_name = "app/studio_detail.html"
    context_object_name = "studio"


#------------------------------------------------------------------------------------------------------------------------
# Просмотр игр с ревьюшками и реакциями
class GameDetailView(DetailView):
    model = Game
    template_name = "app/game_detail.html"
    context_object_name = "game"


#------------------------------------------------------------------------------------------------------------------------
# регистрация
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(
        request,
        "app/register.html",
        {"form": form}
    )

class CustomLoginView(LoginView):
    template_name = "app/login.html"

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("login")


#------------------------------------------------------------------------------------------------------------------------
# Реакции
@login_required
def add_reaction(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    reaction_type = request.POST.get('reaction_type')  # 'нравится' или 'ненравится'

    reaction, created = Reaction.objects.update_or_create(
        user=request.user,
        game=game,
        defaults={'reaction_type': reaction_type}
    )
    return redirect('game_detail', pk=game.id)


#------------------------------------------------------------------------------------------------------------------------
# добавление ревью к Игре
class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['content']
    template_name = 'app/review_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.game_id = self.kwargs['game_id']
        return super().form_valid(form)

    def get_success_url(self):
        if self.object.game:
            return reverse_lazy('game_detail', kwargs={'pk': self.object.game.id})
        else:
            return reverse_lazy('index')

    def test_func(self):
        return self.request.user == self.get_object().user
# Редактирование своего ревью
class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    fields = ['content']
    template_name = 'app/review_form.html'

    def get_success_url(self):
        return reverse_lazy('game_detail', kwargs={'pk': self.object.game.id})

    def test_func(self):
        return self.request.user == self.get_object().user

# Удаление ревью 
class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = 'app/review_delete.html'
    context_object_name = 'review'

    def get_success_url(self):
        return reverse_lazy('game_detail', kwargs={'pk': self.object.game.id})

    # Проверка: только автор может удалить свою ревью
    def test_func(self):
        review = self.get_object()
        return self.request.user == review.user


#------------------------------------------------------------------------------------------------------------------------
# создание репорта
@login_required
def create_report(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    
    if request.method == "POST":  # исправлено на заглавные буквы
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.game = game
            report.save()
            return redirect("game_detail", pk=game_id)  # или имя url для просмотра игры
    else:
        form = ReportForm()

    return render(request, "app/report_form.html", {"form": form, "game": game})


#------------------------------------------------------------------------------------------------------------------------
# Пользовательский Профиль
class ProfileView(LoginRequiredMixin, ListView):
    model = Review
    template_name = 'app/profile.html'
    context_object_name = 'reviews'

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user).select_related('game')

