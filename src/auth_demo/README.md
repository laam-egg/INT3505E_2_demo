# Auth Demo

Demo 3 cách lưu access token vào:

1. localStorage
2. sessionStorage
3. HTTP-Only Cookie

## Getting It Up and Running

### Backend

**Setup:**

```sh
cd <project_root>
cd src/auth_demo/backend

virtualenv venv
source ./venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

then edit the environment variables
in `.env`.

**Run:**

```sh
cd <project_root>
cd src/auth_demo/backend
source ./venv/bin/activate

flask run
```

### Frontend

**Setup:**

```sh
cd <project_root>
cd src/auth_demo/frontend

yarn
cp .env.example .env
```

then edit the environment variables
in `.env`.

**Run:** 

```sh
cd <project_root>
cd src/auth_demo/frontend

yarn dev
```
