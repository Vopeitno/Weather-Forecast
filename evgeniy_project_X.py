"""
- сортировка месяцев по средней температуре,
- бинарное дерево поиска по температуре,
- рекурсивный поиск дней выше заданного порога,
- стек Undo для отмены последнего сохранённого состояния
"""

from copy import deepcopy


class TemperatureNode:
    """Узел бинарного дерева поиска для температуры"""

    def __init__(self, temperature, date):
        """
        Создаёт новый узел дерева.
        
        В одном узле хранится одна температура
        Если такая температура встречается в разные дни,
        даты будут храниться в списке dates
        """
        self.temperature = temperature
        self.dates = [date]
        self.left = None
        self.right = None


def sort_months_by_average(monthly_averages):
    """
    Сортирует месяцы по средней температуре.
    На вход подаётся словарь, где ключ - месяц,
    а значение - средняя температура за этот месяц.
    Возвращается список пар:
    (месяц, средняя температура).
    """
    # Сортируем по средней температуре, от большей к меньшей
    sorted_months = sorted(
        monthly_averages.items(),
        key=lambda month_data: month_data[1],
        reverse=True
    )

    return sorted_months


def insert_temperature(root, temperature, date):
    """
    Добавляет температуру и дату в бинарное дерево поиска
    Меньшие температуры идут в левое поддерево,
    большие температуры - в правое поддерево
    """
    # Если дошли до пустого места, создаём новый узел
    if root is None:
        return TemperatureNode(temperature, date)

    # Если температура меньше текущей, идём влево
    if temperature < root.temperature:
        root.left = insert_temperature(root.left, temperature, date)

    # Если температура больше текущей, идём вправо
    elif temperature > root.temperature:
        root.right = insert_temperature(root.right, temperature, date)

    # Если температура уже есть, просто добавляем новую дату
    else:
        root.dates.append(date)

    return root


def build_temperature_tree(dates, temperatures):
    """
    Строит бинарное дерево поиска по датам и температурам
    dates - список дат
    temperatures - список температур
    """
    root = None

    # Проходим по всем температурам и добавляем их в дерево
    for index in range(len(temperatures)):
        root = insert_temperature(root, temperatures[index], dates[index])

    return root


def find_days_above_threshold(root, threshold):
    """
    Рекурсивно ищет все дни, где температура выше заданного порога
    Возвращает список кортежей: (дата, температура)
    """
    # Если узла нет, искать нечего
    if root is None:
        return []

    result = []

    if root.temperature > threshold:
        # В левом поддереве могут быть подходящие температуры,
        # поэтому тоже его проверяем
        result.extend(find_days_above_threshold(root.left, threshold))

        # Добавляем все даты, которые относятся к текущей температуре
        for date in root.dates:
            result.append((date, root.temperature))

        # В правом поддереве температуры точно больше текущей,
        # поэтому его тоже обходим
        result.extend(find_days_above_threshold(root.right, threshold))

    else:
        # Если текущая температура не подходит,
        # слева температуры ещё меньше, поэтому идём только вправо
        result.extend(find_days_above_threshold(root.right, threshold))

    return result


def save_state(history, data):
    """
    Сохраняет текущее состояние данных в стек Undo
    history - список, который используется как стек
    data - данные, которые нужно сохранить
    """
    # Кладём копию данных, чтобы потом изменения не сломали сохранённое состояние
    history.append(deepcopy(data))


def undo(history):
    """
    Отменяет последнее сохранённое состояние
    Если стек пустой, возвращает None
    """
    # Если в истории ничего нет, отменять нечего
    if len(history) == 0:
        return None

    # pop удаляет и возвращает последний добавленный элемент
    return history.pop()