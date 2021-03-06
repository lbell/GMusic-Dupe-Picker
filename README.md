# GMusic-Dupe-Picker
Interactive Python script for selectively deleting duplicate songs in a Google Play Music library.

Let's face it: although Google Music excels in a lot of areas, library management is not one of those areas. Rather than visually scanning through your music online to find duplicates, then right-clicking, finding delete, confirming the ones you want to get rid of for hours on end, use this wholly analog script to quickly blast duplicate songs in your library.

Finds songs based on Artist and Song name (without regards to album) so you can decide if you want to keep the live version of song X or the studio version, or both.

(_Note: To greatly reduce your effort, try using this script first: https://gist.github.com/lbell/1f05dbed9aa53a2a83c918ceb13021aa to automatically remove "exact" duplicates -- ie, songs with the same artist and title IN THE SAME ALBUM._)

## Usage:
Simply download the script and run `python <scriptname>.py`

Login, then highlight the version(s) of each song you want to DELETE using the `arrow keys` and `spacebar`. Hit `enter` to blast duplicates and go to the next grouping.

Hitting `enter` with no selection will skip. `Ctrl-x` will exit.

Listening to this while doing it helps: https://youtu.be/rY0WxgSXdEE?t=5s

## Requires:
* GMusicapi: https://pypi.org/project/gmusicapi/ or `pip install gmusicapi`
* Pick: https://pypi.org/project/pick/ `pip install pick`

## Appeal: 
This tool works for me. It may not work for you. BUT, if it does, and makes your life easier, please consider a monitary hat tip: http://paypal.me/333221
