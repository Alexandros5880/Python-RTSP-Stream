
clean-pyc:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	name '*~' -exec rm --force  {} 

upload-all:
	git add *
	git commit -m "New Commit"
	git push origin master
	git push heroku master --force

upload-git:
	git add *
	git commit -m "Flask_html_try"
	git push origin master

upload-heroku:
	git push heroku master --force

update-requirements:
	pip3 freeze > requirements.txt
	#pip3 install pipreqs > requirements.txt

update-constrains:
	pip install -c constraints.txt

install-requarements:
	#pip3 install -Ur requirements.txt
	pip3 install -r requirements.txt

install:
	sudo apt install -y apparmor apturl && pip3 install -r requirements.txt


run-local:
	python3 main.py 0

run-server:
	python3 main.py 1

setup-lib:
	apt-get update
	apt-get install -y libgl1-mesa-dev
