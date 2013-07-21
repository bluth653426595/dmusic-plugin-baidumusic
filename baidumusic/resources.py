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

import time
from netlib import Curl
from utils import parser_json
from song import Song

TAGS_MUSIC_KEYS = {
    "song_id" : "sid",
    "song_title" : "title",
    "song_artist" : "artist",
    "album_title" : "album",
    "album_pic_small" : "album_url",
    "lyric_url" : "lyric_url",
    "url" : "uri",
    "kbps" : "#rate",
    "duration" : "#duration",
    "url_expire_time" : "uri_expire_time"
}

public_curl = Curl()

def request_songinfo(song):    
    url = "http://musicmini.baidu.com/app/link/getLinks.php"
    data = dict(songId=song['sid'],
                songArtist=song['artist'],
                songTitle=song['title'],
                linkType=9,
                isLogin=0,
                clientVer="8.0.0.5",
                isCloud=0
                )
    ret = public_curl.request(url, data)
    pret = parser_json(ret)
    if len(pret) > 0:
        return parse_to_dsong(pret[0], song)
    return None
    
def parse_to_dsong(ret, song=None):
    is_dummy = False
    if song is None:
        song = dict()
        is_dummy = True
        
    if isinstance(ret, dict):    
        has_key = "has_key"
    else:    
        has_key = "hasOwnProperty"
    try:
        bsong = ret
        bfile = ret['file_list'][0]
        
        for btag, tag in TAGS_MUSIC_KEYS.iteritems():
            if getattr(bsong, has_key)(btag):
                song[tag] = bsong[btag]
            if getattr(bfile, has_key)(btag):    
                if btag == "duration":
                    song[tag] = bfile[btag] * 1000
                else:    
                    song[tag] = bfile[btag]
                    
    except Exception, e:            
        import sys
        import traceback
        traceback.print_exc(file=sys.stdout)
        return None
    else:
        song["fetch_time"] = time.time()
        
        if is_dummy:
            new_song = Song()
            new_song.init_from_dict(song, cmp_key="sid")
            new_song.set_type('baidumusic')
            return new_song
        return song
