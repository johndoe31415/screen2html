# screen2html
This converts terminal output, recorded by the GNU screen utility, to
formatting that preserves the original terminal colors. You can view an example
here: [https://johndoe31415.github.io/screen2html/](https://johndoe31415.github.io/screen2html/)
To use screen2html, you first need to use the log recording mechanism of
screen. This is achieved either by hitting "Ctrl-A H" during a running screen
session or by invoking screen with the "-L" argument, such as:

```
$ screen -L mylog.txt
```

Afterwards, you can run your logfile by screen2html, which will parse the
contained ANSI escape sequences and produce HTML that honors them. For example:

```
$ ./screen2html mylog.txt >mylog.html
```

The help-page should be self-explanatory:

```
usage: screen2html [-h] [--complete-html] [--css-filename filename]
                   [--css-verbatim] [-c class]
                   filename

positional arguments:
  filename              Screen logfile that should be converted to HTML.

optional arguments:
  -h, --help            show this help message and exit
  --complete-html       Generate a complete HTML file that can be directly
                        rendered in the browser.
  --css-filename filename
                        When generating a complete HTML file, specifies the
                        filename of the CSS to include. Defaults to terminal-
                        tango.css.
  --css-verbatim        When generating a complete HTML file, include the
                        specified CSS file verbatim, i.e., inside the HTML via
                        <style>, instead of by a <link> reference.
  -c class, --classname class
                        CSS class to use in HTML for terminal <pre>. Defaults
                        to xterm.
```


# CSS
You can specify a palette file in simple INI format, as seen in palette.ini.
Four standard palettes are already available and have been ripped from the
mate-terminal source code (using the "parse_mate_terminal" tool): tango, linux,
xterm and rxvt. First, either edit the palette INI file to your wishes, then
generate a CSS by running

```
$ ./mkcss -s mycolscheme >my_terminal.css
```

A help page is available and should, again, be self-explanatory:

```
usage: mkcss [-h] [-p configfile] [-s name] [-c class] [-b index] [-f index]

optional arguments:
  -h, --help            show this help message and exit
  -p configfile, --palette configfile
                        Specifies the palette file that is read in. Defaults
                        to palette.ini.
  -s name, --scheme name
                        Color scheme to pick from palette file. Defaults to
                        tango.
  -c class, --classname class
                        HTML class name that will be used in CSS. Defaults to
                        xterm.
  -b index, --bgcolor index
                        Background color index that is assumed as default.
                        Defaults to 0 (black).
  -f index, --fgcolor index
                        Foreground color index that is assumed as default.
                        Defaults to 7 (white).
```


# Requirements
screen2html requires vanilla Python3, but does not have any other dependencies.


# License
Licensed under the GNU GPL-3 (later versions of the GPL excluded).
