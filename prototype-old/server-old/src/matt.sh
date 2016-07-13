#! /bin/bash

./canadian_http.py 7642&

curl -u matt:zulu -d "$(./produce_dummy_tree.py dummy_tree)" localhost:7641/session/join?port=7642
