#! /usr/bin/env zsh

SNAME=storeit
SPATH=$HOME/code/epitech/storeit/proto/server
CLIPATH=$HOME/code/epitech/storeit/proto/client
CLI_IDX=0
FINDER=0

while getopts "f" opt; do
    case $opt in
      f)
         FINDER=1
         ;;
      \?)
         echo "Invalid option: -$OPTARG" >&2
         ;;
      esac
done

function reset_db {
  cd ./database
  ./init_database.sh &> /dev/null
  cd ..
  log_to_pane "database has been reset"
}

function run_in_tmux {
  tmux split-window -t $SNAME "$* || (echo 'program crashed. Press Enter'; read)"
  tmux select-layout tile
  sleep 0.1
  log_to_pane "command $* has been run"
}

function init_client {
  if [ "$1" != "keep-files" ]; then
    rm -rf /tmp/$1_$CLI_IDX
    rm -rf /tmp/$1_"$CLI_IDX"_git
    rm -f /tmp/$1*.log
    mkdir /tmp/$1_$CLI_IDX
    cd $SPATH/
    rm -rf storeit-demo
    git init --bare storeit-demo
    cd -
  fi

  if [ $FINDER -eq 1 ]; then
    open /tmp/$1_$CLI_IDX
  fi
}

function run_client {

  init_client $1
  pushd /tmp/$1_$CLI_IDX_git
  run_in_tmux node $CLIPATH/main.js -d /tmp/$1_$CLI_IDX
  popd
  log_to_pane "#$CLI_IDX client $1 is running"
  
  if [ $FINDER -eq 1 ]; then
    open /tmp/$1_$CLI_IDX
  fi

}

function kill_client {
  kill $(ps aux|grep -v grep | grep "node" | awk '{print $2}')
  log_to_pane "client $1 has been killed"
}

function log_to_pane {

  BEGIN_COLOR="\e[95m"
  END_COLOR=\e[0m

  echo "\e[95m $(date '+[%H:%M:%S]') \e[0m $1" >> /tmp/panelog.log
}

tmux kill-session -t storeit 2> /dev/null

rm -f /tmp/storeit-server.log
touch /tmp/panelog.log
tmux new-session -d -s $SNAME "tail -f /tmp/panelog.log"
log_to_pane "logging pane..."
#run_in_tmux $SPATH/main.py -l
#sleep 0.5 # wait a little bit for the server to start

source ./simulation.sh
