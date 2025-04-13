# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================


def gui(self, Gtk, vboxstack19, fn, fixes):
    """create a gui"""
    hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox1_label = Gtk.Label(xalign=0)
    hbox1_label.set_text("Fixes")
    hbox1_label.set_name("title")
    hbox1.pack_start(hbox1_label, False, False, 10)

    hbox0 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    hbox0.pack_start(hseparator, True, True, 0)

    hbox13 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox13_label = Gtk.Label(xalign=0)
    hbox13_label.set_text("Choose your cursor globally - /usr/share/icons/default")
    self.cursor_themes = Gtk.ComboBoxText()
    fixes.pop_gtk_cursor_names(self.cursor_themes)
    btn_apply_cursor = Gtk.Button(label="Apply")
    btn_apply_cursor.connect("clicked", self.on_click_apply_global_cursor)
    hbox13.pack_start(hbox13_label, False, False, 10)
    hbox13.pack_end(btn_apply_cursor, False, False, 10)
    hbox13.pack_end(self.cursor_themes, False, False, 10)

    hbox14 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox14_label = Gtk.Label(xalign=0)
    hbox14_label.set_markup("Provide probe link")
    btn_probe = Gtk.Button(label="Get probe link")
    btn_probe.connect("clicked", self.on_click_probe)
    hbox14.pack_start(hbox14_label, False, False, 10)
    hbox14.pack_end(btn_probe, False, False, 10)

    # ======================================================================
    #                       VBOX STACK
    # ======================================================================

    vboxstack19.pack_start(hbox1, False, False, 0)
    vboxstack19.pack_start(hbox0, False, False, 0)
    vboxstack19.pack_start(hbox14, False, False, 0)
    vboxstack19.pack_start(hbox13, False, False, 0)
