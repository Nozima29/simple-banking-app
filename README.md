## Bering Bank
Build a simulation of 'Bering Bank' that allows users to perform the following operations:
- Create user account
- Register cards(plural!)
- Disable card
- Enable card
- Check account balance
- Withdraw cash
- Deposit cash

## How to start

    cd app/bank
    pip install -r requirements.txt
    python manage.py makemigrations
    python manage.py migrate
    

### Launch app in browser

    python manage.py runserver

* Open the app in `http://127.0.0.1:8000/`
* First create account in `http://127.0.0.1:8000/sign-up/`
* Then register card in `http://127.0.0.1:8000/card/`and play!

### Run tests

    pytest

> Tests are found in `cards/tests.py` and `users/tests.py`


### Create superuser

    python manage.py createsuperuser

> Admin panel can be found in `http://127.0.0.1:8000/admin/`



