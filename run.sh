#!/usr/bin/env bash
set -e

packer build amazon-linux.json | tee build.log
