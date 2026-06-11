"""
Функционал включает в себя:
- скользящее среднее температур через очередь
- поиск температурных аномалий (самые тёплые и холодные недели подряд)
- определение температурных трендов по месяцам (потепление/похолодание)
"""

from collections import deque

def smooth_temperatures(dates, temperatures, window_size=7):
    """
    Сглаживает график температур, вычисляя среднее значение за окно заданного размера.
    Возвращает новый список, где каждая температура — это среднее значение за последние `window_size` дней.
    """
    # Очередь, в которую помещается ровно window_size градусников
    queue = deque()
    smoothed_temps = []
    
    for temp in temperatures:
        # Кладем новую температуру в конец очереди (справа)
        queue.append(temp)
        # Если градусников в коробке стало больше, чем нужно, убираем старый (левый), чтобы освободить место
        if len(queue) > window_size:
            queue.popleft()
        # Считаем среднее для тех температур, что сейчас лежат в коробке
        current_average = sum(queue) / len(queue)
        # Округляем до 2 знаков после запятой и сохраняем в итоговый список
        smoothed_temps.append(round(current_average, 2))
        
    return smoothed_temps


def find_temperature_anomalies(dates, temperatures, window_size=7):
    """
    Ищет самые экстремальные периоды (недели) в массиве данных.
    Возвращает два словаря (самый теплый период и самый холодный период) с датами начала, конца и средней температурой. 
    Если данных меньше окна, возвращает (None, None).
    """
    if len(temperatures) < window_size:
        return None, None
    # Ставим начальные значения, самая теплая сумма сначала искусственно занижена, самая холодная завышена.
    max_sum = float('-inf') 
    min_sum = float('inf')
    # Для хранения индекса дней, с которых начинаются аномальные недели
    hottest_idx = 0
    coldest_idx = 0
    
    # Берем окно размеров в 7 дней и двигаем вниз.
    # Останавливаемся так, чтобы впереди оставалось ровно 7 дней
    for i in range(len(temperatures) - window_size + 1):
        # Берем часть списка длиной в 7 дней 
        current_week_temps = temperatures[i : i + window_size]
        current_sum = sum(current_week_temps)
        # Проверяем, побила ли эта неделя рекорд тепла
        if current_sum > max_sum:
            max_sum = current_sum
            hottest_idx = i
        # Проверяем, побила ли эта неделя рекорд холода
        if current_sum < min_sum:
            min_sum = current_sum
            coldest_idx = i
            
    # Собираем словари с результатами
    hottest_period = {
        "start_date": dates[hottest_idx],
        "end_date": dates[hottest_idx + window_size - 1],
        "average_temp": round(max_sum / window_size, 2)
    }
    coldest_period = {
        "start_date": dates[coldest_idx],
        "end_date": dates[coldest_idx + window_size - 1],
        "average_temp": round(min_sum / window_size, 2)
    }
    return hottest_period, coldest_period

def determine_monthly_trend(monthly_averages):
    """
    Сравнивает средние температуры текущего и прошлого месяца, определяя тренд.
    Возвращает: список строк с текстовым описанием изменений и стрелочками.
    """
    # Разделяем словарь на два списка: один с названиями месяцев, другой с температурами
    months = list(monthly_averages.keys())
    temps = list(monthly_averages.values())
    trends_output = []
    # Начинаем со второго месяца (индекс 1), чтобы сравниить с первым (индекс 0)
    for i in range(1, len(months)):
        prev_month = months[i - 1]
        curr_month = months[i]
        prev_temp = temps[i - 1]
        curr_temp = temps[i]
        if curr_temp > prev_temp:
            arrow = "↑"
            trend_text = "потепление"
        elif curr_temp < prev_temp:
            arrow = "↓"
            trend_text = "похолодание"
        else:
            arrow = "→"
            trend_text = "без изменений"
            
        # Формируем итоговую строку для вывода
        trends_output.append(f"{prev_month} -> {curr_month}: {curr_temp}°C {arrow} {trend_text}")
        
    return trends_output

# Блок для проверки работы функций
if __name__ == "__main__":
    # Тестовые данные (простые числа для быстрой проверки логики)
    test_dates = ["01.01", "02.01", "03.01", "04.01", "05.01", "06.01", "07.01"]
    test_temps = [-10, -12, -15, -10, -5, -2, 0]
    
    print("Средняя температура за 3 дня:", smooth_temperatures(test_dates, test_temps, window_size=3))
    
    hot, cold = find_temperature_anomalies(test_dates, test_temps, window_size=3)
    print("\nТеплая аномалия:", hot)
    print("Холодная аномалия:", cold)
    
    print("\nТренды по месяцам:")
    test_months = {"Янв": -10, "Фев": -5, "Мар": 2, "Апр": -1}
    for trend in determine_monthly_trend(test_months):
        print(trend)