#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2013 Deepin, Inc.
#               2011 ~ 2013 Hou ShaoHui
# 
# Author:     Hou ShaoHui <houshao55@gmail.com>
# Maintainer: Hou ShaoHui <houshao55@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from music_browser import MusicBrowser
from music_view import MusicView
from nls import _
from helper import Dispatcher, SignalCollector
from widget.tab_box import  ListTab

music_browser = MusicBrowser()
music_list = MusicView()
radio_list_tab = ListTab(_("百度音乐"), music_list, music_browser)

def enable(dmusic):
    SignalCollector.connect("baidumusic", Dispatcher, "being-quit", lambda w: music_list.save())
    Dispatcher.emit("add-source", radio_list_tab)
    
def disable(dmusic):    
    SignalCollector.disconnect_all("baidumusic")
    Dispatcher.emit("remove-source", radio_list_tab)
