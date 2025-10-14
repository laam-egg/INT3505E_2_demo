# Getting It Up and Running

## Requirements

- Python 3.12+

## Setup

### Python Environment and Packages

```sh
cd <project_root>
cd src/backend
virtualenv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

### Environment Variables

In project root, **copy (NOT DELETE!)** the file `.env.example`
into a new file named `.env`. Adjust the environment
variables as necessary.

### Run

```sh
cd <project_root>
cd src/backend
source ./venv/bin/activate

flask run --host=0.0.0.0 --port=5000
```
