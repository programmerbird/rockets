#!/bin/sh


GIT_PATH=/home/{{user}}/{{name}}.git
APP_PATH=/home/{{user}}/deployed-apps/{{name}}

if [ ! -d /home/{{user}} ]
then
	yes '' | adduser --home /home/{{user}} --disabled-password {{user}}
	
	mkdir -p /home/{{user}}
	chown -R {{user}}:{{user}} /home/{{user}}
fi

if [ ! -d "$APP_PATH/env" ]
then 
	virtualenv --no-site-packages $APP_PATH/env
fi

if [ ! -f "$GIT_PATH/HEAD" ]
then
	cd "$GIT_PATH"
	mv $GIT_PATH/hooks/post-update /tmp/{{random}}.git-post-update
	git init --bare
	mv /tmp/{{random}}.git-post-update $GIT_PATH/hooks/post-update
fi

chmod +x $GIT_PATH/hooks/post-update

touch /var/log/boatyard/{{name}}.error
touch /var/log/boatyard/{{name}}.access
ln -s /var/log/boatyard/{{name}}.error /home/{{user}}/log/{{name}}/error.log
ln -s /var/log/boatyard/{{name}}.access /home/{{user}}/log/{{name}}/access.log

chown -R {{user}}:{{user}} $APP_PATH
chown -R {{user}}:{{user}} $GIT_PATH
chown {{user}}:{{user}} /var/log/boatyard/{{name}}.*

update-rc.d boatyard-{{name}} defaults

/etc/init.d/nginx reload
