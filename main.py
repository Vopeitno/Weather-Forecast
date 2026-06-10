import csv
#импорт функций из файла сергея
from sergey_analyst import (
    load_daily_temperatures,
    build_prefix_sums,
    calculate_monthly_averages,
    find_extreme_days,
)

def main():
    # Загружаем данные и строим префиксные суммы.
    file_path = "data/weather_spb_2025.csv"
    dates, temperatures = load_daily_temperatures(file_path)
    if not dates:
        print("Дневные данные не найдены в файле.")
        return
    prefix = build_prefix_sums(temperatures)

    # Показываем меню, пока пользователь не завершит программу.
    while True:
        print()
        print("1. Показать среднюю температуру за каждый месяц")
        print("2. Показать самый тёплый и самый холодный день")
        print("3. Завершить программу")

        choice = input("Выберите пункт меню: ")

        if choice == "1":
            monthly_averages = calculate_monthly_averages(dates, prefix)

            print()
            print("Средние температуры по месяцам:")
            for month, average in monthly_averages.items():
                print(f"Месяц {month}: {average:.2f} °C")

        elif choice == "2":
            extreme_days = find_extreme_days(dates, temperatures)
            warmest_date = extreme_days[0]
            warmest_temperature = extreme_days[1]
            coldest_date = extreme_days[2]
            coldest_temperature = extreme_days[3]

            print()
            print(
                f"Самый тёплый день: {warmest_date}, "
                f"температура: {warmest_temperature:.1f} °C"
            )
            print(
                f"Самый холодный день: {coldest_date}, "
                f"температура: {coldest_temperature:.1f} °C"
            )

        elif choice == "3":
            print("Программа завершена.")
            break

        else:
            print("Такого пункта меню нет.")


if __name__ == "__main__":
    main()
