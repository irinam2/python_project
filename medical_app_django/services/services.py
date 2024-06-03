import requests
from bs4 import BeautifulSoup
from .models import Service

def search_services(query):
    """
    Функция для поиска медицинских услуг на основе поискового запроса.

    Args:
        query: Поисковый запрос.

    Returns:
        Список объектов `Service` с найденными услугами.
    """

    url = f"https://med.ru/ru/search/node?keys={query}"
    response = requests.get(url)
    response.raise_for_status()  # Поднимает исключение при ошибке запроса
    soup = BeautifulSoup(response.content, 'html.parser')

    services = []
    # Находим все элементы услуг на странице
    services_elements = soup.find_all('h3', class_='search-result__title')

    print(services_elements)
    for service_element in services_elements:
        # Извлекаем данные из элементов HTML
        clinic = service_element.find('a').text.strip()
        link = service_element.find('a')['href']

        # Создание объекта Service
        service = Service.objects.create(
            clinic=clinic,
            link=link
        )
        services.append(service)

    return services