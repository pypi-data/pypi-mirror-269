# fastapitool
Bunch of tools for Fast API, that covers:
- `SimpleModelAPI` class, helps to quickly build CRUD api for db models using SQLAlchemy 2
- `SimpleRestAPI` class, helps to build REST quickly.

# Getting Started
```bash
git clone https://github.com/stonezhong/fastapitool.git

# create a python virtual environment
mkdir -p .venvs
python3 -m venv .venvs
source .venvs/bin/activate
pip install pip setuptools --upgrade
pip install wheel
pip install fastapi pydantic "uvicorn[standard]" sqlalchemy fastapitool

# start a demo server
cd fastapitool/examples
uvicorn demo.main:app

# You can access the Swagger UI at http://localhost:8000/docs
```
