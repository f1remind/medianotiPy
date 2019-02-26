#!/usr/bin/env python
import musicbrainzngs
from datetime import datetime
import json
import os
import logging
import time # keep while logger isn't implemented

NAME = 'medianotipy'
VERSION = '0.0.1.1'

def main():
    musicbrainzngs.set_useragent(NAME, VERSION)

    artists = get_local_artists()
    cache = get_cache()

    new_releases = []
    for artist in artists:
        if artist in cache:
            artistid = cache[artist]['id']
        else:
            results = musicbrainzngs.search_artists(artist=artist)
            if results['artist-count'] > 0:
                artistid = results['artist-list'][0]['id']
                if results['artist-list'][0]['name'].upper() != artist.upper():
                    print(f'Artist {artist} not found')
                    continue
            else:
                print(f'Artist {artist} not found')
                continue

        print(f'Getting Data for {artist}')
        releases = musicbrainzngs.get_artist_by_id(\
            artistid, includes=["release-groups"], \
            release_type=["album"])['artist']['release-group-list']
        releases = sorted(releases, key=lambda x: x['first-release-date'])
        relevant_releases = []
        for release in releases:

            if release['type'] == 'Compilation':
                continue
            if "secondary-type-list" in release and 'Live' in release['secondary-type-list']:
                continue

            release['artist'] = artist
            relevant_releases.append(release)
            print(f'\t{release["title"]}')


            if artist in cache:
                new_release = True
                for cacherelease in cache[artist]['release-group-list']:
                    if cacherelease['id'] == release['id']:
                        new_release = False
                if new_release:
                    print(f"New release! {release['title']} by {artist}")
                    cache[artist]['release-group-list'].append(release)
                    new_releases.append(release)
            else:
                cache[artist] = {'id':artistid, 'release-group-list':relevant_releases}
    print(f'{len(new_releases)} new releases')
    for release in new_releases:
        print(f'{release["artist"]} - {release["title"]}')
    save_cache(cache)
    return True

def get_cache(path=f'{os.getenv("HOME")}/.{NAME}/cache.json'):
    data = {} 
    if os.path.isfile(path):
        try:
            with open(path) as f:
                data = json.loads(f.read())
        except json.decoder.JSONDecodeError as ex:
            logging.exception("Malformed cache.json")
            print("Couldn't load cache. There was an error parsin the file")
    return data

def save_cache(data, path=f'{os.getenv("HOME")}/.{NAME}/cache.json'):
    print(f'Saving cache to {path}')
    with open(path, 'w') as f:
        f.write(json.dumps(data, indent=4))
    print('Done saving')
    return data

def get_local_artists(path=f'{os.getenv("HOME")}/.{NAME}/artists.txt'):
    artists = []
    if os.path.isfile(path):
        with open(path) as f:
            for line in f.readlines():
                artist = line.strip()
                if artist:
                    artists.append(artist)
    else:
        if not os.path.isdir(path[:path.rfind('/')]):
            os.makedirs(path[:path.rfind('/')])
        with open(path, 'w') as f:
            f.write("")
    return artists

if __name__ == '__main__':
    success = False
    while not success:
        try:
            success = main()
        except KeyboardInterrupt:
            break
        except Exception as ex:
            logging.exception("Exception in main")
