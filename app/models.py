from django.db import models
from django.contrib.auth.models import User
# Отдельное для жанров
class Genre(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name="Жанр")

    def __str__(self):
        return self.name

# Разрабы
class Studio(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name="Студия разработчик")
    country = models.CharField(max_length=128, blank=True, verbose_name="Страна Разработки")
    description = models.TextField(blank=True, null=True, verbose_name="Описание студии")

    def __str__(self):
        return self.name



# Основная модель, карточки с играми
class Game(models.Model):
    """
    Модель игр, хранение игр
    Attributes:
        name: Поле название игры,
        image: Поле для вложения картинки,
        description: Поле Контента Поста,
        genre: Поле конкретного жанра,
        studio: Поле для вписания студии кто разработал игру,
        author: Тот кто добавил игру в каталог
    """
    # игра может иметь несколько жанров поэтому ManyToManyField() 
    name = models.CharField(max_length=256, verbose_name="Название Игры")
    image = models.ImageField(upload_to='game_covers/', null=True, blank=True, verbose_name="Обложка Игры")
    description = models.CharField(max_length=3000, verbose_name="Описание Игры")
    genre = models.ManyToManyField(Genre, related_name='games', verbose_name="Жанры Игры")
    studio = models.ForeignKey(Studio, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Студия разработчик")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор") 
    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name_plural = "Игры"





# Реакции
class Reaction(models.Model):
    """
        Модель Реакций на игру, Нравится\Ненравится.

        Attributes:
            user: Автор Реакции,
            game: Игра на которую поставили реакшен,
            reaction_type: Тип нашей Реакции,
    """

    REACTION_CHOICES = [
        ('like', 'Нравится'),
        ('dislike', 'Ненравится'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='reactions')
    reaction_type = models.CharField(max_length=7, choices=REACTION_CHOICES, verbose_name="Тип реакции")
    
    #Это ограничение, которое запрещает ставить две одинаковые реакции. Один пользователь - одна реакция на одну игру.
    class Meta:
        unique_together = ('user', 'game')

    # типа уведомления, get_reaction_type_display встроенный метод, нигде не прописываем его.
    def __str__(self):
        return f"{self.user.username} поставил {self.get_reaction_type_display()} игре {self.game.name}"



# Ревьюшки для карточек
class Review(models.Model):
    """
        Моделька Ревьюшек привязана к посту, можно оставлять свои впечатления.

        Attributes:
            name: Игра к которой написана ревьюшка,
            content: Содержимое Ревью,
            user: Автор Ревью,
            created_at: Время того когда Ревью.
    """
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="reviews", verbose_name="Игры")
    content = models.TextField(verbose_name='Содержимое')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата Создания Ревью")

    def __str__(self):
        return f"{self.game.name} - {self.user.username}"

    class Meta:
        verbose_name_plural = "Комментарии"


# Жалоба 
class Report(models.Model):
    THEME_CHOICES = [
        ('wrong_info', 'Неверная информация'),
        ('wrong_studio', 'Неверная студия'),
        ('wrong_genre', 'Неподходящие жанры'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    game = models.ForeignKey('Game', on_delete=models.CASCADE, verbose_name="Игра")
    theme = models.CharField(max_length=20, choices=THEME_CHOICES, verbose_name="Тема жалобы")
    description = models.TextField(verbose_name="Описание жалобы", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Жалоба от {self.user.username} по игре {self.game.name} — {self.get_theme_display()}"





