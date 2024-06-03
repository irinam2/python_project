import requests
from bs4 import BeautifulSoup
from .models import Service

def search_services(query):
    """
    Функция для поиска медицинских услуг на основе поискового запроса на сайте "Zoon.ru".

    Args:
        query: Поисковый запрос.

    Returns:
        Список объектов `Service` с найденными услугами.
    """

    url = f"https://zoon.ru/search/?city=msk&query={query}"
    response = requests.get(url)
    response.raise_for_status()  # Поднимает исключение при ошибке запроса
    soup = BeautifulSoup(response.content, 'html.parser')

    services = []
    # Находим все элементы услуг на странице
    services_elements = soup.find_all('a', class_='title-link js-item-url')
    for service_element in services_elements:
        # Извлекаем данные из элементов HTML
        print(service_element)
        clinic = service_element.text.strip()
        link = service_element['href']

        # Создание объекта Service
        service = Service.objects.create(
            clinic=clinic,
            link=link
        )
        services.append(service)

    return services