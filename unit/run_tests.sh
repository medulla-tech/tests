#!/bin/bash

verbosity=0
while getopts ":v" opt; do
    case $opt in
        v) (( verbosity=verbosity+1 ))
        ;;
    esac
done

for file in *.list; do
    while IFS= read -r line; do
        if [ ! -z "${line}" ]; then
            cmd="python3 ./_common/xmlrpc_client.py --module ${file::-5} ${line}"
            case $verbosity in
                0) cmd="${cmd} &> /dev/null"
                ;;
                1) cmd="${cmd}"
                ;;
                2) cmd="${cmd} --debug"
                ;;
                *) cmd="${cmd} --debug"
                ;;
            esac
            echo "Running ${cmd}"
            eval ${cmd}
            if [ "$?" == 1 ]; then
                echo "failed"
            else
                echo "passed"
            fi
        fi
    done < ${file}
done
