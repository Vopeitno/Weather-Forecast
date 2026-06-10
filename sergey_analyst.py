import csv

def load_daily_temperatures(file_path):
    # Подготавливаем списки и признак начала дневных данных.
    dates = []
    temperatures = []
    daily_data_started = False

    # Находим нужный заголовок и считываем строки после него.
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)

        for row in reader:
            if not row:
                continue

            if (
                len(row) > 1
                and row[0] == "time"
                and row[1] == "temperature_2m_mean (°C)"
            ):
                daily_data_started = True
                continue

            if daily_data_started:
                dates.append(row[0])
                temperatures.append(float(row[1]))

    return dates, temperatures


def build_prefix_sums(temperatures):
    # Строим массив накопленных сумм температур.
    prefix = [0]

    for temperature in temperatures:
        prefix.append(prefix[-1] + temperature)

    return prefix


def range_sum(prefix, left, right):
    # Возвращаем сумму на отрезке с включёнными границами.
    return prefix[right + 1] - prefix[left]


def calculate_monthly_averages(dates, prefix):
    # Подготавливаем словарь и начало первого месяца.
    monthly_averages = {}
    start_index = 0

    # Находим границы каждого месяца и считаем среднюю через префиксные суммы.
    for index in range(1, len(dates) + 1):
        current_month = dates[start_index][5:7]

        if index == len(dates) or dates[index][5:7] != current_month:
            end_index = index - 1
            month_sum = range_sum(prefix, start_index, end_index)
            days_count = end_index - start_index + 1
            monthly_averages[current_month] = month_sum / days_count
            start_index = index

    return monthly_averages


def find_extreme_days(dates, temperatures):
    # Используем первый день как начальные максимум и минимум.
    warmest_date = dates[0]
    warmest_temperature = temperatures[0]
    coldest_date = dates[0]
    coldest_temperature = temperatures[0]

    # За один проход обновляем самый тёплый и самый холодный день.
    for index in range(1, len(temperatures)):
        if temperatures[index] > warmest_temperature:
            warmest_temperature = temperatures[index]
            warmest_date = dates[index]

        if temperatures[index] < coldest_temperature:
            coldest_temperature = temperatures[index]
            coldest_date = dates[index]

    return (
        warmest_date,
        warmest_temperature,
        coldest_date,
        coldest_temperature,
    )