#!/bin/bash

# Запускаем app.py в фоновом режиме
python app.py &

# Ждем 10 секунд
sleep 10

# Запускаем bot.py
python bot.py 