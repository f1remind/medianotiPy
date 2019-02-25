#!/usr/bin/env python
import musicbrainzngs
from datetime import datetime

#debug dependencies
import pdb
import json

musicbrainzngs.set_useragent("musicnotify", "0.0.1.1")

artists = []
with open('artists.txt') as f:
    for line in f.readlines():
        artist = line.strip()
        if artist:
            artists.append(artist)

for artist in artists:
    print(f'Getting data for {artist}')
    results = musicbrainzngs.search_artists(artist=artist)
    if results['artist-count'] > 0:
        artistdata = results['artist-list'][0]
    else:
        print(f'Artist {artist} not found')
    print(f'{artist}: {artistdata["id"]}')
    releases = musicbrainzngs.get_artist_by_id(artistdata['id'], includes=["release-groups"])['artist']['release-group-list']
    for release in releases:
        print(f'\t{release["title"]}: {release["first-release-date"]}')
        try:
            if len(release['first-release-date']) == 4:
                releasedate = datetime.strptime(release['first-release-date'], '%Y')
            elif len(release['first-release-date']) == 7:
                releasedate = datetime.strptime(release['first-release-date'], '%Y-%m')
            elif len(release['first-release-date']) == 0:
                releasedate = datetime.strptime('1900', '%Y')
            else:
                releasedate = datetime.strptime(release['first-release-date'], '%Y-%m-%d')
        except ValueError as e:
            print(f'Error parsing date {release["first-release-date"]}')
            print(json.dumps(release, indent=4))
            raise e
    #print(json.dumps(artistdata, indent=4))


pdb.set_trace()
