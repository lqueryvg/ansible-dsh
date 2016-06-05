#!/bin/bash

echoerr() { echo "$@" 1>&2; }

echo "this is a message on stdout"
echo "this is a message on stdout"
echoerr "this is a message on stderr"
echoerr "this is a message on stderr"

exit $((RANDOM % 2))

