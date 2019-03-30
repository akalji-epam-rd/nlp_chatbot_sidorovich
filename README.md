# innkeeper_rasabot
Simple telegram-bot

## Подключение к серверу

 - ssh -i CentKeyPair.pem centos@52.89.87.142

Прописать в папке с CentKeyPair либо указать абсолютный путь. Сам файл вы можете найти в канале server в пинах.

## Запуск на сервере
В папке с проектом:
 - sudo python3.6 -m rasa_nlu.train -c nlu_config.yml --data nlu.md -o models --fixed_model_name nlu --project current --verbose
 - sudo python3.6 -m rasa_core.train -d domain.yml -s stories.md -o models/dialogue
 - sudo python3.6 -m rasa_core_sdk.endpoint --actions actions &
 - sudo python3.6 -m rasa_core.run -d models/dialogue -u models/current/nlu --port 5005 --endpoints endpoints.yml --credentials credentials.yml &

Последние две комманды запускаются в фоновом режиме, поэтому не забывайте из убивать.

Чуть позже сделаю всё по-человечески.

## Проблемесы возникающие 

При переподключении к машине jobs лагает и не хочет отображать процессы. Если вам надо убить бота, найдите PID процессов через:

 - sudo lsof -i :5055 (этот порт занят action'ами)
 - sudo lsof -i :5005 (этот порт занят ботом)
 
 Потом просто убиваете процессы через sudo kill *PID*
