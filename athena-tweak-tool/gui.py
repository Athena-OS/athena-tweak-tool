# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

# ============Functions============
import functions as fn

import desktopr
import fixes
import login
import design

# import template

# =============GUI=================
import desktopr_gui
import fixes_gui
import login_gui
import design_gui

# import Template_GUI
# import Polybar_GUI


def gui(self, Gtk, Gdk, GdkPixbuf, base_dir, os, Pango):
    """creation of the gui"""

    # =======================================================
    #                       App Notifications
    # =======================================================

    hbox0 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

    self.notification_revealer = Gtk.Revealer()
    self.notification_revealer.set_reveal_child(False)

    self.notification_label = Gtk.Label()

    pb_panel = GdkPixbuf.Pixbuf().new_from_file(base_dir + "/images/panel.png")
    panel = Gtk.Image().new_from_pixbuf(pb_panel)

    overlayframe = Gtk.Overlay()
    overlayframe.add(panel)
    overlayframe.add_overlay(self.notification_label)

    self.notification_revealer.add(overlayframe)

    hbox0.pack_start(self.notification_revealer, True, False, 0)

    # ==========================================================
    #                       CONTAINER
    # ==========================================================

    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
    vbox1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
    hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

    vbox.pack_start(hbox, True, True, 0)
    self.add(vbox)

    # ==========================================================
    #                    INITIALIZE STACK
    # ==========================================================
    stack = Gtk.Stack()
    stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
    stack.set_transition_duration(350)

    vboxstack12 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    # vboxstack15 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack16 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    # vboxstack17 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack19 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    # vboxstack21 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack22 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack24 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

    # ==========================================================
    #                DESKTOP
    # ==========================================================

    desktopr_gui.gui(self, Gtk, GdkPixbuf, vboxstack12, desktopr, fn, base_dir, Pango)

    # ==========================================================
    #                 DESIGN
    # ==========================================================

    design_gui.gui(self, Gtk, GdkPixbuf, vboxstack24, design, fn, base_dir, Pango)

    # ==========================================================
    #                         LOGIN
    # ==========================================================

    #login_gui.gui(self, Gtk, vboxstack22, sddm, lightdm, lxdm, fn, login)
    login_gui.gui(self, Gtk, GdkPixbuf, vboxstack22, login, fn, base_dir, Pango)

    # # ==========================================================
    # #               FIXES
    # # ==========================================================

    fixes_gui.gui(self, Gtk, vboxstack19, fn, fixes)

    # ==========================================================
    #                   ADD TO WINDOW
    # ==========================================================

    stack.add_titled(vboxstack24, "stack24", "Design")  # Design

    stack.add_titled(vboxstack12, "stack12", "Desktop")  # Desktop installer

    stack.add_titled(vboxstack22, "stack22", "Login")

    stack.add_titled(vboxstack19, "stack19", "Fixes")  # Fixes

    stack_switcher = Gtk.StackSidebar()
    stack_switcher.set_name("sidebar")
    stack_switcher.set_stack(stack)

    # =====================================================
    #                       LOGO
    # =====================================================

    ivbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    # pixbuf = GdkPixbuf.Pixbuf().new_from_file_at_size
    # (fn.path.join(base_dir, 'images/arcolinux-stock.png'), 45, 45)
    # image = Gtk.Image().new_from_pixbuf(pixbuf)

    # =====================================================
    #               PACKAGE MANAGER CHOICE
    # =====================================================

    def on_pkg_manager_changed(combo):
        self.manager = combo.get_active_text()
        print("Selected manager:", self.manager)

    # =====================================================
    #               RESTART/QUIT BUTTON
    # =====================================================

    def on_quit(self):
        fn.unlink("/tmp/att.lock")
        Gtk.main_quit()
        print("Thanks for using Athena Tweak Tool")
        print("Report issues to make it even better")
        print(
            "---------------------------------------------------------------------------"
        )

    lbl_distro = Gtk.Label(xalign=0)
    lbl_distro.set_markup("Working on\nAthena OS")
    # Dropdown for selecting package manager
    pkg_manager_combo = Gtk.ComboBoxText()
    pkg_manager_combo.append_text("dnf")
    pkg_manager_combo.append_text("rpm-ostree")
    pkg_manager_combo.set_active(0)  # default to dnf
    self.manager = pkg_manager_combo.get_active_text()
    pkg_manager_combo.connect("changed", on_pkg_manager_changed)
    btn_reload_att = Gtk.Button(label="Reload ATT")
    btn_reload_att.set_size_request(100, 30)
    btn_reload_att.connect("clicked", self.on_reload_att_clicked)
    btn_restart_att = Gtk.Button(label="Restart ATT")
    btn_restart_att.set_size_request(100, 30)
    btn_restart_att.connect("clicked", self.on_refresh_att_clicked)
    btn_quit_att = Gtk.Button(label="Quit ATT")
    btn_quit_att.set_size_request(100, 30)
    btn_quit_att.connect("clicked", on_quit)

    # =====================================================
    #               SUPPORT LINK
    # =====================================================
    support_eventbox = Gtk.EventBox()

    pbp = GdkPixbuf.Pixbuf().new_from_file_at_size(
        fn.path.join(base_dir, "images/support.png"), 58, 58
    )
    pimage = Gtk.Image().new_from_pixbuf(pbp)

    support_eventbox.add(pimage)

    support_eventbox.connect("button_press_event", self.on_social_clicked)
    support_eventbox.set_property("has-tooltip", True)

    support_eventbox.connect(
        "query-tooltip", self.tooltip_callback, "Support or get support"
    )

    # =====================================================
    #                      PACKS
    # =====================================================

    hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
    hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
    hbox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
    hbox4 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
    hbox5 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
    hbox6 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)

    hbox1.pack_start(support_eventbox, False, False, 0)
    hbox2.pack_start(lbl_distro, False, False, 0)
    hbox5.pack_start(pkg_manager_combo, False, False, 10)
    #hbox6.pack_start(btn_reload_att, False, False, 0)
    hbox3.pack_start(btn_restart_att, False, False, 0)
    hbox4.pack_start(btn_quit_att, False, False, 0)

    # ivbox.pack_start(image, False, False, 0)
    ivbox.pack_start(stack_switcher, True, True, 0)

    ivbox.pack_start(hbox1, False, False, 0)
    ivbox.pack_start(hbox2, False, False, 0)
    ivbox.pack_start(hbox5, False, False, 0)
    ivbox.pack_start(hbox3, False, False, 0)
    ivbox.pack_start(hbox4, False, False, 0)

    vbox1.pack_start(hbox0, False, False, 0)
    vbox1.pack_start(stack, True, True, 0)

    # make the content scrollable
    scrolledWindow = Gtk.ScrolledWindow()
    scrolledWindow.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
    scrolledWindow.add(vbox1)

    hbox.pack_start(ivbox, False, True, 0)
    # hbox.pack_start(vbox1, True, True, 0)
    hbox.pack_start(scrolledWindow, True, True, 0)

    stack.set_hhomogeneous(False)
    stack.set_vhomogeneous(False)
