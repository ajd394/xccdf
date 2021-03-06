#!/bin/bash

echo "################################################################################"
echo "####                         CICLOMATIC COMPLEXITY                          ####"
echo "################################################################################"
echo ""

radon cc -s -a -e *test*,test*,*test src/xccdf

echo "################################################################################"
echo "####                         MAINTAINABILITY INDEX                          ####"
echo "################################################################################"
echo ""

radon mi -s -e *test*,test*,*test src/xccdf
