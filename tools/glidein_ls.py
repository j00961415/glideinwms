#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2009 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

# Description:
#   Execute a ls command on a condor job working directory
#
# Usage:
#  glidein_ls.py <cluster>.<process> [<dir>] [-name <schedd_name>] [-pool <pool_name> ] [-timeout <nr secs>]

import sys, os.path
sys.path.append(os.path.join(sys.path[0], "../.."))

from glideinwms.tools.lib import glideinCmd

glideinCmd.exe_cmd(lambda argv:(['ls']+argv))
