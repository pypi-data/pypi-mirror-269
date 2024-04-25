# -*- coding: utf-8 -*-
# Copyright (C) 2015-2020 Christian Tanzer All rights reserved
# tanzer@gg32.com                                      https://www.gg32.com
# #*** <License> ************************************************************#
# This module is part of the package JNJ.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <https://www.gg32.com/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    JNJ.SRM
#
# Purpose
#    Template declarations for SRM (sailing race management)
#
# Revision Dates
#    11-Feb-2015 (CT) Creation (factored from JNJ.Templateer)
#    ««revision-date»»···
#--

"""
Declare templates related to SRM (sailing race management).
"""

from   _JNJ               import JNJ
from   _JNJ.Templateer    import Template

Template \
    ( "ETR_table_regatta",                "html/ETR/regatta.m.jnj"
    , parent_name = "ETR_table"
    )
Template \
    ( "ETR_table_regatta_register",       "html/ETR/regatta_register.m.jnj"
    , parent_name = "ETR_table_regatta"
    )
Template \
    ( "ETR_table_regatta_result",         "html/ETR/regatta_result.m.jnj"
    , parent_name = "ETR_table_regatta"
    )

Template ("regatta_calendar",             "html/regatta_calendar.jnj")
Template ("regatta_page",                 "html/regatta_page.jnj")
Template ("regatta_page_r",               "html/regatta_page_r.jnj")
Template ("regatta_ranking",              "html/regatta_ranking.jnj")
Template ("regatta_register_email",       "email/regatta_register.jnj")

if __name__ != "__main__" :
    JNJ._Export_Module ()
### __END__ JNJ.SRM
