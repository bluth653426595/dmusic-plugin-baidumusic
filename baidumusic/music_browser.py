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

import gtk
import webkit
import javascriptcore as jscore

from widget.ui import NetworkConnectFailed
from deepin_utils.net import is_network_connected
from widget.ui_utils import switch_tab

from music_player import MusicPlayer, PlayerInterface, TTPDownload

class MusicBrowser(gtk.VBox):
    
    def __init__(self):
        super(MusicBrowser, self).__init__()
        
        self.webview = webkit.WebView()
        self.webview.set_transparent(True)
        
        self.webview.open("http://musicmini.baidu.com/static/recommend/recommend.html")
        self.webview.connect("load-finished", self.on_webview_load_finished)
        
        self._player = MusicPlayer()
        self._player_interface = PlayerInterface()
        self._ttp_download = TTPDownload()
        self.is_reload_flag = False
        
        self.network_failed_box = NetworkConnectFailed(self.check_network_connection)
        self.check_network_connection(auto=True)
        
    def check_network_connection(self, auto=False):    
        if is_network_connected():
            switch_tab(self, self.webview)
        else:    
            switch_tab(self, self.network_failed_box)
        
    def on_webview_load_finished(self, widget, event):    
        self.js_context = jscore.JSContext(self.webview.get_main_frame().get_global_context()).globalObject        
        self.js_context.player = self._player
        self.js_context.window.top.ttp_download = self._ttp_download
        self.js_context.window.top.playerInterface = self._player_interface
        self.js_context.link_support = True
        self.js_context.alert = self._player.alert
        if not self.is_reload_flag:
            self.webview.reload()
            self.is_reload_flag = True
