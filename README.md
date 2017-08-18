# screen2html
[![Build Status](https://travis-ci.org/johndoe31415/screen2html.svg?branch=master)](https://travis-ci.org/johndoe31415/screen2html)

This tool converts text that contains ANSI escape sequences for coloring or
formatting text (bold, underline, italics) to HTML, trying to preserve the
original terminal colors as closely as possible. One use case is to record a
screen session to a screen logfile and convert this to HTML (where you'd
otherwise make a non-copy/pastable screenshot if you wanted to preserve the
original colors). You can view an example here:
[https://johndoe31415.github.io/screen2html/](https://johndoe31415.github.io/screen2html/)
To use screen2html, you first need to use the log recording mechanism of
screen. This is achieved either by hitting "Ctrl-A H" during a running screen
session or by invoking screen with the "-L" argument, such as:

```
$ screen -L mylog.txt
```

Note that old versions of screen do not support setting the filename with the
"-L" option (my version 4.05.00 of 2016-12-10 does) -- these versions will
create a ```screenlog.*``` file instead.

Afterwards, you can run your logfile by screen2html, which will parse the
contained ANSI escape sequences and produce HTML that honors them. For example:

```
$ ./screen2html --complete-html --css-mode=style screenlog.0 >screen.html
```

The help-page should be self-explanatory:

```
usage: screen2html [-h] [--complete-html] [--html-css-inclusion {link,style}]
                   [--css-filename filename] [--css-mode {class,style}]
                   [--write-css] [--full-css] [-p configfile] [-s name]
                   [-b index] [-f index] [-c class]
                   filename

positional arguments:
  filename              Screen logfile that should be converted to HTML.

optional arguments:
  -h, --help            show this help message and exit
  --complete-html       Generate a complete HTML file that can be directly
                        rendered in the browser.
  --html-css-inclusion {link,style}
                        When generating a complete HTML example, determines
                        how CSS is referenced when css-mode is 'class'. This
                        can be either a link to the CSS file ('link') or
                        included verbatim as a <style> tag ('style'). Defaults
                        to link.
  --css-filename filename
                        When generating a complete HTML file, specifies the
                        filename of the CSS to include. Defaults to terminal-
                        tango.css.
  --css-mode {class,style}
                        Choose how CSS attributes are selected. 'class'
                        includes class attributes that refer to CSS. 'style'
                        does not reference CSS classes, but puts everything
                        inline inside 'style' attributes directly. Defaults to
                        link.
  --write-css           Do not only put the name of the CSS filename in the
                        'link' tag of an example HTML, but also write CSS file
                        itself.
  --full-css            Write a full CSS file containing all classes, not just
                        those classes which are needed to render the
                        particular log output.
  -p configfile, --schemes-config configfile
                        Specifies the color schemes configuration file that is
                        read in and contains color master data. Defaults to
                        color_schemes.ini.
  -s name, --scheme name
                        Color scheme to pick from configuration file. Defaults
                        to tango.
  -b index, --bgcolor index
                        Background color index that is assumed as default.
                        Defaults to 0 (black).
  -f index, --fgcolor index
                        Foreground color index that is assumed as default.
                        Defaults to 7 (white).
  -c class, --classname class
                        CSS class to use for terminal <pre>. Defaults to
                        xterm.
```

The CSS can also be written out by specifying the `--write-css` parameter
(otherwise it is not overwritten by default).


# Requirements
screen2html requires vanilla Python3, but does not have any other dependencies.


# License
Licensed under the GNU GPL-3 (later versions of the GPL excluded).
