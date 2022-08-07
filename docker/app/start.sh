#!/bin/bash

# Map secrets based on input
while getopts a:b: flag
do
   case "${flag}" in
        a) app1-super-secret-json=${OPTARG};;
        b) app1-super-secret-string=${OPTARG};;
        
    esac
done

# Print secret
while [ i=i ]
do
   echo $app1-super-secret-json
   echo $app1-super-secret-string
   # Sleep a bit to avoid loop overload
   sleep 10
done

trap 'cleanup; exit 130' INT
trap 'cleanup; exit 143' TERM
