#!/bin/bash
# Course launcher prepared with Codex assistance on 2026-09-09.
# Source this file from the project root or using its absolute path.
# Uses the existing, verified Anaconda installation.
export PATH="/opt/anaconda3/bin:$PATH"
export MPLCONFIGDIR="/Users/cosmic-rishant/Desktop/HW_AST_5765C/audit/runtime/matplotlib"
export IPYTHONDIR="/Users/cosmic-rishant/Desktop/HW_AST_5765C/audit/runtime/ipython"
export JUPYTER_RUNTIME_DIR="/Users/cosmic-rishant/Desktop/HW_AST_5765C/audit/runtime/jupyter"
export XDG_CACHE_HOME="/Users/cosmic-rishant/Desktop/HW_AST_5765C/audit/runtime/cache"
mkdir -p "$MPLCONFIGDIR" "$IPYTHONDIR" "$JUPYTER_RUNTIME_DIR" "$XDG_CACHE_HOME"
printf 'AST 5765 environment: '
python --version
