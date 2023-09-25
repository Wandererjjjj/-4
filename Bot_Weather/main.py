import telebot
import requests
import json
import datetime
import webbrowser

bot = telebot.TeleBot('6515605206:AAGrQtar768wTnAa9I1KinxvPuHk4cngTEI')
API = '3482c7ba45ad49e5f20ccc32ded99a05'

def log_message(user_id, message_text, is_user=True):
    with open(f'{user_id}.log', 'a') as log_file:
        if is_user:
            log_file.write(f"User {user_id}: {message_text} ")
        else:
            log_file.write(f"Bot: {message_text} ")

@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.chat.id
    log_message(user_id, f"User {user_id}: {message.text}\n")
    bot.send_message(message.chat.id, "Привет! Я бот. Напиши <u><b>/help</b></u>, чтобы узнать список команд.",
                     parse_mode='html')
    log_message(user_id, "Bot: Привет! Я бот. Напиши /help, чтобы узнать список команд.\n",
                is_user=False)

@bot.message_handler(commands=['help'])
def help_message(message):
    user_id = message.chat.id
    log_message(user_id, f"User {user_id}: {message.text}\n")
    bot.send_message(message.chat.id, "Вот список доступных команд:\n"
                                      "<u><b>/start</b></u> - Начать диалог\n"
                                      "<u><b>/help</b></u> - Показать список команд\n\n"
                                      "<u><b>/weather</b></u> - Показать погоду на данный момент\n"
                                      "<u><b>/weather_detail</b></u> - Показать погоду подробно\n"
                                      "<u><b>/forecast</b></u> - Прогноз погоды на будущее\n"
                                      "<u><b>/website</b></u> - Сайт openweather\n", parse_mode='html')
    log_message(user_id, "Bot: Вот список доступных команд:\n"
                         "/start - Начать диалог\n"
                         "/help - Показать список команд\n"
                         "/weather - Показать погоду на данный момент\n"
                         "/weather_detail - Показать погоду подробно\n"
                         "/forecast - Прогноз погоды на будущее\n"
                         "<u><b>/website</b></u> - Сайт openweather\n")

@bot.message_handler(commands=['weather'])
def get_weather_init(message):
    user_id = message.chat.id
    log_message(user_id, f"User {user_id}: {message.text}")
    bot.send_message(message.chat.id, f"Введите город пожалуйста: ")
    log_message(user_id, "Bot: Введите город пожалуйста: ", is_user=False)
    bot.register_next_step_handler(message, get_weather)

@bot.message_handler(commands=['weather_detail'])
def get_weather_detail_init(message):
    user_id = message.chat.id
    log_message(user_id, f"User {user_id}: {message.text}")
    bot.send_message(message.chat.id, f"Введите город пожалуйста: ")
    log_message(user_id, "Bot: Введите город пожалуйста: ", is_user=False)
    bot.register_next_step_handler(message, get_weather_detail)

@bot.message_handler(commands=['forecast'])
def get_forecast_init(message):
    user_id = message.chat.id
    log_message(user_id, f"User {user_id}: {message.text}")
    bot.send_message(message.chat.id,
                     f"Введите город и дату (YYYY-MM-DD) для прогноза погоды (например, Moscow,2023-10-01): ")
    log_message(user_id, "Bot: Введите город и дату (YYYY-MM-DD) для прогноза погоды (например, Moscow,2023-10-01): ",
                is_user=False)
    bot.register_next_step_handler(message, get_forecast)

@bot.message_handler(commands=['website'])
def open_website(message):
    user_id = message.chat.id
    log_message(user_id, f"User {user_id}: {message.text}")
    bot.send_message(message.chat.id, "Открываю веб-сайт OpenWeatherMap...")
    log_message(user_id, "Bot: Открываю веб-сайт OpenWeatherMap...", is_user=False)
    webbrowser.open('https://openweathermap.org')

@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_id = message.chat.id
    user_message = message.text
    log_message(user_id, user_message)
    if user_message == '/weather':
        get_weather(message)
    elif user_message == '/weather_detail':
        get_weather_detail(message)
    elif user_message == '/forecast':
        get_forecast_init(message)

def get_weather(message):
    user_id = message.chat.id
    user_message = message.text
    log_message(user_id, user_message)
    city = user_message.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        Temp = data["main"]["temp"]
        bot.reply_to(message, f'Сейчас температура: {Temp}\n')
        image = 'Heat.jpg' if Temp > 5.0 else 'Cold.jpg'
        file_path = './' + image
        file = open(file_path, 'rb')
        bot.send_photo(message.chat.id, file)

        with open(f'{user_id}.log', 'a') as log_file:
            log_file.write(f'Bot: Сейчас температура: {Temp}\n')
            log_file.write(f'Bot: Отправлено фото: {file_path}\n')
    else:
        bot.reply_to(message, f'Город указан не верно')

def get_weather_detail(message):
    user_id = message.chat.id
    user_message = message.text
    log_message(user_id, user_message)
    city = user_message.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        Temp = data["main"]["temp"]
        Feel = data["main"]["feels_like"]
        Temp_min = data["main"]["temp_min"]
        Temp_max = data["main"]["temp_max"]
        Pressure = data["main"]["pressure"]
        Humidity = data["main"]["humidity"]
        Wind_speed = data["wind"]["speed"]

        bot.reply_to(message,
                     f'Сейчас погода: \nСейчас температура: {Temp} \nПо ощущениям: {Feel} \nМинимальная температура: '
                     f'{Temp_min} \nМаксимальная температура: {Temp_max} '
                     f'\nДавление: {Pressure} \nВлажность: {Humidity} \nСкорость ветра: {Wind_speed}\n')

        image = 'Heat.jpg' if Temp > 5.0 else 'Cold.jpg'
        file_path = './' + image
        file = open(file_path, 'rb')
        bot.send_photo(message.chat.id, file)

        with open(f'{user_id}.log', 'a') as log_file:
            log_file.write(f'Bot: Сейчас погода: \nСейчас температура: {Temp} \nПо ощущениям: {Feel} '
                           f'\nМинимальная температура: {Temp_min} \nМаксимальная температура: {Temp_max} '
                           f'\nДавление: {Pressure} \nВлажность: {Humidity} \nСкорость ветра: {Wind_speed}\n')
            log_file.write(f'Bot: Отправлено фото: {file_path}\n')
    else:
        bot.reply_to(message, f'Город указан не верно')

def get_forecast(message):
    user_id = message.chat.id
    user_message = message.text
    log_message(user_id, user_message)
    city_and_date = user_message.strip().lower().split(',')

    if len(city_and_date) != 2:
        bot.reply_to(message, "Пожалуйста, введите город и дату в формате 'Город,YYYY-MM-DD'.")
        log_message(user_id, "Bot: Пожалуйста, введите город и дату в формате 'Город,YYYY-MM-DD'.", is_user=False)
        return

    city = city_and_date[0].strip()
    date_str = city_and_date[1].strip()

    try:
        forecast_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        bot.reply_to(message, "Неверный формат даты. Пожалуйста, используйте формат 'YYYY-MM-DD'.")
        log_message(user_id, "Bot: Неверный формат даты. Пожалуйста, используйте формат 'YYYY-MM-DD'.", is_user=False)
        return

    res = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        forecasts = data.get("list", [])

        if not forecasts:
            bot.reply_to(message, "Прогноз погоды не найден для указанного города и даты.")
            log_message(user_id, "Bot: Прогноз погоды не найден для указанного города и даты.", is_user=False)
            return

        closest_forecast = None
        closest_time_diff = None

        for forecast in forecasts:
            forecast_datetime = datetime.datetime.fromtimestamp(forecast.get("dt"))
            time_diff = abs((forecast_datetime.date() - forecast_date).days)

            if closest_forecast is None or time_diff < closest_time_diff:
                closest_forecast = forecast
                closest_time_diff = time_diff

        if closest_forecast:
            Temp = closest_forecast["main"]["temp"]
            Weather_description = closest_forecast["weather"][0]["description"]
            bot.reply_to(message, f'Прогноз погоды для {city} на {forecast_date}:\n'
                                  f'Температура: {Temp}°C\n'
                                  f'Описание: {Weather_description}')
            log_message(user_id, f'Bot: Прогноз погоды для {city} на {forecast_date}:\n'
                                 f'Температура: {Temp}°C\n'
                                 f'Описание: {Weather_description}\n', is_user=False)
            image = 'Heat.jpg' if Temp > 5.0 else 'Cold.jpg'
            file_path = './' + image
            file = open(file_path, 'rb')
            bot.send_photo(message.chat.id, file)
        else:
            bot.reply_to(message, "Прогноз погоды не найден для указанного города и даты.")
            log_message(user_id, "Bot: Прогноз погоды не найден для указанного города и даты.", is_user=False)
    else:
        bot.reply_to(message, f'Произошла ошибка при получении прогноза погоды: {res.status_code}')
        log_message(user_id, f'Bot: Произошла ошибка при получении прогноза погоды: {res.status_code}', is_user=False)

if __name__ == '__main__':
    bot.infinity_polling()