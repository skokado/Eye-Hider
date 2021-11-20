# eye-hider

目線隠しアプリ

powered by [dlib](https://github.com/davisking/dlib)

# Demo

![demo](docs/demo.gif)

# Run

```shell
$ git clone https://github.com/skokado/Eye-Hider.git
$ cd Eye-Hider/

$ # Backend
$ cd backend/
$ pipenv sync
$ pipenv shell
$ make model
$ gunicorn -k uvicorn.workers.UvicornWorker app.main:app

$ # Frontend
$ cd frontend/
$ yarn start
```
