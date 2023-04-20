# Todolist project

## Stack: python3.9, Django, Postgres

### Create your boards, share it with other users, create categories for your goals,
### create goals (set deadlines, priority, change groups). Create new user manually or authorize with VK.
### See your goals list and create new goals through Telegram bot.

### Example of the app running is available at http://158.160.59.87/
### Telegram bot @todolist_new_bot

* Create virtual environment
```
python3 -m venv venv
```
```
venv/Scripts/activate (Windows)
source venv/bin/activate (MacOS)
```
* Install requirements:
```
poetry install
```
### Preparing django project:

* Run docker desktop on you PC
* Create .env
* Make migrations
* Run in terminal: ```docker-compose up -d```

