release_ports:
	sudo kill $$(sudo lsof -ti :5055)
	sudo kill $$(sudo lsof -ti :5005)

restart_bot:
	sudo python3.6 -m rasa_core_sdk.endpoint --actions actions &
	sudo python3.6 -m rasa_core.run -d models/dialogue -u models/current/nlu --port 5005 --endpoints endpoints.yml --credentials credentials.yml &

retrain_bot:
	sudo python3.6 -m rasa_nlu.train -c nlu_config.yml --data training_dataset.json -o models --fixed_model_name nlu --project current --verbose
	sudo python3.6 -m rasa_core.train -d domain.yml -s stories.md -o models/dialogue

restart_full:
	sudo python3.6 -m rasa_nlu.train -c nlu_config.yml --data training_dataset.json -o models --fixed_model_name nlu --project current --verbose
	sudo python3.6 -m rasa_core.train -d domain.yml -s stories.md -o models/dialogue
	sudo python3.6 -m rasa_core_sdk.endpoint --actions actions &
	sudo python3.6 -m rasa_core.run -d models/dialogue -u models/current/nlu --port 5005 --endpoints endpoints.yml --credentials credentials.yml &	

restart_cmd:
	sudo python3.6 -m rasa_nlu.train -c nlu_config.yml --data training_dataset.json -o models --fixed_model_name nlu --project current --verbose
	sudo python3.6 -m rasa_core.train -d domain.yml -s stories.md -o models/dialogue
	sudo python3.6 -m rasa_core_sdk.endpoint --actions actions --port 6066 &
	sudo python3.6 -m rasa_core.run -d models/dialogue -u models/current/nlu --port 6006 --endpoints endpoints_cmd.yml

release_cmd:
	sudo kill $$(sudo lsof -ti :6066)

