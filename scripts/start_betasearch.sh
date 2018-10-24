#!/bin/bash
#
# To test-run:
# 
#       sudo -H -u ubuntu ./start_betasearch.sh
# 
# To actually run:
# 
#       (install betasearch.service startup service)
#	/etc/systemd/system/.
#
# Shell script used to start up centillion so that 
# it always runs, and re-spawns when it dies.
# 
# This is reliant on having pyenv set up already
# on beavo, the server.

CENTIL_DIR="/home/ubuntu/betasearch"
PYENV_BIN="/home/ubuntu/.pyenv/bin"

echo "Preparing python"
eval "$(${PYENV_BIN}/pyenv init -)"

echo "Changing directories"
cd ${CENTIL_DIR}

echo "Installing virtualenv"
virtualenv betavp
source betavp/bin/activate
betavp/bin/pip install -r requirements.txt
python setup.py build install

echo "Running beta search centillion"

CENTILLION_CONFIG="${CENTIL_DIR}/config/config_flask.py" python ${CENTIL_DIR}/scripts/run_betasearch.py && tail -f /nev/null
