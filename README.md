# lifehack-backend

### Dependencies

<ul>
    <li> 
        <a href="https://www.djangoproject.com/" >Django</a>
    </li>
    <li> 
        <a href="https://pytorch.org/" >PyTorch</a>
    </li>
<ul>

The weights for Model 1 (SSD MobileNet) and Model 2 (FasterRCNN MobileNet) are stored in the "weights" directory.

### Usage

Firstly, you need to create a .env file in the root directory and put your cloudinary credentials as follows:

```
API_SECRET=
API_KEY=
CLOUD_NAME=
```

To run the development server at http://127.0.0.1:8000/

```
    $ python3 -m venv .venv
    $ source .venv/bin/activate
    $ pip3 install -r requirements.txt
    $ python3 manage.py makemigrations
    $ python3 manage.py migrate
    $ python3 manage.py createsuperuser
    $ python3 manage.py runserver
```

The website is not hosted anywhere temporarily due to the large size of PyTorch.
