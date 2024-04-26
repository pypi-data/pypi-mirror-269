# Queue Service

Executes tasks which take too much time. :)


# Setup

```
python3 -m venv .venv
source .venv/bin/activate # on linux/mac
.venv/Scripts/activate.bat # on windows

pip install -r ./requirements.txt
cp .env.example .env
```

# Run

```
uvicorn app.server:app
```
