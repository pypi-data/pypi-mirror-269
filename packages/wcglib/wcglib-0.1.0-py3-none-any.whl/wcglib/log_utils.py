#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import sys, os

script_path = os.path.abspath(__file__)
dir_path = os.path.dirname(script_path)
dir_name = os.path.basename(dir_path)

log = logging.getLogger(dir_name)

log.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s : %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)
