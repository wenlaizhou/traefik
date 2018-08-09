# coding=utf8
import sys

import itertools, pprint

reload(sys)
sys.setdefaultencoding('utf-8')

import os
import re
import utils

pprint.pprint(utils.getGoDeps())