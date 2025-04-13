#!/usr/bin/env python3

# ============================================================
# Inspired by Arch Linux Tweak Tool
# ============================================================
# pylint:disable=C0103,C0115,C0116,C0411,C0413,E1101,E0213,I1101,R0902,R0904,R0912,R0913,R0914,R0915,R0916,R1705,W0613,W0621,W0622,W0702,W0703
# pylint:disable=C0301,C0302 #line too long
import gi

gi.require_version("Gtk", "3.0")

import design
import support
import splash
import settings
import login
import fixes
import gui
import desktopr
from subprocess import call
import os
import subprocess
import signal
import datetime
import functions as fn


from gi.repository import Gdk, GdkPixbuf, Gtk, Pango, GLib
from os import readlink

# from time import sleep
# from subprocess import PIPE, STDOUT, call
# import polybar


base_dir = fn.path.dirname(fn.path.realpath(__file__))

class Main(Gtk.Window):
    def __init__(self):
        print(
            "---------------------------------------------------------------------------"
        )
        print("If you have errors, report it on Athena GitHub project or Athena Discord Server")
        print(
            "---------------------------------------------------------------------------"
        )
        print("Link:")
        print(" - Athena OS - https://athenaos.org/")
        print(
            "---------------------------------------------------------------------------"
        )
        print("Backups of files related to the ATT are created.")
        print("You can recognize them by the extension .bak or .back")
        print("If we have a reset button, the backup file will be used")
        print(
            "---------------------------------------------------------------------------"
        )
        print("[INFO] : pkgver = pkgversion")
        print("[INFO] : pkgrel = pkgrelease")
        print(
            "---------------------------------------------------------------------------"
        )
        print("[INFO] : Distro = " + fn.distr)
        print(
            "---------------------------------------------------------------------------"
        )

        print("[INFO] : User = " + fn.sudo_username)
        fn.findgroup()
        print(
            "---------------------------------------------------------------------------"
        )
        super(Main, self).__init__(title="Athena Tweak Tool")
        self.set_border_width(10)
        self.connect("delete-event", self.on_close)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_icon_from_file(fn.path.join(base_dir, "images/archlinux.png"))
        self.set_default_size(1150, 920)

        self.opened = True
        self.firstrun = True
        # self.desktop = ""
        self.timeout_id = None

        self.design_status = Gtk.Label()
        self.desktop_status = Gtk.Label()
        self.login_status = Gtk.Label()
        self.image_design = Gtk.Image()
        self.image_DE = Gtk.Image()
        self.image_login = Gtk.Image()

        self.grub_image_path = ""
        self.login_wallpaper_path = ""
        self.fb = Gtk.FlowBox()
        self.flowbox_wall = Gtk.FlowBox()

        splScr = splash.SplashScreen()

        while Gtk.events_pending():
            Gtk.main_iteration()

        # =====================================================
        #     ENSURING WE HAVE THE DIRECTORIES WE NEED
        # =====================================================

        # ensuring we have a directory for backups
        if not fn.path.isdir(fn.home + "/.config/athena-tweak-tool"):
            try:
                fn.makedirs(fn.home + "/.config/athena-tweak-tool", 0o766)
                fn.permissions(fn.home + "/.config/athena-tweak-tool")
            except Exception as error:
                print(error)

        # if there is a file called default remove it
        if fn.path.isfile("/usr/share/icons/default"):
            try:
                fn.unlink("/usr/share/icons/default")
            except Exception as error:
                print(error)

        # ensuring we have an index.theme
        if not fn.path.isdir("/usr/share/icons/default"):
            try:
                fn.makedirs("/usr/share/icons/default", 0o755)
            except Exception as error:
                print(error)

        if not fn.path.isfile("/usr/share/icons/default/index.theme"):
            if fn.path.isfile("/usr/share/icons/default/index.theme.bak"):
                try:
                    fn.shutil.copy(
                        "/usr/share/icons/default/index.theme.bak",
                        "/usr/share/icons/default/index.theme",
                    )
                except Exception as error:
                    print(error)
            else:
                try:
                    fn.shutil.copy(
                        "/usr/share/athena-tweak-tool/data/arco/cursor/index.theme",
                        "/usr/share/icons/default/index.theme",
                    )
                except Exception as error:
                    print(error)


        # =====================================================
        #      LAUNCHING GUI AND SETTING ALL THE OBJECTS
        # =====================================================

        gui.gui(self, Gtk, Gdk, GdkPixbuf, base_dir, os, Pango)

        # ====================DESIGN INSTALL===================

        self.button_install_design.set_sensitive(True)

        # ====================DESKTOP INSTALL===================

        self.button_install_desktop.set_sensitive(True)

        # ====================LOGIN INSTALL===================

        self.button_install_login.set_sensitive(True)

        # Create att.lock

        if not fn.path.isfile("/tmp/att.lock"):
            with open("/tmp/att.lock", "w", encoding="utf-8") as f:
                f.write("")

        # =====================================================
        #     IF ALL THIS IS DONE - DESTROY SPLASH SCREEN
        # =====================================================

        splScr.destroy()

    # =====================================================
    # =====================================================
    # =====================================================
    # =====================================================
    #     END OF DEF __INIT__(SELF)
    # =====================================================
    # =====================================================
    # =====================================================
    # =====================================================

    # ================================================================================
    # ================================================================================
    # ================================================================================
    # ================================================================================
    # ================================================================================
    # ================================================================================
    #                MAIN FUNCTIONS
    # ================================================================================
    # ================================================================================
    # ================================================================================
    # ================================================================================
    # ================================================================================
    # ================================================================================

    #    #====================================================================
    #    #                       DESIGN
    #    #====================================================================

    def on_d_combo_changed_design(self, widget):
        try:
            pixbuf3 = GdkPixbuf.Pixbuf().new_from_file_at_size(
                base_dir + "/design_data/" + self.d_combo_design.get_active_text().lower().replace(" ", "") + ".png",
                345,
                345,
            )
            self.image_design.set_from_pixbuf(pixbuf3)
        except:
            self.image_design.set_from_pixbuf(None)
        if design.check_design(self.d_combo_design.get_active_text()):
            self.design_status.set_text("This design is installed")
        else:
            self.design_status.set_text("This design is NOT installed")

    def on_install_clicked_design(self, widget, state):
        print("Installing " + self.d_combo_design.get_active_text())
        #design.check_lock(self, self.d_combo_design.get_active_text(), state)
        design.install_design(self, self.d_combo_design.get_active_text(), state, self.manager)

    def on_default_clicked_design(self, widget):
        if design.check_design(self.d_combo_design.get_active_text()) is True:
            secs = settings.read_section()
            if "DESIGN" in secs:
                settings.write_settings(
                    "DESIGN", "default", self.d_combo_design.get_active_text()
                )
            else:
                settings.new_settings(
                    "DESIGN", {"default": self.d_combo_design.get_active_text()}
                )
        else:
            fn.show_in_app_notification(self, "That design is not installed")
            print("The design is not installed")


    #    #====================================================================
    #    #                       DESKTOPR
    #    #====================================================================

    def on_d_combo_changed_desktop(self, widget):
        try:
            pixbuf3 = GdkPixbuf.Pixbuf().new_from_file_at_size(
                base_dir + "/desktop_data/" + self.d_combo_desktop.get_active_text().lower().replace(" ", "_") + ".png",
                345,
                345,
            )
            self.image_DE.set_from_pixbuf(pixbuf3)
        except:
            self.image_DE.set_from_pixbuf(None)
        if desktopr.check_desktop(desktopr.session_mapping.get(self.d_combo_desktop.get_active_text())):
            self.desktop_status.set_text("This desktop is installed")
        else:
            self.desktop_status.set_text("This desktop is NOT installed")

    def on_install_clicked_desktop(self, widget, state):
        print("Installing " + self.d_combo_desktop.get_active_text())
        #desktopr.check_lock(self, self.d_combo_desktop.get_active_text(), state)
        desktopr.install_desktop(self, self.d_combo_desktop.get_active_text(), state, self.manager)

    def on_default_clicked_desktop(self, widget):
        if desktopr.check_desktop(desktopr.session_mapping.get(self.d_combo_desktop.get_active_text())) is True:
            secs = settings.read_section()
            if "DESKTOP" in secs:
                settings.write_settings(
                    "DESKTOP", "default", self.d_combo_desktop.get_active_text()
                )
            else:
                settings.new_settings(
                    "DESKTOP", {"default": self.d_combo_desktop.get_active_text()}
                )
        else:
            fn.show_in_app_notification(self, "That desktop is not installed")
            print("Desktop is not installed")


    #    #====================================================================
    #    #                            LOGIN
    #    #====================================================================

    def on_d_combo_changed_login(self, widget):
        try:
            pixbuf3 = GdkPixbuf.Pixbuf().new_from_file_at_size(
                base_dir + "/login_data/" + login.login_mapping.get(self.d_combo_login.get_active_text()) + ".png",
                345,
                345,
            )
            self.image_login.set_from_pixbuf(pixbuf3)
        except:
            self.image_login.set_from_pixbuf(None)
        if login.check_login(self.d_combo_login.get_active_text()):
            self.login_status.set_text("This login is installed")
        else:
            self.login_status.set_text("This login is NOT installed")

    def on_install_clicked_login(self, widget, state):
        print("Installing " + self.d_combo_login.get_active_text())
        login.install_login(self, self.d_combo_login.get_active_text(), state)

    # ====================================================================
    #                       FIXES
    # ====================================================================

    def on_click_probe(self, widget):
        try:
            fn.install_package(self, "hw-probe", self.manager)
            fn.install_package(self, "alacritty", self.manager)
            result = fn.subprocess.call(
                "alacritty --hold -e hw-probe -all -upload",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            if result == 0:
                print("Probe link has been created")
                GLib.idle_add(
                    fn.show_in_app_notification, self, "Probe link has been created"
                )
            else:
                print(f"Failed to create probe link. Exit code: {result}")
                GLib.idle_add(
                    fn.show_in_app_notification,
                    self,
                    f"Failed to create probe link. Exit code: {result}",
                )
        except Exception as error:
            print(error)

    def on_click_apply_global_cursor(self, widget):
        cursor = self.cursor_themes.get_active_text()
        fixes.set_global_cursor(self, cursor)
        print("Cursor is saved in /usr/share/icons/default")
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "Cursor saved in /usr/share/icons/default",
        )


    # =====================================================
    #               PATREON LINK
    # =====================================================

    def on_social_clicked(self, widget, event):
        sup = support.Support(self)
        response = sup.run()

        if response == Gtk.ResponseType.DELETE_EVENT:
            sup.destroy()

    def tooltip_callback(self, widget, x, y, keyboard_mode, tooltip, text):
        tooltip.set_text(text)
        return True


    # ====================================================================
    #                            BOTTOM BUTTONS
    # ====================================================================

    def on_refresh_att_clicked(self, desktop):
        fn.restart_program()

    def on_close(self, widget, data):
        fn.unlink("/tmp/att.lock")
        Gtk.main_quit()

    def on_reload_att_clicked(self, widget):
        fixes.pop_gtk_cursor_names(self.cursor_themes)
        print("Reloaded")

    # ================================================================================
    # ================================================================================
    # ================================================================================
    # ================================================================================
    # ================================================================================
    # ================================================================================
    #                END OF MAIN FUNCTIONS
    # ================================================================================
    # ================================================================================
    # ================================================================================
    # ================================================================================
    # ================================================================================
    # ================================================================================


# ====================================================================
#                       MAIN
# ====================================================================


def signal_handler(sig, frame):
    print("\nATT is Closing.")
    fn.unlink("/tmp/att.lock")
    Gtk.main_quit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    # These lines offer protection and grace when a kernel has obfuscated or removed basic OS functionality.
    os_function_support = True
    try:
        fn.getlogin()
    except:
        os_function_support = False
    if not fn.path.isfile("/tmp/att.lock") and os_function_support:
        with open("/tmp/att.pid", "w", encoding="utf-8") as f:
            f.write(str(fn.getpid()))
            f.close()
        style_provider = Gtk.CssProvider()
        style_provider.load_from_path(base_dir + "/att.css")

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )
        w = Main()
        w.show_all()
        Gtk.main()
    else:
        md = ""

        if os_function_support:
            md = Gtk.MessageDialog(
                parent=Main(),
                flags=0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.YES_NO,
                text="Lock File Found",
            )
            md.format_secondary_markup(
                "The lock file has been found. This indicates there is already an instance of <b>Athena Tweak Tool</b> running.\n\
Click yes to remove the lock file\n\
and try running ATT again"
            )
        else:
            md = Gtk.MessageDialog(
                parent=Main(),
                flags=0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.CLOSE,
                text="Kernel Not Supported",
            )
            md.format_secondary_markup(
                "Your current kernel does not support basic os function calls. <b>Athena Tweak Tool</b> \
requires these to work."
            )

        result = md.run()
        md.destroy()

        if result in (Gtk.ResponseType.OK, Gtk.ResponseType.YES):
            pid = ""
            with open("/tmp/att.pid", "r", encoding="utf-8") as f:
                line = f.read()
                pid = line.rstrip().lstrip()
                f.close()

            try:
                if fn.check_if_process_is_running(int(pid)):
                    md = Gtk.MessageDialog(
                        parent=Main(),
                        flags=0,
                        message_type=Gtk.MessageType.INFO,
                        buttons=Gtk.ButtonsType.CLOSE,
                        text="You first need to close the existing application",
                    )
                    md.format_secondary_markup(
                        "You first need to close the existing application"
                    )
                    result = md.run()
                    md.destroy()
                else:
                    fn.unlink("/tmp/att.lock")
            except:
                print(
                    "Make sure there is just one instance of Athena Tweak Tool running"
                )
                print("Then you can restart the application")
