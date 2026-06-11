#импорт функций из файла сергея
from sergey_analyst import (
    load_daily_temperatures,
    build_prefix_sums,
    calculate_monthly_averages,
    find_extreme_days,
)
#Импорт функций из файла ксении
from ksenia_dop_trends import (
    smooth_temperatures,
    find_temperature_anomalies,
    determine_monthly_trend,
)
#Импорт функций из файла евгения
from evgeniy_project_X import (
    sort_months_by_average,
    build_temperature_tree,
    find_days_above_threshold,
    save_state,
    undo,
)

def main():
    # Загружаем данные и строим префиксные суммы.
    file_path = "data/weather_spb_2025.csv"
    dates, temperatures = load_daily_temperatures(file_path)
    if not dates:
        print("Дневные данные не найдены в файле.")
        return
    prefix = build_prefix_sums(temperatures)
    monthly_averages = calculate_monthly_averages(dates, prefix)
    temperature_tree = build_temperature_tree(dates, temperatures)
    history = []

    # Показываем меню, пока пользователь не завершит программу.
    while True:
        print()
        print("1. Показать среднюю температуру за каждый месяц")
        print("2. Показать самый тёплый и самый холодный день")
        print("3. Применить скользящее среднее температур через очередь")
        print("4. Найти самые тёплые и холодные недели подряд")
        print("5. Определить температурные тренды по месяцам")
        print("6. Отсортировать месяцы по средней температуре")
        print("7. Найти дни с температурой выше заданного порога")
        print("8. Отменить последнее сглаживание температур")
        print("9. Завершить программу")

        choice = input("Выберите пункт меню: ")

        if choice == "1":
            print("\nСредние температуры по месяцам:")
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
            # Сохраняем данные перед применением сглаживания.
            save_state(history, temperatures)
            temperatures = smooth_temperatures(
                dates,
                temperatures,
                window_size=7,
            )

            # Пересчитываем данные после изменения температур.
            prefix = build_prefix_sums(temperatures)
            monthly_averages = calculate_monthly_averages(dates, prefix)
            temperature_tree = build_temperature_tree(dates, temperatures)

            print("\nСкользящее среднее за 7 дней:")
            for index in range(len(dates)):
                print(f"{dates[index]}: {temperatures[index]:.2f} °C")

        elif choice == "4":
            hottest_period, coldest_period = find_temperature_anomalies(
                dates,
                temperatures,
                window_size=7,
            )

            print("\nСамая тёплая неделя:")
            print(
                f"{hottest_period['start_date']} - "
                f"{hottest_period['end_date']}, "
                f"средняя температура: "
                f"{hottest_period['average_temp']:.2f} °C"
            )
            print("Самая холодная неделя:")
            print(
                f"{coldest_period['start_date']} - "
                f"{coldest_period['end_date']}, "
                f"средняя температура: "
                f"{coldest_period['average_temp']:.2f} °C"
            )

        elif choice == "5":
            trends = determine_monthly_trend(monthly_averages)

            print("\nТемпературные тренды:")
            for trend in trends:
                print(trend)

        elif choice == "6":
            sorted_months = sort_months_by_average(monthly_averages)

            print("\nМесяцы от самого тёплого к самому холодному:")
            for month, average in sorted_months:
                print(f"Месяц {month}: {average:.2f} °C")

        elif choice == "7":
            try:
                threshold = float(input("Введите температурный порог: "))
            except ValueError:
                print("Температурный порог должен быть числом.")
                continue

            days_above_threshold = find_days_above_threshold(
                temperature_tree,
                threshold,
            )

            print()
            if days_above_threshold:
                print(f"Дни с температурой выше {threshold:.1f} °C:")
                for date, temperature in days_above_threshold:
                    print(f"{date}: {temperature:.1f} °C")
            else:
                print("Дни с температурой выше порога не найдены.")

        elif choice == "8":
            restored_temperatures = undo(history)

            if restored_temperatures is None:
                print("Нет сохранённого состояния для отмены.")
            else:
                temperatures = restored_temperatures
                prefix = build_prefix_sums(temperatures)
                monthly_averages = calculate_monthly_averages(dates, prefix)
                temperature_tree = build_temperature_tree(dates, temperatures)
                print("Предыдущее состояние температур восстановлено.")

        elif choice == "9":
            print("Программа завершена.")
            break

        else:
            print("Такого пункта меню нет.")


if __name__ == "__main__":
    main()
