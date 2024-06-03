"""
Модуль представления функций
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Service, SearchHistory, FavoriteService
from .services import search_services

from .forms import UserRegisterForm

def index(request):
    """
    # Функция для отображения главной страницы
    """
    return render(request, "index.html")

def search(request):
    """
    # Функция для обработки поиска
    """
    # Проверяем, был ли отправлен POST-запрос
    if request.method == "POST":
        # Получаем запрос пользователя
        query = request.POST["query"]
        # Выполняем поиск по услугам
        services = search_services(query)
        # Если пользователь авторизован, сохраняем историю поиска
        if request.user.is_authenticated:
            SearchHistory.objects.create(user=request.user, query=query)

        # Создаем список словарей для каждой услуги
        service_data = []
        for service in services:
            print(service)  # Выводим информацию об услуге (отладочная информация)
            service_data.append(
                {"id": service.id, "name": service.clinic, "link": service.link}
            )
        # Отображаем результаты поиска
        return render(request, "results.html", {"services": service_data})
    # Отображаем форму поиска
    return render(request, "search.html")


def signup(request):
    """
    # Функция для обработки регистрации пользователя
    """
    # Проверяем, был ли отправлен POST-запрос
    if request.method == "POST":
        # Создаем форму регистрации
        form = UserRegisterForm(request.POST)
        # Проверяем валидность формы
        if form.is_valid():
            # Сохраняем нового пользователя
            form.save()
            # Получаем имя пользователя
            username = form.cleaned_data.get("username")
            # Выводим сообщение об успешной регистрации
            messages.success(
                request,
                f"Аккаунт {username} успешно создан! Вы можете войти в систему.",
            )
            # Перенаправляем пользователя на страницу входа
            return redirect("login")
    form = UserRegisterForm()
    # Отображаем форму регистрации
    return render(request, "signup.html", {"form": form})


def login_view(request):
    """
    # Функция для обработки входа пользователя
    """
    # Проверяем, был ли отправлен POST-запрос
    if request.method == "POST":
        # Создаем форму аутентификации
        form = AuthenticationForm(request, data=request.POST)
        # Проверяем валидность формы
        if form.is_valid():
            # Получаем имя пользователя и пароль
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            # Аутентифицируем пользователя
            user = authenticate(username=username, password=password)
            # Если аутентификация успешна
            if user is not None:
                # Авторизуем пользователя
                login(request, user)
                # Выводим сообщение о успешном входе
                messages.success(request, f"Добро пожаловать, {username}!")
                # Перенаправляем пользователя на главную страницу
                return redirect("index")
            # Выводим сообщение об ошибке аутентификации
            messages.error(request, "Неверный логин или пароль.")
        else:
            # Выводим сообщение об ошибке валидации формы
            messages.error(request, "Неверный формат данных.")
    # Создаем пустую форму аутентификации
    form = AuthenticationForm()
    # Отображаем форму входа
    return render(request, "login.html", {"form": form})

def logout_view(request):
    """
    # Функция для обработки выхода пользователя
    """
    # Выводим пользователя из системы
    logout(request)
    # Выводим сообщение о успешном выходе
    messages.success(request, "Вы вышли из системы!")
    # Перенаправляем пользователя на главную страницу
    return redirect("index")


def profile(request):
    """
    # Функция для отображения профиля пользователя
    """
    # Проверяем, авторизован ли пользователь
    if request.user.is_authenticated:
        # Получаем информацию о пользователе
        user = request.user
        # Получаем список избранных услуг
        favorite_services = FavoriteService.objects.filter(user=user)
        # Получаем историю поиска (последние 5 поисков)
        search_history = SearchHistory.objects.filter(user=user).order_by(
            "-created_at"
        )[
            :5
        ]
        # Отображаем страницу профиля
        return render(
            request,
            "profile.html",
            {
                "user": user,
                "favorite_services": favorite_services,
                "search_history": search_history,
            },
        )
    # Перенаправляем пользователя на страницу входа
    return redirect("login")

def service_details(request, service_id):
    """
    # Функция для отображения подробной информации об услуге
    """
    # Получаем информацию об услуге по ее ID
    service = Service.objects.get(pk=service_id)
    # Отображаем страницу с подробной информацией об услуге
    return render(request, "service_details.html", {"service": service})


def add_to_favorite(request, service_id):
    """
    # Функция для добавления услуги в избранное
    """
    # Проверяем, авторизован ли пользователь
    if request.user.is_authenticated:
        # Получаем информацию об услуге по ее ID
        service = Service.objects.get(pk=service_id)
        # Добавляем услугу в избранное
        FavoriteService.objects.create(user=request.user, service=service)
        # Выводим сообщение о успешном добавлении услуги в избранное
        messages.success(request, f"Услуга '{service.clinic}' добавлена в избранное.")
    else:
        # Выводим сообщение о необходимости авторизации
        messages.warning(
            request, "Пожалуйста, авторизуйтесь, чтобы добавить услугу в избранное."
        )
    # Перенаправляем пользователя на страницу профиля
    return redirect("profile")


def remove_from_favorite(request, service_id):
    """
    # Функция для удаления услуги из избранного
    """
    # Проверяем, авторизован ли пользователь
    if request.user.is_authenticated:
        # Получаем информацию об услуге по ее ID
        service = Service.objects.get(pk=service_id)
        # Удаляем услугу из избранного
        FavoriteService.objects.filter(user=request.user, service=service).delete()
        # Выводим сообщение о успешном удалении услуги из избранного
        messages.success(request, f"Услуга '{service.name}' удалена из избранного.")
    else:
        # Выводим сообщение о необходимости авторизации
        messages.warning(
            request, "Пожалуйста, авторизуйтесь, чтобы удалить услугу из избранного."
        )
    # Перенаправляем пользователя на страницу профиля
    return redirect("profile")
