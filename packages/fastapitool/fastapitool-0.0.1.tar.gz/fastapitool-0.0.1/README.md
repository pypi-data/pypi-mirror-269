# fastapitool
Bunch of tools for Fast API

# 测试安装
```bash
mkdir -p ~/fastapi-test
mkdir -p ~/fastapi-test/.venvs
cd ~/fastapi-test
python3 -m venv .venvs
source .venvs/bin/activate
pip install pip setuptools --upgrade
pip install wheel


pip install fastapi pydantic uvicorn[standard]==0.23.2
pip install -e /home/stonezhong/DATA_DISK/projects/fastapitool

# 运行程序
uvicorn main:app

# ssh tunnel
ssh -L 8000:localhost:8000 trantor

```

```
core
  |
  +-- models
        |
        +-- __init__.py
        |
        +-- base.py         define the common base class for all model classes
        |
        +- student.py       specific model class

uvicorn demo.main:app

```