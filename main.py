#!/usr/bin/env python3
import world
import ui
from gi.repository import Gtk

def main():
    w = world.World()
    w.parse_and_add('zones.yaml')
    window = ui.MainWindow()
    window.show_all()
    window.setWorld( w )
    Gtk.main()

if __name__ == '__main__':
    main()
