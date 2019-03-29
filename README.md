# innkeeper_rasabot
Simple telegram-bot

## Запуск на сервере
В папке с проектом:
 - sudo python3.6 -m rasa_nlu.train -c nlu_config.yml --data nlu.md -o models --fixed_model_name nlu --project current --verbose
 - sudo python3.6 -m rasa_core.train -d domain.yml -s stories.md -o models/dialogue
 - sudo python3.6 -m rasa_core_sdk.endpoint --actions actions &
 - sudo python3.6 -m rasa_core.run -d models/dialogue -u models/current/nlu --port 5005 --endpoints endpoints.yml --credentials credentials.yml &

Последние две комманды запускаются в фоновом режиме, поэтому не забывайте из убивать.

Чуть позже сделаю всё по-человечески.
