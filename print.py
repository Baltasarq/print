#! /bin/env python
# (c) 2025 Baltasar MIT License <baltasarq@gmail.com>


from argparse import ArgumentParser
import platform
import sys


if "win" in platform.system().lower():
    DEFAULT_DEVICE = "PRN"
else:
    DEFAULT_DEVICE = "/dev/usb/lp0"
...

ESC_P = {
    "^[": chr(27),
    "^v": chr(12),
    "^l": chr(10),
    "^r": chr(13),
}


def interpret_data(data: str):
    """Interprets the data given as a string.
        The following changes that are carried out
        are stored in the ESC_P dictionary.
        :param data: the data to interpret.
    """
    i = 0
    toret = ""
    while i < len(data):
        ch = data[i]

        if  (ch == '^'
        and (i + 1) < len(data)):
            ch += data[i + 1]
            i += 1
        ...
        
        toret += ESC_P.get(ch, ch)
        i += 1
    ...
    
    return toret
...


class Printer:
    """Class representing the communication with the printer."""
    def __init__(self, device):
        """Creates a new printer using a device.
           If none is provided, then /dev/usb/lp0 is used.
            :param device: the printer device.
        """
        if not device:
            device = DEFAULT_DEVICE
        ...
        
        self.__dev = device
    ...
    
    @property
    def device(self):
        return self.__dev
    ...

    def send(self, data: str):
        """Sends new data to the printer.
            :param data: the data to send to the printer, as str.
        """
        with open(self.device, "wt") as dev:
            dev.write(data)
        ...
    ...

    def sendfile(self, filename: str):
        """Sends a whole file to the printer.
            :param filename: the path of the file to print.
        """
        with open(filename, "rt") as f:
            for l in f:
                self.send(l.rstrip())
                self.send(interpret_data("^r^l"))
            ...
        ...
        
        self.send(interpret_data("^v"))
    ...
...


if __name__ == "__main__":
    parser = ArgumentParser(
                    description="Sending commands to the printer.",
                    epilog="(c) 2026 Baltasar 'retro' printing with ESC/P codes.")

    parser.add_argument("-d", "--dev", help="the device of the printer.")
    parser.add_argument("-v", "--verbose", help="see how to type codes.", action='store_true')
    parser.add_argument("-s", "--send", help="raw data to print.")
    parser.add_argument("-f", "--file", help="the path of a file to print.")

    args = vars(parser.parse_args())

    filename = args.get("file")
    send = args.get("send")
    device = args.get("device")
    verbose = args.get("verbose")

    if verbose:
        print(str.join("\n",
                    ([k.ljust(4) + ": chr(s) " + str.join(", ", (str(ord(ch)) for ch in v))
                                        for k, v in ESC_P.items()])))
        sys.exit(0)
    ...

    if (not filename
    and not send):
        print("[ERR] You must specify at least -f or -s")
        sys.exit(-1)
    ...

    pr = Printer(device)

    if filename:
        pr.sendfile(filename)
    else:
        pr.send(interpret_data(send))
    ...
...
