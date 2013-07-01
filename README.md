# Overholt

Overholt is an example Flask application illustrating some of my common practices

## Development Environment

At the bare minimum you'll need the following for your development environment:

1. [Python](http://www.python.org/)
2. [MySQL](http://www.mysql.com/)
3. [Redis](http://redis.io/)

It is strongly recommended to also install and use the following tools:

1. [virtualenv](https://python-guide.readthedocs.org/en/latest/dev/virtualenvs/#virtualenv)
2. [virtualenvwrapper](https://python-guide.readthedocs.org/en/latest/dev/virtualenvs/#virtualenvwrapper)
3. [Vagrant](http://vagrantup.com)
3. [Berkshelf](http://berkshelf.com)

### Local Setup

The following assumes you have all of the recommended tools listed above installed.

#### 1. Clone the project:

    $ git clone git@github.com:mattupstate/overholt.git
    $ cd overholt

#### 2. Create and initialize virtualenv for the project:

    $ mkvirtualenv overholt
    $ pip install -r requirements.txt

#### 3. Install the required cookbooks:

    $ berks install

#### 4. Install the Berkshelf plugin for Vagrant:

    $ vagrant plugin install vagrant-berkshelf

#### 5. Start virtual machine:

    $ vagrant up

#### 6. Upgrade the database:

    $ alembic upgrade head

#### 7. Run the development server:

    $ python wsgi.py

#### 8. In another console run the Celery app:

    $ celery -A overholt.tasks worker

#### 9. Open [http://localhost:5000](http://localhost:5000)


### Development

If all went well in the setup above you will be ready to start hacking away on
the application.

#### Database Migrations

This application uses [Alembic](http://alembic.readthedocs.org/) for database
migrations and schema management. Changes or additions to the application data
models will require the database be updated with the new tables and fields.
Additionally, ensure that any new models are imported into the consolidated
models file at `overholt.models`. To generate a migration file based on the
current set of models run the following command:

    $ alembic revision --autogenerate -m "<a description of what was modified>"

Review the resulting version file located in the `alembic/versions` folder. If
the file is to your liking upgrade the database with the following command:

    $ alembic upgrade head

For anything beyond this workflow please read the Alembic documentation.

#### Management Commands

Management commands can be listed with the following command:

    $ python manage.py

These can sometimes be useful to manipulate data while debugging in the browser.


#### Tests

To run the tests use the following command:

    $ nosetests
