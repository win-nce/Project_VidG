from django.contrib import admin
from .models import Game, Studio, Genre, Reaction, Review, Report

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Studio)
class StudioAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    search_fields = ('name', 'country')

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'studio')
    search_fields = ('name', 'author__username', 'studio__name')
    list_filter = ('genre', 'studio')
    filter_horizontal = ('genre',)  # для выбора жанров в админке
    autocomplete_fields = ['studio']  # чтобы удобно искать студии
    readonly_fields = ('id',)

@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'reaction_type')
    list_filter = ('reaction_type',)
    search_fields = ('user__username', 'game__name')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('game', 'user', 'created_at')
    search_fields = ('game__name', 'user__username')
    list_filter = ('created_at',)

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'theme', 'created_at')
    list_filter = ('theme', 'created_at')
    search_fields = ('user__username', 'game__name', 'description')
