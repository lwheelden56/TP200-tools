#!/bin/bash

echo "TP200W Functions"
PS3='Which function?: '
options=("Status" "Reboot" "Test" "Quit")
select opt in "${options[@]}"
do
    case $opt in
        "Status")
            sudo ./venv/bin/python3 status-TP200W.py
            break
            ;;
        "Reboot")
            sudo ./venv/bin/python3 reboot-TP200W.py
            break
            ;;
        "Test")
            sudo ./venv/bin/python3 test-TP200W.py
            break
            ;;
        "Quit")
            break
            ;;
        *) echo "invalid option $REPLY";;
    esac
done
