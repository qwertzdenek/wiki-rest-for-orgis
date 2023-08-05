REST API for Wikipedia
======================

Hello there!

How to run
----------

- create Virtual Environment

    `python3 -m venv venv`

- activate it

    `source venv/bin/activate`

- install dependencies

    `python3 -m pip install -r requirements.txt`

- setup env file if you need credentials

    `mv .env.sample .env`

- run the server

    `uvicorn app:api`

now you can find API at `http://localhost:8000`.