#! /bin/bash

./canadian_http.py 7643&
curl -u sevauk:zulu -d "$(./produce_dummy_tree.py dummy_tree)" localhost:7641/session/join?port=7643
sleep 1
curl -u sevauk:zulu -d "$(cat dummy_json_file.json)" localhost:7641/data/tree
