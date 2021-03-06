#!/bin/bash

echo "################################################################################"
echo "####                              UNIT TESTS                                ####"
echo "################################################################################"
echo ""

coverage run --source=xccdf --omit="*tests*,*exception*" setup.py test

echo "################################################################################"
echo "####                             CODE COVERAGE                              ####"
echo "################################################################################"
echo ""

coverage report -m