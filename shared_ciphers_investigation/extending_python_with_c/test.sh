# Add path to .so to PYTHONPATH
# export PYTHONPATH=$PYTHONPATH:/home/kevin/code/kmip_poc/shared_ciphers_investigation/extending_python_with_c/build/lib.linux-x86_64-cpython-311
# PYTHON=python

# Use debug build of Python ... begin:
# export PYTHONHOME=/home/kevin/code/cpython
# export PYTHONPATH=/home/kevin/code/cpython/Lib:/home/kevin/code/kmip_poc/shared_ciphers_investigation/extending_python_with_c/build/lib.linux-x86_64-cpython-313-pydebug
# export PYTHON=/home/kevin/code/cpython/debug/python
# PYTHON=/home/kevin/code/cpython/debug/python

export PYTHONHOME=/home/kevin/python-debug-install/
export PYTHONPATH=/home/kevin/python-debug-install/lib/python3.13/:/home/kevin/code/kmip_poc/shared_ciphers_investigation/extending_python_with_c/build/lib.linux-x86_64-cpython-313-pydebug
export PYTHON=/home/kevin/python-debug-install/bin/python3

# Use debug build of Python ... end:
$PYTHON test_spam.py -k goof 