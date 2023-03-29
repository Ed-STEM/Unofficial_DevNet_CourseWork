#! /bin/zsh

export XCiscoMerakiAPIKey=TestKEY
export FLASK_APP=EE_CafeWeb
export FLASK_ENV=development
export FLASK_DEBUG=1


python -m flask init-db 
python -m flask run --cert=adhoc
