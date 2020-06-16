#!/usr/bin/env bash
# coding=utf-8

# WARNING: DO NOT EDIT!
#
# This file was generated by plugin_template, and is managed by it. Please use
# './plugin-template --travis pulp_rpm' to update this file.
#
# For more info visit https://github.com/pulp/plugin_template

set -mveuo pipefail

source .travis/utils.sh

export POST_SCRIPT=$TRAVIS_BUILD_DIR/.travis/post_script.sh
export POST_DOCS_TEST=$TRAVIS_BUILD_DIR/.travis/post_docs_test.sh
export FUNC_TEST_SCRIPT=$TRAVIS_BUILD_DIR/.travis/func_test_script.sh

# Needed for both starting the service and building the docs.
# Gets set in .travis/settings.yml, but doesn't seem to inherited by
# this script.
export DJANGO_SETTINGS_MODULE=pulpcore.app.settings
export PULP_SETTINGS=$TRAVIS_BUILD_DIR/.travis/settings/settings.py

if [ "$TEST" = "docs" ]; then
  cd docs
  make PULP_URL="http://pulp" html
  cd ..

  if [ -f $POST_DOCS_TEST ]; then
    source $POST_DOCS_TEST
  fi
  exit
fi

cd ../pulp-openapi-generator

./generate.sh pulpcore python
pip install ./pulpcore-client
./generate.sh pulp_rpm python
pip install ./pulp_rpm-client
cd $TRAVIS_BUILD_DIR

if [ "$TEST" = 'bindings' ]; then
  python $TRAVIS_BUILD_DIR/.travis/test_bindings.py
  cd ../pulp-openapi-generator
  if [ ! -f $TRAVIS_BUILD_DIR/.travis/test_bindings.rb ]
  then
    exit
  fi

  rm -rf ./pulpcore-client

  ./generate.sh pulpcore ruby 0
  cd pulpcore-client
  gem build pulpcore_client
  gem install --both ./pulpcore_client-0.gem
  cd ..
  rm -rf ./pulp_rpm-client

  ./generate.sh pulp_rpm ruby 0

  cd pulp_rpm-client
  gem build pulp_rpm_client
  gem install --both ./pulp_rpm_client-0.gem
  cd ..
  ruby $TRAVIS_BUILD_DIR/.travis/test_bindings.rb
  exit
fi

cat unittest_requirements.txt | cmd_stdin_prefix bash -c "cat > /tmp/unittest_requirements.txt"
cmd_prefix pip3 install -r /tmp/unittest_requirements.txt

# check for any uncommitted migrations
echo "Checking for uncommitted migrations..."
cmd_prefix bash -c "django-admin makemigrations --check --dry-run"

# Run unit tests.
cmd_prefix bash -c "PULP_DATABASES__default__USER=postgres django-admin test --noinput /usr/local/lib/python${TRAVIS_PYTHON_VERSION}/site-packages/pulp_rpm/tests/unit/"

# Run functional tests
export PYTHONPATH=$TRAVIS_BUILD_DIR:$TRAVIS_BUILD_DIR/../pulpcore${PYTHONPATH:+:${PYTHONPATH}}

if [[ "$TEST" == "performance" ]]; then
  wget -qO- https://github.com/crazy-max/travis-wait-enhanced/releases/download/v1.0.0/travis-wait-enhanced_1.0.0_linux_x86_64.tar.gz | sudo tar -C /usr/local/bin -zxvf - travis-wait-enhanced
  echo "--- Performance Tests ---"
  if [[ -z ${PERFORMANCE_TEST+x} ]]; then
    travis-wait-enhanced --interval=1m --timeout=40m -- pytest -vv -r sx --color=yes --pyargs --capture=no --durations=0 pulp_rpm.tests.performance
  else
    travis-wait-enhanced --interval=1m --timeout=40m -- pytest -vv -r sx --color=yes --pyargs --capture=no --durations=0 pulp_rpm.tests.performance.test_$PERFORMANCE_TEST
  fi
  exit
fi

if [ -f $FUNC_TEST_SCRIPT ]; then
  source $FUNC_TEST_SCRIPT
else
    pytest -v -r sx --color=yes --pyargs pulp_rpm.tests.functional
fi

if [ -f $POST_SCRIPT ]; then
  source $POST_SCRIPT
fi
