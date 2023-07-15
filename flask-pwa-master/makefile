.PHONY: environment
environment:
	pyenv install -s 3.10.0
	pyenv uninstall --force flask-pwa
	pyenv virtualenv 3.10.0 --force flask-pwa
	pyenv local flask-pwa

.PHONY: install
install:
	pip3 freeze | xargs -r pip3 uninstall -y && \
	pip3 install -r requirements.txt

.PHONY: run
run:
	export FLASK_ENV=development && flask run -p 15316
