#!/bin/env bash

# Benjamin Adam Catching
# 2020-04-20
# Andino lab

python3 mask_single_sim.py $1 $2 $3 

## End-of-job summary, if running as a job
[[ -n "$JOB_ID" ]] && qstat -j "$JOB_ID"
