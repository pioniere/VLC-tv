# VLC-tv
Python based IPTV streams player for VLC.

VLC-tv provides a simple interface (both command line and GUI) that allows users to easily watch streaming IPTV content through VLC. While it is simple enough to watch single IPTV streams through VLC, there is no easy way to maintain a list of commonly watched channels, or to easily switch between them. These Python scripts solve that problem. Both scripts use the **python-vlc** module to stream the content and the **pickledb** module to store and access channel stream entries. There is probably a cleaner way to store and access this data, but for this it was pickledb. The GUI uses the excellent **PySimpleGUI**. Of course, you will also need to have VLC installed.

Both the command line and GUI versions are easy to use and fairly self-explanatory. The Python code is far from perfect and provided as is, where is, with no warranty. Others are encouraged to make additions and improvements.
## The tv.db file
The tv.db file referred to in the source code is in the following format for pickledb:
```python
{"First Channel Name", "http://your.iptvprovider.com/firstchannel.ts",
"Second Channel Name", "http://your.iptvprovider.com/secondchannel.ts"}
```
It is probably easiest to create this list manually to begin with, although the GUI has the capability to add individual channels. Again, others are encouraged to make additions and improvements. The URLs can contain any streaming format that VLC supports.

## Links
* [python-vlc](https://github.com/oaubert/python-vlc)
* [pickledb](https://github.com/patx/pickledb)
* [pysimplegui](https://github.com/PySimpleGUI/PySimpleGUI)
* [VLC](https://www.videolan.org/vlc/)
