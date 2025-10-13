# Tohoilykisa (aka The Clumsiness competition)

<em>This branch is for Cyber Security Base Project I.</em>

The clumsiness competition application keeps track of the users' clumsiness.

The idea behind this application is to determine who is the most clumsy person in the group. There are many ways to exhibit clumsiness, for instance, tripping, falling down while walking (maybe the road is icy or maybe you are just clumsy), falling down while standing (now you are just being clumsy), falling off a vehicle (e.g., a bicycle), bumping into something (e.g., a wall, a chair, a coffee table, another person (spatial awareness is challenging..)), getting a cut or a burn while doing something (e.g., reading a book and getting a paper cut, burning yourself while cooking or baking), hitting your head on a cabinet door, or dropping something for no reason.

In the end, the most important criterion for defining clumsiness is that it is caused by oneself accidentally. It is not about incidents that occur while attempting something potentially harmful but about everyday incidents.

<b>Application features (working process):</b>

- The user can create an account, log in and log out.
- The user can create, join and leave a competition group.
- Events are categorized based on the type of clumsiness. There are default event categories and events. The user can create new event categories and events.
- The user can log an event that has happened to them inside a competition group.
- Within different competition groups, there is a scoreboard to track who has been the most clumsy.
- The user can view their own competition group's scoreboard.

## Startup instructions

This application cannot be tested on Fly.io. Here are the instructions how to start the application locally.

Python3 and postgresql are required.

Clone this repository to your computer:

```
git clone https://github.com/rautiais/tohoilykisa.git
```

Navigate to its root directory. Create a .env file in the directory and set its contents as follows:

```
DATABASE_URL=postgresql:///username
SECRET_KEY=<secret-key>
```

You can create your own secret-key with this command:

```
$ python3
>>> import secrets
>>> secrets.token_hex(16)
```

Activate the virtual environment and install the application dependencies with the commands:

```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r ./requirements.txt
```

Start the database in a separate terminal by running the command:

```
start-pg.sh
```

Define the database schema with the command:

```
$ psql < schema.sql
```

Or you can create your own database with the command:

```
$ psql
user=# CREATE DATABASE <database-name>;
```

And then define the database schema with the new database:

```
$ psql -d <database-name> < schema.sql
```

Start the application with the command:

```
$ flask run
```
