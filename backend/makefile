run_dev:
	set DB_URL=$(shell python -c "import configparser; config = configparser.ConfigParser(); config.read('config.ini'); print(config.get('database', 'dev'))") && \
	set CRAWLER_URL=$(shell python -c "import configparser; config = configparser.ConfigParser(); config.read('config.ini'); print(config.get('url', 'key'))") && \
	python main.py

run_prod:
	set DB_URL=$(shell python -c "import configparser; config = configparser.ConfigParser(); config.read('config.ini'); print(config.get('database', 'prod'))") && \
	set CRAWLER_URL=$(shell python -c "import configparser; config = configparser.ConfigParser(); config.read('config.ini'); print(config.get('url', 'key'))") && \
	python main.py

reset_dev:
	cd database && \
	del tonie_dev.db && \
	cd .. && \
	cd model && \
	python tonie.py

reset_prod:
	cd database && \
	del tonie_prod.db && \
	cd .. && \
	cd model && \
	python tonie.py