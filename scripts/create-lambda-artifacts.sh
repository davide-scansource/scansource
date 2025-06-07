#!/bin/sh

set -e # Exit immediately if a command exits with a non-zero status.

BASEDIR=$(pwd)

echo "Create Lambda1 Artifact"

cd $BASEDIR/lambdas/lambda1

zip -r $BASEDIR/artifacts/lambda1.zip .

echo "Create Lambda2 Artifact"

cd $BASEDIR/lambdas/lambda2

zip -r $BASEDIR/artifacts/lambda2.zip .


