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


from song import Song
from events import event_manager
from pyquery import PyQuery

try:
    from simplejson import json
except ImportError:    
    import json
    
from resources import parse_to_dsong    


class MusicPlayer(object):        
    down_type = 0
    
    @property
    def ClientInfo(self):
        info = dict(bduss="",
                    client_version="8.0.0.5",
                    is_hq_enabled=0,
                    vip_level=1,
                    )
        return json.dumps(info)
    
    def AddSongs(self, dummy_songs):
        ''' '''
        songs = self.parse_dummy_songs(dummy_songs)
        if songs:        
            event_manager.emit("add-songs", songs)
        
    def PlaySongs(self, dummy_songs):    
        songs = self.parse_dummy_songs(dummy_songs)
        if songs:
            event_manager.emit("play-songs", songs)
            
    def FavoriteSongs(self, dummy_songs):
        pass
    
    def DownloadSongs(self, args):    
        print args
        
    @classmethod    
    def parse_dummy_songs(cls, dummy_songs):    
        songs = []
        for i in dummy_songs:
            song = parse_to_dsong(dummy_songs[i])
            if song:
                songs.append(song)
        return songs        
    
    def Login(self):
        print "login"
        
    def alert(self, *args):    
        print args
    
                
class PlayerInterface(object):
    
    def setLoginCallBackType(down_type):
        MusicPlayer.down_type = down_type
        
        
class TTPDownload(object):        
    
    def init(self, down_type, dummy_songs):
        print "Don't support"
        # print MusicPlayer.parse_dummy_songs(dummy_songs)
