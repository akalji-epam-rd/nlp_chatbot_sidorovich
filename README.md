# innkeeper_rasabot
Simple telegram-bot.

## Подключение к серверу

 - ssh -i CentKeyPair.pem centos@52.89.87.142

Прописать в папке с CentKeyPair либо указать абсолютный путь. Сам файл вы можете найти в канале server в пинах.

## Запуск на сервере
### По-человечески
Запускаем необходимое в bash'е в папке с проектом.
Команды прописаны в Makefile:
 - **restart_full**
  Полностью перезапускает бота (вместе с обучением)
 - **restart_bot**
  Перезапускает только actions и самого бота.
 - **retrain_bot**
  Заново обучает rasa_nlu и rasa_core.
 - **release_ports**
  Убивает процессы занимающие порты 5055 (actions) и 5005 (bot). 
  
Убивать процессы необходимо перед перезапуском бота, т.к. новые процессы не смогут подключиться к тем же портам.

Если выдается ошибка, скорее всего задач уже нет. Можно проверить их наличие вручную через sudo lsof см. ниже.

### Если уж очень вам хочется писать всё руками или копипастить
То же самое, что и выше, только явно.

В папке с проектом:
 - sudo python3.6 -m rasa_nlu.train -c nlu_config.yml --data training_dataset.json -o models --fixed_model_name nlu --project current --verbose
 - sudo python3.6 -m rasa_core.train -d domain.yml -s stories.md -o models/dialogue
 - sudo python3.6 -m rasa_core_sdk.endpoint --actions actions &
 - sudo python3.6 -m rasa_core.run -d models/dialogue -u models/current/nlu --port 5005 --endpoints endpoints.yml --credentials credentials.yml &

Последние две комманды запускаются в фоновом режиме, поэтому не забывайте их убивать. +если вам не надо переобучать модель, вы можете запустить только их.

#### Проблемесы возникающие 

При переподключении к машине jobs лагает и не хочет отображать процессы, а нам надо убить их, т.к. они занимают порты как минимум.

Если вам надо убить бота, найдите PID процессов через:

 - sudo lsof -i :5055 (этот порт занят action'ами)
 - sudo lsof -i :5005 (этот порт занят ботом)
 
 Потом просто убиваете процессы через sudo kill *PID*
