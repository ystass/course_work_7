from rest_framework.pagination import PageNumberPagination


class HabitPaginator(PageNumberPagination):
    page_size = 5  # Количество привычек на странице
    page_size_query_param = "page_size"  # Параметр запроса для указания количества привычек на странице
    max_page_size = 10  # Максимальное количество привычек на странице
