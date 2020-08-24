ifeq ($(OS), Windows_NT)
    local = python main.py 0
    server = python main.py 1
    install_req = pip3 install -r requirements.txt
else
    local = python3 main.py 0
    server = python3 main.py 1
    install_req = pip3 install -r requirements.txt
endif


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


install-requarements:
	$(install_req)


run-local:
	$(local)


run-server:
	$(server)



setup-lib:
	sudo apt-get update
	sudo apt-get install -y libgl1-mesa-dev
