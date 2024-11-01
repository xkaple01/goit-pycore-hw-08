## OOP Virtual Assistant
### Backend and Frontend in Python
### Usage

Clone repository
```sh
git clone https://github.com/xkaple01/goit-pycore-hw-08.git
cd goit-pycore-hw-08
```

Build docker image
```sh
docker build -t xkaple01/goit-pycore-hw-08 .
```

Create docker volume
```sh
docker volume create addressbook
```

Run docker container 
```sh
docker run --rm -it -p 8080:8080 --mount type=volume,src=addressbook,target=/goit-pycore-hw-08/backend/database xkaple01/goit-pycore-hw-08
```

Open browser at 0.0.0.0:8080 \
Work with application

Stop docker container
```sh
press ctrl-c in terminal
```

Run the new docker container
```sh
docker run --rm -it -p 8080:8080 --mount type=volume,src=addressbook,target=/goit-pycore-hw-08/backend/database xkaple01/goit-pycore-hw-08
```

Open browser at 0.0.0.0:8080 \
Work with application

Notice that the state of all Python objects persists even though the docker container was stopped and then the new container was launched. \
State persistence is possible due to objects serialization (pickling) into and then de-serialization from mounted docker volume.

Stop docker container
```sh
press ctrl-c in terminal
```

Remove docker volume
```sh
 docker volume rm addressbook
```

