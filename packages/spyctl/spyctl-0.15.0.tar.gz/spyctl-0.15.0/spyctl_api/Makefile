virtual_env:
	/usr/bin/python3.11 -m venv ./spyctl_api_venv --clear

update_requirements: virtual_env
	# Copy the spyctl-cli pyproject.toml and code to the build directory
	rm -rf requirements.txt test_requirements.txt
	rm -rf ./build
	mkdir ./build
	mkdir ./build/spyctl
	cp -R ../spyctl ../pyproject.toml ../LICENSE ../docs ./build/spyctl
	# Install pip-tools in the virtual environment
	. spyctl_api_venv/bin/activate; pip install pip-tools
	# Compile the requirements for the container
	. spyctl_api_venv/bin/activate; pip-compile -q requirements.in --output-file=requirements.txt --strip-extras
	# Update the location of the spyctl package to where it will be
	# in the container. See Dockerfile..
	sed -i 's|-e file:./build/spyctl|-e /spyctl|g' ./requirements.txt
	# Compile the requirements for local testing
	touch /tmp/requirements.in
	cat test_requirements.in > /tmp/requirements.in
	cat requirements.in >> /tmp/requirements.in
	. spyctl_api_venv/bin/activate; pip-compile -q /tmp/requirements.in --output-file=test_requirements.txt --strip-extras
	# sed -i 's|-e file:./build/spyctl|./build/spyctl|g' ./test_requirements.txt
	# Install the requirements for local testing
	. spyctl_api_venv/bin/activate; pip install -U -r test_requirements.txt
	# To install the code for type hinting
	. spyctl_api_venv/bin/activate; pip install ..	

install_test_requirements: virtual_env
	rm -rf ./build
	mkdir ./build
	mkdir ./build/spyctl
	cp -r ../spyctl ../pyproject.toml ./build/spyctl
	. spyctl_api_venv/bin/activate; pip install -U -r test_requirements.txt	
	# To install the code for type hinting
	. spyctl_api_venv/bin/activate; pip install ..	

docker_build:
	docker build -t spyctl_api:latest .

docker_test_build:
	rm -rf ./build
	mkdir ./build
	mkdir ./build/spyctl
	cp -r ../spyctl ../pyproject.toml ./build/spyctl
	docker build -f TestDockerfile -t spyctl_test_api:latest .

docker-run:
	docker-compose up -d

docker-test-run:
	docker-compose -f test-docker-compose.yaml up -d

docker-down:
	docker-compose down --remove-orphans

local_spyctl_build:
	(cd ..; pip3.11 uninstall spyctl -y; pip3.11 install .)
