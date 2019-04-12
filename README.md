# MedianotiPY

## Description

A simple tool to keep up with new releases from your favorite bands.

## How it works

This tool connects to the musicbrainz API to fetch a list of all _albums_ from artists declared in the configuration.
Singles or live albums are currently *not* causing notifications.

The initial fetching of any artist does not cause notifications.
The results are saved to a cache and compared with each run.

## Configuration

The program fetches a list of artists from $HOME/.medianotipy/artists.txt separated by newlines.

The cache of previous results is saved to $HOME/.medianotipy/cache.json in json-format.

## TODO

* Support notification by mail and run periodically in the background.
* Proper documentation with docstrings
* Make available using pip
* Create simple configuration options to also notify when new singles or live albums are released.
* Parameterize the artists file instead of using a fixed path

