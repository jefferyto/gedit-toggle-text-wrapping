# Toggle Text Wrapping, a plugin for gedit #

Quickly toggle text wrapping from the View menu or Toolbar  
<https://github.com/jefferyto/gedit-toggle-text-wrapping>  
0.3.1

All bug reports, feature requests and miscellaneous comments are welcome
at the [project issue tracker][].

## Requirements ##

0.3.0 and higher requires gedit 3; gedit 2 users should use [0.2.0][] by
Christian Hartmann.

## Installation ##

1.  Download the source code (as [zip][] or [tar.gz][]) and extract.
2.  Copy the `toggletextwrapping` folder and the appropriate `.plugin`
    file into `~/.local/share/gedit/plugins` (create if it does not
    exist):
    *   For gedit 3.6 and earlier, copy
        `toggletextwrapping.plugin.python2` and rename to
        `toggletextwrapping.plugin`.
    *   For gedit 3.8 and later, copy `toggletextwrapping.plugin`.
3.  Restart gedit, select **Edit > Preferences** (or
    **gedit > Preferences** on Mac), and enable the plugin in the
    **Plugins** tab.

## Usage ##

To toggle text wrapping for the current document, either:

*   Select **View > Text Wrap**;
*   Click the checkmark button in the Toolbar; or
*   Use the <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>B</kbd> keyboard
    shortcut.

Note that this only affects the current (active) document; text wrapping
for documents in other tabs and/or windows will be unaffected, and the
global text wrapping preferences will remain unchanged.

## Credits ##

Christian Hartmann:  
Parts of this plugin are based on the work of Mike Doty <mike@psyguygames.com>
who wrote the infamous SplitView plugin. The rest is inspired from the Python
Plugin Howto document and the Python-GTK documentation.

Francisco Franchetti:  
This plugin was developed for gedit 2 by Christian Hartmann at <christian.hartmann@berlin.de>.

Jeffery To:  
Based on the work by Christian Hartmann and Francisco Franchetti :-)

## License ##

Copyright &copy; 2008-2009 Christian Hartmann <christian.hartmann@berlin.de>  
Copyright &copy; 2011 Francisco Franchetti <nixahn@gmail.com>  
Copyright &copy; 2013 Jeffery To <jeffery.to@gmail.com>

Available under GNU General Public License version 3


[project issue tracker]: https://github.com/jefferyto/gedit-toggle-text-wrapping/issues
[zip]: https://github.com/jefferyto/gedit-toggle-text-wrapping/archive/master.zip
[tar.gz]: https://github.com/jefferyto/gedit-toggle-text-wrapping/archive/master.tar.gz
[0.2.0]: http://hartmann-it-design.de/gedit/TextWrap/index.html
