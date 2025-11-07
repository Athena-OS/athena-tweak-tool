# pylint:disable=C0115,I1101

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf
import cairo
import os

base_dir = os.path.dirname(os.path.realpath(__file__))

class SplashScreen(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, Gtk.WindowType.POPUP, title="")
        self.set_decorated(False)
        self.set_resizable(False)
        self.set_size_request(500, 250)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_keep_above(True)

        # Ask for an RGBA visual (window with alpha channel)
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual and self.is_composited():
            self.set_visual(visual)

        # We’ll do our own background
        self.set_app_paintable(True)
        self.connect("draw", self._on_draw_clear)

        main_vbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.add(main_vbox)

        self.image = Gtk.Image()
        pimage = GdkPixbuf.Pixbuf.new_from_file_at_size(
            os.path.join(base_dir, "images", "athenaos-logo.svg"),
            341, 416
        )
        self.image.set_from_pixbuf(pimage)

        main_vbox.pack_start(self.image, True, True, 0)
        self.show_all()

    def _on_draw_clear(self, widget, cr: cairo.Context):
        # Clear the whole window to fully transparent
        cr.set_source_rgba(0, 0, 0, 0)          # transparent
        cr.set_operator(cairo.OPERATOR_SOURCE)  # replace anything underneath
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)    # normal drawing for children
        return False
