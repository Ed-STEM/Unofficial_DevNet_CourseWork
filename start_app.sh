#! /bin/zsh

export XCiscoMerakiAPIKey= <secret key>
export FLASK_APP=EE_CafeWeb
export FLASK_ENV=development
export FLASK_DEBUG=1


flask init-db &
flask run