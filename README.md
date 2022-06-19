# Car-leasing

Car leasing compagny api with dockerized 

# Build image and try api

```
> docker-compose up --build
```

If you want to seed db to create realistic demo

```
> docker-compose exec api python manage.py seed_db
```


# Install for dev

Run a
```
> python -m virtualenv venv
> source venv/bin/activate
> pip install -r requirements.txt
```
