


echo "Installing requirements.ini" >&2
if [ -f "$APP_PATH/app{{secret}}/requirements.ini" ]
then 
	$APP_PATH/env/bin/pip install -r "$APP_PATH/app{{secret}}/requirements.ini" | sed "s@$APP_PATH/app{{secret}}/@@g" | sed "s@$APP_PATH/env/@@g"
fi
