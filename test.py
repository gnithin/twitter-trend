#!/usr/bin/env python

"""
A test script.
Will have all the classes and methods covered,
with comments for better undertsanding.
"""

# Copyright (C) 2015  Abhishek Bhattacharjee <abhishek.bhattacharjee11@gmail.com>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

################################################################################

from twitter.twrapper import *


def test1():
    """
    Tests the twitter class and tweet class
    """
    # use authenticate to get the token
    token = authenticate()
    # create a twitter obj with screen_name
    tc = twitter("abshk11")
    tc._set_conn()
    # Use the auth token and no of counts of tweets
    # for the screen_name(symantec)
    tweets = get_tweets_from_json(tc._fetch_tweets(token, 3))

    for t in tweets:
        t._print_details()
        print "----------------------------------"

# Test
if __name__ == "__main__":
    test1()
