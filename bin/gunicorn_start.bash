#!/bin/bash

NAME="supertramp_server"                          # Name of the application
DJANGODIR=~/ocr-server                            # Django project directory
SOCKFILE=~/ocr-server/gunicorn.sock               # we will communicte using this unix socket
USER=azureuser                                    # the user to run as
#GROUP=webapps                                    # the group to run as
NUM_WORKERS=20                                    # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=supertramp_server.settings # which settings file should Django use
DJANGO_WSGI_MODULE=supertramp_server.wsgi         # WSGI module name

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source ~/.virtualenvs/supertramp-server/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER \
  --log-level=debug \
  --bind=unix:$SOCKFILE