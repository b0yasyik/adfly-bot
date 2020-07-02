install:
	python -m ensurepip --user --default-pip
	python -m pip install --user -Ur requirements.txt pip
update:
	git fetch --all
	git reset --hard origin/master
