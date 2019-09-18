"# PalveluViuhka" 

Installation
------------

### Prepare and activate virtualenv
    Windows
        ```
        python -m venv env
        call env/scripts/activate
        ```
    Linux
        ```
        python3 -m venv env
        source venv/bin/activate
        ```


### Install required packages

Install all packages required for development with pip command:

    pip install -r requirements.txt


### Create the database

Linux
    ```shell
    sudo -u postgres psql -c "create role employment with encrypted password 'secure-password';"
    sudo -u postgres psql -c "create database employment_services"
    ```

Windows
    ```shell
    psql -U postgres -c "create role employment with encrypted password 'secure-password';"
    psql -U postgres -c "create database employment_services"
    ```

### Build Employment Search static resources

Make sure you have Node 8 or LTS and yarn installed.

```shell
./build-resources
```

### Dev environment configuration

Create a file `employment/.env` to configure the dev environment e.g.:

```
DEBUG=1
ALLOWED_HOSTS='*'
DATABASE_NAME='employment_services'
DATABASE_USER='employment'
DATABASE_PASSWORD='secure-password'
```
### Run Django migrations and import data

```shell
python manage.py migrate
python manage.py createsuperuser
```
