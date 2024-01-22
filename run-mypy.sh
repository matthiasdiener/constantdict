#!/bin/bash

set -ex

mypy --strict constantdict/ test/ examples/
