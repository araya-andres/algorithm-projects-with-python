#!/bin/bash

pip freeze > tmp
grep -vxf requirements.txt tmp > requirements.dev.txt
rm tmp