# portal-backend

### Create venv and activate (on linux and mac)

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install requriements

```bash
pip install -r requirements.txt
```

### Start database

```bash
./start_db.sh
```

### Do once:

#### Migrate database

```bash
python manage.py migrate
```

#### Create superuser

```bash
python manage.py createsuperuser
```

### Start app

```bash
python manage.py runserver
```
