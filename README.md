# Planetarium service 
Planetarium service, made in Django REST

## Features:

- JWT authentication
- Admin panel ```/admin/```
- Documentation is located at ```/api/doc/swagger```
- Managing reservations and tickets
- Nested creation for tickets from reservation
- Filtering by title and / or theme in AstronomyShow
- Filtering by date and / or show in ShowSession
- Creating / deleting / updating is only available for admins
- Read only abilities for authorized users



# Test it on Docker:
```
   docker pull wonsky/planetarium_service
```


## Installing using GitHub

1) Open Terminal and open folder to clone project in.

2) Clone repository into a desirable folder:

    ```
    git clone https://github.com/Wonsky1/planetarium-mate.git
    ```

3) Open cloned folder in terminal

4) If you don't have **pip** installed  [install it here](https://pip.pypa.io/en/stable/installation/#).

5) Create and activate **Virtual environment**:
   
   **Windows**
   ```
   python -m venv venv
   ```
   
   ```
   venv\Scripts\activate
   ```
   
   **MacOS**
   ```
   python3 -m venv venv
   ```
   
   ```
   source venv/bin/activate
   ```
   
6) Open cloned folder and install needed requirements using:

    ```
    pip install -r requirements.txt
    ```

7) Migrate:

   ```
   python manage.py migrate
   ```

8) Install database fixture:

   ```
   python manage.py loaddata db_data.json
   ```

9) Create .env file using ```env_example``` file

10) Run server:
   
   ```
   python manage.py runserver
   ```

11) Go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Run with Docker
Docker should be installed.
   ```
   docker-compose build
   docker-compose up
   ```
# Getting access:

- create user via ```api/user/register```
- get access token via ```api/user/token```
## Admin credentials:
- email: 
```admin@admin.com```
- password: 
```admin```

## User credentials: 
- email: 
```user@user.com```
- password: 
```user12345```


# Some of pages images:

- Documentation:
![image](https://i.imgur.com/1vDuoHH.png)

- Planetarium router: 
![image](https://i.imgur.com/SKFZrz9.png)

Diagram:\
![image](https://i.imgur.com/jLnWno4.png)
