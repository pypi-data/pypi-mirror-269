#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2016-2024 Christian Tanzer. All rights reserved
# tanzer@gg32.com                                      https://www.gg32.com
# Web: https://www.gg32.com/en/ Email: tanzer@swing.co.at
# All rights reserved
# ****************************************************************************
# This module is licensed under the terms of the BSD 3-Clause License
# <https://www.gg32.com/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    _JNJ.setup
#
# Purpose
#    Setup file for package namespace JNJ
#
# Revision Dates
#    12-Oct-2016 (CT) Creation
#    13-Oct-2016 (CT) Use `find_packages`, `_TFL.fs_find`, not home-grown code
#    22-Feb-2017 (CT) Use `TFL_STP`, not home-grown code
#    25-Feb-2017 (CT) Pass `data_dirs` to `packages_plus_data_files`
#    27-Feb-2017 (CT) Add Python 3.6 to `classifiers`
#    25-Mar-2020 (CT) Restrict Python versions to >=3.7
#    29-May-2023 (CT) Restrict Python versions to >=3.8
#    24-Apr-2024 (CT) Restrict Python versions to >=3.9
#    ««revision-date»»···
#--

from   setuptools               import setup

import TFL_STP as STP

STP.change_to_dir (__file__)

license = "BSD License"
name    = "JNJ"
p_name  = "_JNJ"

version              = STP.package_version ()
long_description     = STP.long_description ()
packages, data_files = STP.packages_plus_data_files \
    (p_name, data_dirs = ["email", "html", "httpd_config"])
Test_Command         = STP.Test_Command

if __name__ == "__main__" :
    setup \
    ( name                 = name
    , version              = version
    , description          =
        "Package providing a Jinja2-based template framework."
    , long_description     = long_description
    , license              = license
    , author               = "Christian Tanzer"
    , author_email         = "tanzer@swing.co.at"
    , url                  = "https://codeberg.org/tanzer/tapyr"
    , packages             = packages
    , package_dir          = { p_name : "." }
    , package_data         = { p_name : data_files }
    , platforms            = "Any"
    , classifiers          = \
        [ "Development Status :: 5 - Production/Stable"
        , "License :: OSI Approved :: " + license
        , "Operating System :: OS Independent"
        , "Programming Language :: Python"
        , "Intended Audience :: Developers"
        , "Topic :: Internet :: WWW/HTTP :: Dynamic Content"
        , "Topic :: Software Development :: Libraries :: Python Modules"
        , "Topic :: Text Processing :: Markup :: HTML"
        ]
    , python_requires      = ">=3.9"
    , setup_requires       = ["TFL_STP>=3"]
    , install_requires     = ["TFL>=3", "CHJ>=3", "jinja2"]
    , extras_require       = dict ()
    , cmdclass             = dict (test = Test_Command)
    , zip_safe             = False ### no eggs, please
    )

### __END__ _JNJ.setup
