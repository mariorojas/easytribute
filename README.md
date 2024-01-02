# easytribute.com
Main code repository for [easytribute.com](https://www.easytribute.com)

## Development setup

In a Python 3.x virtual environment:
```
$ make install
```

Now you can start the development server:
```
$ make runserver
```

In case of front-end deployment, please run the following command before adding any styles to `scss/styles.scss`:
```
$ make sass-watch
```

## Production deployment

In a Python 3.x environment connected to a repository:
```
$ make deploy
$ cp .env.example .env
```

**IMPORTANT:** Ensure to set the correct environment variables in the `.env` file for your setup.
