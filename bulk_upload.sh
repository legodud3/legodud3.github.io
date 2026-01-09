#!/bin/bash
# Wrapper script to run bulk_upload.py with warnings suppressed
python3 -W ignore bulk_upload.py "$@"
