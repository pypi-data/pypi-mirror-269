#!/bin/sh
ssh -f -L 5001:localhost:5001 foo@ipfs.filforge.io -N
