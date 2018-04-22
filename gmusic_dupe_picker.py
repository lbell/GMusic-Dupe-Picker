# !/usr/bin/env python

# NO WARRANTIES expressed or implied. This could completely delete everything!
# (I don't see how it would, but if it does, I would like to know about it...)
#
# If you find this useful (it is extraordinarly useful) please consider a small
# monitary hat tip: https://www.paypal.me/333221/5

from gmusicapi import Mobileclient
from getpass import getpass
from collections import defaultdict
from pick import pick

# Rearrange this list or comment out items to customize the display of songs
# in the picker.
order = (
    "track",
    "thumb",
    "length",
    "plays",
    "album",
    "artist",
    "match",
    # "album_count",
)

# Adjust the numbers to alter the column widths:
columns = {
    "track": ("D-Trk", 5),
    "thumb": ("Thumb", 4),
    "album": ("Album", 25),
    "artist": ("Album Artist", 15),
    "match": ("NID", 3),
    "album_count": ("MySongs", 7),
    "length": ("Length", 6),
    "plays": ("Plays", 5),
}


client = Mobileclient()
conn = False

print("\n")
while not conn:
    conn = client.login(
        str(raw_input('Username:')),
        getpass(),
        Mobileclient.FROM_MAC_ADDRESS
    )

print("\n")

print('Getting updated list of all songs. (This may take a while)')
all_songs = client.get_all_songs()

####################################
# Reduce api calls during dev and moderately speed up boot
# ##################################
# import pickle
# with open('pickledsongs', 'wb') as fp:
#     pickle.dump(all_songs, fp)
#
# with open('pickledsongs', 'rb') as fp:
#     all_songs = pickle.load(fp)
####################################

print('Processing %s songs...' % (len(all_songs)))

candidate_songs = defaultdict(list)
album_list = defaultdict(int)
dup_songs = {}
trash_songs = {}


for song in all_songs:
    # Title & Artist only to find same songs in different albums
    key = "%s - by %s" % (song.get('title').encode("utf-8"), song.get('artist').encode("utf-8"))
    key = key.title()

    candidate_songs[key].append(song)
    album_list[song.get('albumId')] += 1  # TODO Not consistent


dict(candidate_songs)
album_list[None] = 999  # placeholder

for key in candidate_songs:
    if len(candidate_songs[key]) > 1:
        dup_songs[key] = candidate_songs[key]


def get_label(song):
    """Creates a "label" for options in pick by processesin song information
    on the fly.

    Note: changing this will require tweaking the "title" option for pick to
    ensure the columns line up.
    """
    discnum = song.get('discNumber', 0)
    tracknum = song.get('trackNumber', 0)
    rate = song.get('rating')
    if rate == "1":
        thumb = "-"
    elif rate == "5":
        thumb = "+"
    else:
        thumb = ""
    album_count = album_list.get(song.get('albumId'))  # TODO inconsistent?
    if album_count == 999:
        album_count = ' UsrDef'
    dur = int(song.get('durationMillis', 0))
    length = "{}:{:02d}".format((dur / (1000 * 60)) % 60, (dur / 1000) % 60)

    values = {
        "track": "{:2}-{:02d}".format(discnum, tracknum),
        "thumb": thumb,
        "album": song.get('album').encode("utf-8"),
        "artist": song.get('albumArtist').encode("utf-8"),
        "album_count": album_count,
        "match": 'Y' if song.get('nid') else 'N',
        "length": length,
        "plays": song.get('playCount', 0)
    }

    label = ""
    for item in order:
        col = columns[item]
        val = str(values.get(item))
        label += " {:{width}s} |".format(val[:col[1]], width=col[1])
    label = label[1:][:-1]

    return label


header = ""
for item in order:
    col = columns[item]
    header += " {:{width}s} |".format(col[0][:col[1]], width=col[1])
header = "  " + header[1:][:-1]

numdup = str(len(dup_songs))
count = 1
for item in sorted(dup_songs, key=lambda item: dup_songs[item][0].get('artist'), reverse=False):
    options = dup_songs[item]
    title = ("\n\n\n" +
             "(" + str(count) + " of " + numdup + ")\n" +
             "Select all of the songs to be DELETED using arrow and space. Hit ENTER to DELETE selected.\n" +
             "(This is NOT reversable. There will be no warnings. Proceed with caution.)" +
             "\n\n\n\n  " +
             item +
             "\n\n" +
             header
             )

    selected = pick(options, title, multi_select=True, indicator='*', options_map_func=get_label)

    if len(selected):
        delete_ids = []
        delete_songs = []
        for item in selected:
            delete_ids.append(item[0]['id'])
            print("Deleting: [%s] from [%s]..." % (item[0]['title'], item[0]['album']))
        client.delete_songs(delete_ids)

    count += 1

print('\n\nAll done. Bye!')
