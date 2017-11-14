# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# PyDevNS - Pure Python DNS server for developers
# MIT License
#
# Copyright (c) 2017 Dave Hayes <dwhayes@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
PyDevNS
~~~~~~~~~~~~~~~~~~~~~
PyDevNS is a DNS server for developers.

:copyright: (c) 2017 Dave Hayes.
:license: MIT, see LICENSE for more details.
"""

from .config import Config
config = Config()  # noqa


__title__ = "devns"
__version__ = "0.4.7"
__author__ = "Dave Hayes"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2017 Dave Hayes"

from .dns import DNS  # noqa
from . import server  # noqa
