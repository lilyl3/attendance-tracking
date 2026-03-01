#!/bin/bash
PID=$(lsof -ti :8501)
if [ -n "$PID" ]; then
    kill $PID
fi