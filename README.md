# Print

A printing utiliy using plain text codes. It prints ASCII directly to the printer, and makes possible to send control codes, like the following:

```
^[  : chr(s) 27
^v  : chr(s) 12
^l  : chr(s) 10
^r  : chr(s) 13
```

It allows to print a file or to print a character string directly. For instance:

```
python print.py --send Hola!^v
```

Will print "hola" on paper, and immediately will feed a whole page out.

```
python print.py --file print.py
```
The above will print the contents of the `print.py` file, as plain text.

By default, it uses `PRN` on Windows, and `/dev/usb/lp0` on Linux or UNIX. The device can still be specified in the command line, though:

```
python print.py --dev /dev/lp0 --file print.py
```
