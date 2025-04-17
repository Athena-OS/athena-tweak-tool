#!/usr/bin/env python3

# ============================================================
# Inspired by Arch Linux Tweak Tool
# ============================================================
# pylint:disable=C0103,C0115,C0116,C0411,C0413,E1101,E0213,I1101,R0902,R0904,R0912,R0913,R0914,R0915,R0916,R1705,W0613,W0621,W0622,W0702,W0703
# pylint:disable=C0301,C0302 #line too long

import zsh_theme
import design
import terminals
import support
import splash
import settings
import services
import pacman_functions
import login
import fixes
import gui
import desktopr
from packages_prompt_gui import PackagesPromptGui
from subprocess import call
import os
import subprocess
import signal
import datetime
import functions as fn
import gi


gi.require_version("Gtk", "3.0")
from gi.repository import Gdk, GdkPixbuf, Gtk, Pango, GLib
from os import readlink

# from time import sleep
# from subprocess import PIPE, STDOUT, call
# import polybar


base_dir = fn.path.dirname(fn.path.realpath(__file__))
pmf = pacman_functions


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

        # t = fn.threading.Thread(target=fn.get_desktop,
        #                                args=(self,))
        # t.daemon = True
        # t.start()
        # t.join()

        # print(self.desktop)

        # in a video ATT did not change - lateron it did...?
        # if fn.path.isdir("/root/.config/xfce4/xfconf/xfce-perchannel-xml/"):
        #     try:
        #         fn.shutil.rmtree("/root/.config/xfce4/xfconf/xfce-perchannel-xml/")
        #         if fn.path.isdir(
        #             fn.home + "/.config/xfce4/xfconf/xfce-perchannel-xml/"
        #         ):
        #             fn.shutil.copytree(
        #                 fn.home + "/.config/xfce4/xfconf/xfce-perchannel-xml/",
        #                 "/root/.config/xfce4/xfconf/xfce-perchannel-xml/",
        #             )
        #     except Exception as error:
        #         print(error)

        # =====================================================
        #     ENSURING WE HAVE THE DIRECTORIES WE NEED
        # =====================================================

        # make directory if it doesn't exist
        if not fn.path.isdir(fn.log_dir):
            try:
                fn.mkdir(fn.log_dir)
            except Exception as error:
                print(error)

        # make directory if it doesn't exist
        if not fn.path.isdir(fn.att_log_dir):
            try:
                fn.mkdir(fn.att_log_dir)
            except Exception as error:
                print(error)

        # ensuring we have a neofetch directory
        if not fn.path.exists(fn.home + "/.config/neofetch"):
            try:
                fn.makedirs(fn.home + "/.config/neofetch", 0o766)
                fn.permissions(fn.home + "/.config/neofetch")
            except Exception as error:
                print(error)

        # ensuring we have a fastfetch directory
        if not fn.path.exists(fn.home + "/.config/fastfetch"):
            try:
                fn.makedirs(fn.home + "/.config/fastfetch", 0o766)
                fn.permissions(fn.home + "/.config/fastfetch")
            except Exception as error:
                print(error)

        # ensuring we have .autostart
        if not fn.path.exists(fn.home + "/.config/autostart"):
            try:
                fn.makedirs(fn.home + "/.config/autostart", 0o766)
                fn.permissions(fn.home + "/.config/autostart")
            except Exception as error:
                print(error)

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
        #                   MAKING BACKUPS
        # =====================================================

        # ensuring we have a backup of index.theme
        if fn.path.exists("/usr/share/icons/default/index.theme"):
            if not fn.path.isfile("/usr/share/icons/default/index.theme" + ".bak"):
                try:
                    fn.shutil.copy(
                        "/usr/share/icons/default/index.theme",
                        "/usr/share/icons/default/index.theme" + ".bak",
                    )
                except Exception as error:
                    print(error)

        # ensuring we have a backup of samba.conf
        if fn.path.exists("/etc/samba/smb.conf"):
            if not fn.path.isfile("/etc/samba/smb.conf" + ".bak"):
                try:
                    fn.shutil.copy(
                        "/etc/samba/smb.conf", "/etc/samba/smb.conf" + ".bak"
                    )
                except Exception as error:
                    print(error)

        # ensuring we have a backup of the nsswitch.conf
        if fn.path.exists("/etc/nsswitch.conf"):
            if not fn.path.isfile("/etc/nsswitch.conf" + ".bak"):
                try:
                    fn.shutil.copy("/etc/nsswitch.conf", "/etc/nsswitch.conf" + ".bak")
                except Exception as error:
                    print(error)

        # ensuring we have a backup of the config.fish
        if not fn.path.isfile(
            fn.home + "/.config/fish/config.fish" + ".bak"
        ) and fn.path.isfile(fn.home + "/.config/fish/config.fish"):
            try:
                fn.shutil.copy(
                    fn.home + "/.config/fish/config.fish",
                    fn.home + "/.config/fish/config.fish" + ".bak",
                )
                fn.permissions(fn.home + "/.config/fish/config.fish.bak")
            except Exception as error:
                print(error)

        # ensuring we have a backup or the athena mirrorlist
        if fn.path.isfile(fn.athena_mirrorlist):
            if not fn.path.isfile(fn.athena_mirrorlist + ".bak"):
                try:
                    fn.shutil.copy(
                        fn.athena_mirrorlist, fn.athena_mirrorlist + ".bak"
                    )
                except Exception as error:
                    print(error)

        # # ensuring we have a backup or the xerolinux mirrorlist
        # if fn.path.isfile(fn.xerolinux_mirrorlist):
        #     if not fn.path.isfile(fn.xerolinux_mirrorlist + ".bak"):
        #         try:
        #             fn.shutil.copy(
        #                 fn.xerolinux_mirrorlist, fn.xerolinux_mirrorlist + ".bak"
        #             )
        #         except Exception as error:
        #             print(error)

        # ensuring we have a backup of the archlinux mirrorlist
        if fn.path.isfile(fn.mirrorlist):
            if not fn.path.isfile(fn.mirrorlist + ".bak"):
                try:
                    fn.shutil.copy(fn.mirrorlist, fn.mirrorlist + ".bak")
                except Exception as error:
                    print(error)

        # ensuring we have a backup of current /etc/hosts
        if fn.path.isfile("/etc/hosts"):
            try:
                if not fn.path.isfile("/etc/hosts" + ".bak"):
                    fn.shutil.copy("/etc/hosts", "/etc/hosts" + ".bak")
            except Exception as error:
                print(error)

        # make backup of ~/.bashrc
        if fn.path.isfile(fn.bash_config):
            try:
                if not fn.path.isfile(fn.bash_config + ".bak"):
                    fn.shutil.copy(fn.bash_config, fn.bash_config + ".bak")
                    fn.permissions(fn.home + "/.bashrc.bak")
            except Exception as error:
                print(error)

        # make backup of ~/.zshrc
        if fn.path.isfile(fn.zsh_config):
            try:
                if not fn.path.isfile(fn.zsh_config + ".bak"):
                    fn.shutil.copy(fn.zsh_config, fn.zsh_config + ".bak")
                    fn.permissions(fn.home + "/.zshrc.bak")
            except Exception as error:
                print(error)

        # put usable .zshrc file there if nothing
        if not fn.path.isfile(fn.zsh_config):
            try:
                fn.shutil.copy(fn.zshrc_arco, fn.home)
                fn.permissions(fn.home + "/.zshrc")
            except Exception as error:
                print(error)

        # make backup of /etc/pacman.conf
        if fn.path.isfile(fn.pacman):
            if not fn.path.isfile(fn.pacman + ".bak"):
                try:
                    fn.shutil.copy(fn.pacman, fn.pacman + ".bak")
                except Exception as error:
                    print(error)

        # make backup of .config/xfce4/terminal/terminalrc
        if fn.file_check(fn.xfce4_terminal_config):
            try:
                if not fn.path.isfile(fn.xfce4_terminal_config + ".bak"):
                    fn.shutil.copy(
                        fn.xfce4_terminal_config, fn.xfce4_terminal_config + ".bak"
                    )
                    fn.permissions(fn.xfce4_terminal_config + ".bak")
            except Exception as error:
                print(error)

        # make backup of .config/alacritty/alacritty.yml
        if fn.file_check(fn.alacritty_config):
            try:
                if not fn.path.isfile(fn.alacritty_config + ".bak"):
                    fn.shutil.copy(fn.alacritty_config, fn.alacritty_config + ".bak")
                    fn.permissions(fn.alacritty_config + ".bak")
            except Exception as error:
                print(error)

        # =====================================================
        #               CATCHING ERRORS
        # =====================================================

        # ensuring permissions
        a2 = fn.stat(fn.home + "/.config/athena-tweak-tool")
        att = a2.st_uid

        # fixing root permissions if the folder exists
        # can be removed later - 02/11/2021 startdate
        if fn.path.exists(fn.home + "/.config-att"):
            fn.permissions(fn.home + "/.config-att")

        if att == 0:
            fn.permissions(fn.home + "/.config/athena-tweak-tool")
            print("Fixing athena-tweak-tool permissions...")

        if not fn.path.isfile(fn.config):
            key = {"theme": ""}
            settings.make_file("TERMITE", key)
            fn.permissions(fn.config)

        # =====================================================
        #      LAUNCHING GUI AND SETTING ALL THE OBJECTS
        # =====================================================

        gui.gui(self, Gtk, Gdk, GdkPixbuf, base_dir, os, Pango)

        # =====================================================
        #               READING AND SETTING
        # =====================================================

        # ========================ATHENA REPO=============================

        athena_repo = pmf.check_repo("[athena]")

        # ========================ARCO REPO=============================

        arco_testing = pmf.check_repo("[arcolinux_repo_testing]")
        arco_base = pmf.check_repo("[arcolinux_repo]")
        arco_3p = pmf.check_repo("[arcolinux_repo_3party]")
        arco_xl = pmf.check_repo("[arcolinux_repo_xlarge]")

        # ========================ARCH REPO=============================

        arch_testing = pmf.check_repo("[core-testing]")
        arch_core = pmf.check_repo("[core]")
        arch_extra = pmf.check_repo("[extra]")
        arch_community = pmf.check_repo("[extra-testing]")
        arch_multilib_testing = pmf.check_repo("[multilib-testing]")
        arch_multilib = pmf.check_repo("[multilib]")

        # ========================OTHER REPO=============================

        reborn_repo = pmf.check_repo("[Reborn-OS]")
        garuda_repo = pmf.check_repo("[garuda]")
        blackarch_repo = pmf.check_repo("[blackarch]")
        chaotics_repo = pmf.check_repo("[chaotic-aur]")
        endeavouros_repo = pmf.check_repo("[endeavouros]")
        nemesis_repo = pmf.check_repo("[nemesis_repo]")
        # xero_repo = pmf.check_repo("[xerolinux_repo]")
        # xero_xl_repo = pmf.check_repo("[xerolinux_repo_xl]")
        # xero_nv_repo = pmf.check_repo("[xerolinux_nvidia_repo]")

        # ========================ARCO MIRROR=============================

        if fn.path.isfile(fn.arcolinux_mirrorlist):
            arco_mirror_seed = pmf.check_mirror(
                "Server = https://ant.seedhost.eu/arcolinux/$repo/$arch"
            )
            arco_mirror_gitlab = pmf.check_mirror(
                "Server = https://gitlab.com/arcolinux/$repo/-/raw/main/$arch"
            )
            arco_mirror_belnet = pmf.check_mirror(
                "Server = https://ftp.belnet.be/arcolinux/$repo/$arch"
            )
            arco_mirror_accum = pmf.check_mirror(
                "Server = https://mirror.accum.se/mirror/arcolinux.info/$repo/$arch"
            )
            arco_mirror_funami = pmf.check_mirror(
                "Server = https://mirror.funami.tech/arcolinux/$repo/$arch"
            )
            arco_mirror_jingk = pmf.check_mirror(
                "Server = https://mirror.jingk.ai/arcolinux/$repo/$arch"
            )
            arco_mirror_aarnet = pmf.check_mirror(
                "Server = https://mirror.aarnet.edu.au/pub/arcolinux/$repo/$arch"
            )
            # arco_mirror_github = pmf.check_mirror(
            #     "Server = https://arcolinux.github.io/$repo/$arch")

        # ========================ATHENA MIRROR SET TOGGLE=====================

        self.athena_switch.set_active(athena_repo)
        self.opened = False

        # ========================ARCO MIRROR SET TOGGLE=====================

        if fn.path.isfile(fn.arcolinux_mirrorlist):
            self.aseed_button.set_active(arco_mirror_seed)
            self.agitlab_button.set_active(arco_mirror_gitlab)
            self.abelnet_button.set_active(arco_mirror_belnet)
            self.afunami_button.set_active(arco_mirror_funami)
            self.ajingk_button.set_active(arco_mirror_jingk)
            self.aaccum_button.set_active(arco_mirror_accum)
            self.aarnet_button.set_active(arco_mirror_aarnet)
            # self.agithub_button.set_active(arco_mirror_github)

        # ========================ARCO REPO SET TOGGLE=====================

        self.atestrepo_button.set_active(arco_testing)
        self.arepo_button.set_active(arco_base)
        self.a3prepo_button.set_active(arco_3p)
        self.axlrepo_button.set_active(arco_xl)

        # ========================ARCH LINUX REPO SET TOGGLE==================

        self.checkbutton2.set_active(arch_testing)
        self.checkbutton6.set_active(arch_core)
        self.checkbutton7.set_active(arch_extra)
        self.checkbutton5.set_active(arch_community)
        self.checkbutton3.set_active(arch_multilib_testing)
        self.checkbutton8.set_active(arch_multilib)

        # ========================OTHER REPO SET TOGGLE==================

        self.reborn_switch.set_active(reborn_repo)
        self.opened = False
        self.garuda_switch.set_active(garuda_repo)
        self.opened = False
        self.blackarch_switch.set_active(blackarch_repo)
        self.opened = False
        self.chaotics_switch.set_active(chaotics_repo)
        self.opened = False
        self.endeavouros_switch.set_active(endeavouros_repo)
        self.opened = False
        self.nemesis_switch.set_active(nemesis_repo)
        self.opened = False
        # self.xerolinux_switch.set_active(xero_repo)
        # self.opened = False
        # self.xerolinux_xl_switch.set_active(xero_xl_repo)
        # self.opened = False
        # self.xerolinux_nv_switch.set_active(xero_nv_repo)
        # self.opened = False

        # ====================DESIGN INSTALL REINSTALL===================

        if not fn.path.isfile(fn.athena_mirrorlist):
            self.button_install_design.set_sensitive(False)
            self.button_reinstall_design.set_sensitive(False)

        if fn.path.isfile(fn.athena_mirrorlist):
            if fn.check_athena_repos_active() is True:
                self.button_install_design.set_sensitive(True)
                self.button_reinstall_design.set_sensitive(True)
            else:
                self.button_install_design.set_sensitive(False)
                self.button_reinstall_design.set_sensitive(False)

        # ====================DESKTOP INSTALL REINSTALL===================

        if not fn.path.isfile(fn.athena_mirrorlist):
            self.button_install_desktop.set_sensitive(False)
            self.button_reinstall_desktop.set_sensitive(False)

        if fn.path.isfile(fn.athena_mirrorlist):
            if fn.check_athena_repos_active() is True:
                self.button_install_desktop.set_sensitive(True)
                self.button_reinstall_desktop.set_sensitive(True)
            else:
                self.button_install_desktop.set_sensitive(False)
                self.button_reinstall_desktop.set_sensitive(False)

        # ====================LOGIN INSTALL===================

        if not fn.path.isfile(fn.athena_mirrorlist):
            self.button_install_login.set_sensitive(False)

        if fn.path.isfile(fn.athena_mirrorlist):
            if fn.check_athena_repos_active() is True:
                self.button_install_login.set_sensitive(True)
            else:
                self.button_install_login.set_sensitive(False)

    # =====================================================
    
        if not fn.path.isfile("/tmp/att.lock"):
            with open("/tmp/att.lock", "w", encoding="utf8") as f:
                f.write("")

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

    # ====================================================================
    #                       ATHENA MIRRORLIST
    # ====================================================================

    def on_click_reset_athena_mirrorlist(self, widget):
        if fn.path.isfile(fn.athena_mirrorlist_original):
            fn.shutil.copy(fn.athena_mirrorlist_original, fn.athena_mirrorlist)
            fn.show_in_app_notification(
                self, "Original Athena mirrorlist is applied"
            )
        fn.restart_program()

    # ====================================================================
    #                       BASH
    # ====================================================================

    def tobash_apply(self, widget):
        fn.change_shell(self, "bash")

    def on_install_bash_completion_clicked(self, widget):
        fn.install_package(self, "bash")
        fn.install_package(self, "bash-completion")

    def on_remove_bash_completion_clicked(self, widget):
        fn.remove_package(self, "bash-completion")

    def on_arcolinux_bash_clicked(self, widget):
        try:
            if fn.path.isfile(fn.bashrc_arco):
                fn.shutil.copy(fn.bashrc_arco, fn.bash_config)
                fn.permissions(fn.home + "/.bashrc")
            fn.source_shell(self)
        except Exception as error:
            print(error)

        print("ATT ~/.bashrc is applied")
        GLib.idle_add(fn.show_in_app_notification, self, "ATT ~/.bashrc is applied")

    def on_bash_reset_clicked(self, widget):
        try:
            if fn.path.isfile(fn.bash_config + ".bak"):
                fn.shutil.copy(fn.bash_config + ".bak", fn.bash_config)
                fn.permissions(fn.home + "/.bashrc")
        except Exception as error:
            print(error)

        print("Your personal ~/.bashrc is applied again - logout")
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "Your personal ~/.bashrc is applied again - logout",
        )

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
        fn.create_log(self)
        print("Installing " + self.d_combo_design.get_active_text())
        design.check_lock(self, self.d_combo_design.get_active_text(), state)

    def on_default_clicked_design(self, widget):
        fn.create_log(self)
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
        fn.create_log(self)
        print("Installing " + self.d_combo_desktop.get_active_text())
        desktopr.check_lock(self, self.d_combo_desktop.get_active_text(), state)

    def on_default_clicked_desktop(self, widget):
        fn.create_log(self)
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
        fn.create_log(self)
        print("Installing " + self.d_combo_login.get_active_text())
        login.install_login(self, self.d_combo_login.get_active_text(), state)

    #    #====================================================================
    #    #                       FISH
    #    #====================================================================

    def on_install_only_fish_clicked_reboot(self, widget):
        fn.install_package(self, "fish")
        fn.restart_program()

    def on_install_only_fish_clicked(self, widget):
        fn.install_package(self, "fish")
        print("Only Fish has been installed")
        print("Fish is installed without a configuration")
        fn.show_in_app_notification(
            self, "Only the Fish package is installed without a configuration"
        )

    def on_remove_only_fish_clicked(self, widget):
        fn.remove_package(self, "fish")

    def on_arcolinux_fish_package_clicked(self, widget):
        fn.install_arco_package(self, "arcolinux-fish-git")
        if fn.check_package_installed("arcolinux-fish-git") is True:
            # backup whatever is there
            if fn.path_check(fn.home + "/.config/fish"):
                now = datetime.datetime.now()

                if not fn.path.exists(fn.home + "/.config/fish-att"):
                    fn.makedirs(fn.home + "/.config/fish-att")
                    fn.permissions(fn.home + "/.config/fish-att")

                if fn.path.exists(fn.home + "/.config-att"):
                    fn.permissions(fn.home + "/.config-att")

                fn.copy_func(
                    fn.home + "/.config/fish",
                    fn.home
                    + "/.config/fish-att/fish-att-"
                    + now.strftime("%Y-%m-%d-%H-%M-%S"),
                    isdir=True,
                )
                fn.permissions(
                    fn.home
                    + "/.config/fish-att/fish-att-"
                    + now.strftime("%Y-%m-%d-%H-%M-%S")
                )

            fn.copy_func("/etc/skel/.config/fish", fn.home + "/.config/", True)
            fn.permissions(fn.home + "/.config/fish")

            # if there is no file .config/fish
            if not fn.path.isfile(fn.home + "/.config/fish/config.fish"):
                fn.shutil.copy(
                    "/etc/skel/.config/fish/config.fish",
                    fn.home + "/.config/fish/config.fish",
                )
                fn.permissions(fn.home + "/.config/fish/config.fish")

            fn.source_shell(self)
            print(
                "ATT Fish config is installed and your old fish folder (if any) is in ~/.config/fish-att"
            )
            fn.show_in_app_notification(self, "ATT fish config is installed")

    def on_arcolinux_only_fish_clicked(self, widget):
        if not fn.path.isdir(fn.home + "/.config/fish/"):
            try:
                fn.mkdir(fn.home + "/.config/fish/")
                fn.permissions(fn.home + "/.config/fish/")
            except Exception as error:
                print(error)

        if fn.path.isfile(fn.fish_arco):
            fn.shutil.copy(fn.fish_arco, fn.home + "/.config/fish/config.fish")
            fn.permissions(fn.home + "/.config/fish/config.fish")

        if not fn.path.isfile(fn.home + "/.config/fish/config.fish.bak"):
            fn.shutil.copy(fn.fish_arco, fn.home + "/.config/fish/config.fish.bak")
            fn.permissions(fn.home + "/.config/fish/config.fish.bak")

        fn.source_shell(self)
        print("Fish config has been saved")
        fn.show_in_app_notification(self, "Fish config has been saved")

    def on_fish_reset_clicked(self, widget):
        if fn.path.isfile(fn.home + "/.config/fish/config.fish.bak"):
            fn.shutil.copy(
                fn.home + "/.config/fish/config.fish.bak",
                fn.home + "/.config/fish/config.fish",
            )
            fn.permissions(fn.home + "/.config/fish/config.fish")

        if not fn.path.isfile(fn.home + "/.config/fish/config.fish.bak"):
            fn.shutil.copy(fn.fish_arco, fn.home + "/.config/fish/config.fish")
            fn.permissions(fn.home + "/.config/fish/config.fish")

        print("Fish config reset")
        fn.show_in_app_notification(self, "Fish config reset")

    def on_remove_fish_all(self, widget):
        fn.remove_package_s("arcolinux-fish-git")
        fn.remove_package_s("fish")
        print("Fish is removed - remove the folder in ~/.config/fish manually")
        fn.show_in_app_notificatio(
            self, "Fish is removed - remove the folder in ~/.config/fish manually"
        )

    def tofish_apply(self, widget):
        fn.change_shell(self, "fish")

    # ====================================================================
    #                       FIXES
    # ====================================================================

    def on_click_install_arch_keyring(self, widget):
        pathway = base_dir + "/data/arch/packages/"
        file = fn.listdir(pathway)
        fn.install_local_package(self, pathway + str(file).strip("[]'"))

    def on_click_install_arch_keyring_online(self, widget):
        pathway = "/tmp/att-installation/"
        fn.mkdir(pathway)
        command = (
            "wget https://archlinux.org/packages/core/any/archlinux-keyring/download --content-disposition -P"
            + pathway
        )
        try:
            fn.subprocess.call(
                command,
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            print("Downloading the package")
            GLib.idle_add(fn.show_in_app_notification, self, "Downloading the package")
        except Exception as error:
            print(error)

        file = fn.listdir(pathway)
        fn.install_local_package(self, pathway + str(file).strip("[]'"))
        try:
            fn.shutil.rmtree(pathway)
        except Exception as error:
            print(error)

    def on_click_fix_pacman_keys(self, widget):
        fn.install_package(self, "alacritty")
        try:
            fn.subprocess.call(
                "alacritty --hold -e /usr/share/athena-tweak-tool/data/any/fix-pacman-databases-and-keys",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            print("Pacman has been reset (gpg, libraries,keys)")
            GLib.idle_add(fn.show_in_app_notification, self, "Pacman keys fixed")
        except Exception as error:
            print(error)

    def on_click_probe(self, widget):
        fn.install_package(self, "hw-probe")
        fn.install_package(self, "alacritty")
        try:
            fn.subprocess.call(
                "alacritty --hold -e /usr/share/athena-tweak-tool/data/arco/bin/arcolinux-probe",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            print("Probe link has been created")
            GLib.idle_add(
                fn.show_in_app_notification, self, "Probe link has been created"
            )
        except Exception as error:
            print(error)

    def on_click_fix_mainstream(self, widget):
        fn.install_package(self, "alacritty")
        try:
            command = "alacritty --hold -e /usr/share/athena-tweak-tool/data/any/set-mainstream-servers"
            fn.subprocess.call(
                command.split(" "),
                shell=False,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            print("Mainstream servers have been set")
            GLib.idle_add(
                fn.show_in_app_notification, self, "Mainstream servers have been saved"
            )
        except Exception as error:
            print(error)

    def on_click_reset_mirrorlist(self, widget):
        try:
            if fn.path.isfile(fn.mirrorlist + ".bak"):
                fn.shutil.copy(fn.mirrorlist + ".bak", fn.mirrorlist)
        except Exception as error:
            print(error)
        print("Your original mirrorlist is back")
        GLib.idle_add(
            fn.show_in_app_notification, self, "Your original mirrorlist is back"
        )

    def on_click_get_arch_mirrors(self, widget):
        fn.install_package(self, "alacritty")
        try:
            fn.install_package(self, "reflector")
            fn.subprocess.call(
                "alacritty --hold -e /usr/share/athena-tweak-tool/data/any/archlinux-get-mirrors-reflector",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            print("Fastest Arch Linux servers have been set using reflector")
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                "Fastest Arch Linux servers saved - reflector",
            )
        except:
            print("Install alacritty")

    def on_click_get_arch_mirrors2(self, widget):
        fn.install_package(self, "alacritty")
        try:
            fn.subprocess.call(
                "alacritty --hold -e /usr/share/athena-tweak-tool/data/any/archlinux-get-mirrors-rate-mirrors",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            print("Fastest Arch Linux servers have been set using rate-mirrors")
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                "Fastest Arch Linux servers saved - rate-mirrors",
            )
        except Exception as error:
            print(error)

    def on_click_fix_sddm_conf(self, widget):
        fn.install_package(self, "alacritty")
        try:
            command = "alacritty --hold -e /usr/share/athena-tweak-tool/data/arco/bin/arcolinux-fix-sddm-config"
            fn.subprocess.call(
                command,
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            print("We use the default setup from plasma")
            print("Two files:")
            print(" - /etc/sddm.conf")
            print(" - /etc/sddm.d.conf/kde_settings.conf")
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                "Saved the original SDDM configuration",
            )
        except:
            print("Install alacritty")

    def on_click_fix_pacman_conf(self, widget):
        try:
            command = "alacritty --hold -e /usr/local/bin/arcolinux-fix-pacman-conf"
            fn.subprocess.call(
                command,
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            print("Saved the original /etc/pacman.conf")
            GLib.idle_add(
                fn.show_in_app_notification, self, "Saved the original /etc/pacman.conf"
            )
        except Exception as error:
            print(error)

    def on_click_fix_pacman_gpg_conf(self, widget):
        if not fn.path.isfile(fn.gpg_conf + ".bak"):
            fn.shutil.copy(fn.gpg_conf, fn.gpg_conf + ".bak")
        fn.shutil.copy(fn.gpg_conf_original, fn.gpg_conf)
        print("The new /etc/pacman.d/gnupg/gpg.conf has been saved")
        print("We only add servers to the config")
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "The new /etc/pacman.d/gnupg/gpg.conf has been saved",
        )

    def on_click_fix_pacman_gpg_conf_local(self, widget):
        if not fn.path.isdir(fn.home + "/.gnupg"):
            try:
                fn.makedirs(fn.home + "/.gnupg", 0o766)
                fn.permissions(fn.home + "/.gnupg")
            except Exception as error:
                print(error)

        if not fn.path.isfile(fn.gpg_conf_local + ".bak"):
            try:
                fn.shutil.copy(fn.gpg_conf_local, fn.gpg_conf_local + ".bak")
                fn.permissions(fn.gpg_conf_local + ".bak")
            except Exception as error:
                print(error)

        fn.shutil.copy(fn.gpg_conf_local_original, fn.gpg_conf_local)
        fn.permissions(fn.gpg_conf_local)
        print("The new ~/.gnupg/gpg.conf has been saved")
        print("We only add servers to the config")
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "The new ~/.gnupg/gpg.conf has been saved",
        )

    def on_click_install_arch_mirrors(self, widget):
        fn.install_package(self, "reflector")
        self.btn_run_reflector.set_sensitive(True)

    def on_click_install_arch_mirrors2(self, widget):
        fn.install_package(self, "rate-mirrors")
        self.btn_run_rate_mirrors.set_sensitive(True)

    def on_click_apply_global_cursor(self, widget):
        cursor = self.cursor_themes.get_active_text()
        fixes.set_global_cursor(self, cursor)
        print("Cursor is saved in /usr/share/icons/default")
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "Cursor saved in /usr/share/icons/default",
        )

    def on_click_remove_all_variety_packages(self, widget):
        try:
            fn.install_package(self, "alacritty")
            fn.subprocess.call(
                "alacritty --hold -e /usr/share/athena-tweak-tool/data/arco/bin/arcolinux-remove-variety",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            print("Removing variety and any related packages")
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                "Removing variety and any related packages",
            )
        except:
            print("Install alacritty")

    def on_click_remove_all_conky_packages(self, widget):
        try:
            fn.install_package(self, "alacritty")
            fn.subprocess.call(
                "alacritty --hold -e /usr/share/athena-tweak-tool/data/arco/bin/arcolinux-remove-conky",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            print("Removing conky and any related packages")
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                "Removing conky and any related packages",
            )
        except:
            print("Install alacritty")

    def on_click_remove_all_kernels_but_linux(self, widget):
        try:
            fn.install_package(self, "alacritty")
            fn.subprocess.call(
                "alacritty --hold -e /usr/share/athena-tweak-tool/data/arco/bin/arcolinux-remove-all-kernels-but-linux",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            print("Removing kernel(s) and any related packages")
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                "Removing kernel(s) and any related packages",
            )
        except:
            print("Install alacritty")

    def on_click_remove_all_kernels_but_linux_cachyos(self, widget):
        try:
            fn.install_package(self, "alacritty")
            fn.subprocess.call(
                "alacritty --hold -e /usr/share/athena-tweak-tool/data/arco/bin/arcolinux-remove-all-kernels-but-linux-cachyos",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            print("Removing kernel(s) and any related packages")
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                "Removing kernel(s) and any related packages",
            )
        except:
            print("Install alacritty")

    def on_click_remove_all_kernels_but_linux_lts(self, widget):
        try:
            fn.install_package(self, "alacritty")
            fn.subprocess.call(
                "alacritty --hold -e /usr/share/athena-tweak-tool/data/arco/bin/arcolinux-remove-all-kernels-but-linux-lts",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            print("Removing kernel(s) and any related packages")
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                "Removing kernel(s) and any related packages",
            )
        except:
            print("Install alacritty")

    def on_click_remove_all_kernels_but_linux_zen(self, widget):
        try:
            fn.install_package(self, "alacritty")
            fn.subprocess.call(
                "alacritty --hold -e /usr/share/athena-tweak-tool/data/arco/bin/arcolinux-remove-all-kernels-but-linux-zen",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            print("Removing kernel(s) and any related packages")
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                "Removing kernel(s) and any related packages",
            )
        except:
            print("Install alacritty")

    def on_click_change_debug(self, widget):
        try:
            fn.install_package(self, "alacritty")
            fn.subprocess.call(
                "alacritty --hold -e /usr/share/athena-tweak-tool/data/arco/bin/remove-debug",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            print("Changing debug into !debug in /etc/makepkg.conf")
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                "Changing debug into !debug in /etc/makepkg.conf",
            )
        except:
            print("Install alacritty")

    def on_mirror_seed_repo_toggle(self, widget, active):
        if not pmf.mirror_exist(
            "Server = https://ant.seedhost.eu/arcolinux/$repo/$arch"
        ):
            pmf.append_mirror(self, fn.seedhostmirror)
        else:
            if self.opened is False:
                pmf.toggle_mirrorlist(self, widget.get_active(), "arco_mirror_seed")

    def on_mirror_gitlab_repo_toggle(self, widget, active):
        if not pmf.mirror_exist(
            "Server = https://gitlab.com/arcolinux/$repo/-/raw/main/$arch"
        ):
            pmf.append_mirror(self, fn.seedhostmirror)
        else:
            if self.opened is False:
                pmf.toggle_mirrorlist(self, widget.get_active(), "arco_mirror_gitlab")

    def on_mirror_belnet_repo_toggle(self, widget, active):
        if not pmf.mirror_exist(
            "Server = https://ant.seedhost.eu/arcolinux/$repo/$arch"
        ):
            pmf.append_mirror(self, fn.seedhostmirror)
        else:
            if self.opened is False:
                pmf.toggle_mirrorlist(self, widget.get_active(), "arco_mirror_belnet")

    def on_mirror_funami_repo_toggle(self, widget, active):
        if not pmf.mirror_exist(
            "Server = https://mirror.funami.tech/arcolinux/$repo/$arch"
        ):
            pmf.append_mirror(self, fn.seedhostmirror)
        else:
            if self.opened is False:
                pmf.toggle_mirrorlist(self, widget.get_active(), "arco_mirror_funami")

    def on_mirror_jingk_repo_toggle(self, widget, active):
        if not pmf.mirror_exist(
            "Server = https://mirror.jingk.ai/arcolinux/$repo/$arch"
        ):
            pmf.append_mirror(self, fn.seedhostmirror)
        else:
            if self.opened is False:
                pmf.toggle_mirrorlist(self, widget.get_active(), "arco_mirror_jingk")

    def on_mirror_accum_repo_toggle(self, widget, active):
        if not pmf.mirror_exist(
            "Server = https://mirror.accum.se/mirror/arcolinux.info/$repo/$arch"
        ):
            pmf.append_mirror(self, fn.seedhostmirror)
        else:
            if self.opened is False:
                pmf.toggle_mirrorlist(self, widget.get_active(), "arco_mirror_accum")

    def on_mirror_aarnet_repo_toggle(self, widget, active):
        if not pmf.mirror_exist(
            "Server = https://mirror.aarnet.edu.au/pub/arcolinux/$repo/$arch"
        ):
            pmf.append_mirror(self, fn.aarnetmirror)
        else:
            if self.opened is False:
                pmf.toggle_mirrorlist(self, widget.get_active(), "arco_mirror_aarnet")

    # def on_mirror_github_repo_toggle(self, widget, active):
    #     if not pmf.mirror_exist("Server = https://ant.seedhost.eu/arcolinux/$repo/$arch"):
    #         pmf.append_mirror(self, fn.seedhostmirror)
    #     else:
    #         if self.opened is False:
    #             pmf.toggle_mirrorlist(self, widget.get_active(),
    #                                   "arco_mirror_github")

    # =====================================================
    #               PACMAN CONF
    # =====================================================

    def on_update_pacman_databases_clicked(self, Widget):
        fn.update_repos(self)
        print("sudo pacman -Sy")
        print("All the selected pacman databases are up-to-date")
        fn.show_in_app_notification(
            self, "All the selected pacman databases are up-to-date"
        )

    def on_athena_clicked(self, widget):
        fn.install_athena(self)
        print("Athena keyring and mirrors added")
        print("Restart Att and select the repos")
        GLib.idle_add(
            fn.show_in_app_notification, self, "Athena keyring and mirrors added"
        )
        fn.update_repos(self)

    def on_athena_toggle(self, widget, active):
        if not pmf.repo_exist("[athena]"):
            pmf.append_repo(self, fn.athena_repo)
            print("Repo has been added to /etc/pacman.conf")
            fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(), "athena")

    def on_arcolinux_clicked(self, widget):
        fn.install_arcolinux(self)
        print("ArcoLinux keyring and mirrors added")
        fn.show_in_app_notification(
            self, "ArcoLinux keyring and mirrors added + activated"
        )
        self.on_pacman_atestrepo_toggle(self.atestrepo_button, False)
        self.on_pacman_arepo_toggle(self.arepo_button, True)
        self.on_pacman_a3p_toggle(self.a3prepo_button, True)
        self.on_pacman_axl_toggle(self.axlrepo_button, True)
        fn.update_repos(self)
        # fn.restart_program()

    def on_pacman_atestrepo_toggle(self, widget, active):
        if not pmf.repo_exist("[arcolinux_repo_testing]"):
            pmf.append_repo(self, fn.atestrepo)
            print("Repo has been added to /etc/pacman.conf")
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                "Repo has been added to /etc/pacman.conf",
            )
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(), "arco_testing")

    def on_pacman_arepo_toggle(self, widget, active):
        if not pmf.repo_exist("[arcolinux_repo]"):
            pmf.append_repo(self, fn.arepo)
            print("Repo has been added to /etc/pacman.conf")
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                "Repo has been added to /etc/pacman.conf",
            )
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(), "arco_base")
                if fn.check_arco_repos_active() is True:
                    self.button_install_design.set_sensitive(True)
                    self.button_install_desktop.set_sensitive(True)
                    self.button_reinstall_design.set_sensitive(True)
                    self.button_reinstall_desktop.set_sensitive(True)
                    self.install_arco_vimix.set_sensitive(True)
                else:
                    self.button_install_design.set_sensitive(False)
                    self.button_install_desktop.set_sensitive(False)
                    self.button_reinstall_design.set_sensitive(False)
                    self.button_reinstall_desktop.set_sensitive(False)
                    self.install_arco_vimix.set_sensitive(False)
        utilities.set_util_state_arco_switch(self)

    def on_pacman_a3p_toggle(self, widget, active):
        if not pmf.repo_exist("[arcolinux_repo_3party]"):
            pmf.append_repo(self, fn.a3drepo)
            print("Repo has been added to /etc/pacman.conf")
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                "Repo has been added to /etc/pacman.conf",
            )
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(), "arco_a3p")
                if fn.check_arco_repos_active() is True:
                    self.button_install_design.set_sensitive(True)
                    self.button_install_desktop.set_sensitive(True)
                    self.button_reinstall_design.set_sensitive(True)
                    self.button_reinstall_desktop.set_sensitive(True)
                else:
                    self.button_install_design.set_sensitive(False)
                    self.button_install_desktop.set_sensitive(False)
                    self.button_reinstall_design.set_sensitive(False)
                    self.button_reinstall_desktop.set_sensitive(False)

    def on_pacman_axl_toggle(self, widget, active):
        if not pmf.repo_exist("[arcolinux_repo_xlarge]"):
            pmf.append_repo(self, fn.axlrepo)
            print("Repo has been added to /etc/pacman.conf")
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                "Repo has been added to /etc/pacman.conf",
            )
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(), "arco_axl")

    def on_reborn_clicked(self, widget):
        fn.install_reborn(self)
        print("Reborn keyring and mirrors added")
        print("Restart Att and select the repos")
        GLib.idle_add(
            fn.show_in_app_notification, self, "Reborn keyring and mirrors added"
        )
        fn.update_repos(self)

    def on_reborn_toggle(self, widget, active):
        if not pmf.repo_exist("[Reborn-OS]"):
            pmf.append_repo(self, fn.reborn_repo)
            print("Repo has been added to /etc/pacman.conf")
            fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(), "reborn")

    def on_blackarch_clicked(self, widget):
        fn.install_blackarch(self)
        print("BlackArch keyring and mirrors added")
        print("Restart Att and select the repos")
        GLib.idle_add(
            fn.show_in_app_notification, self, "BlackArch keyring and mirrors added"
        )
        fn.update_repos(self)

    def on_blackarch_toggle(self, widget, active):
        if not pmf.repo_exist("[blackarch]"):
            pmf.append_repo(self, fn.blackarch_repo)
            print("Repo has been added to /etc/pacman.conf")
            fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(), "blackarch")

    def on_garuda_clicked(self, widget):
        fn.install_chaotics(self)
        print("Chaotics keyring and mirrors added")
        print("Restart Att and select the repos")
        GLib.idle_add(
            fn.show_in_app_notification, self, "Chaotics keyring and mirrors added"
        )
        fn.update_repos(self)

    def on_garuda_toggle(self, widget, active):
        if not pmf.repo_exist("[garuda]"):
            pmf.append_repo(self, fn.garuda_repo)
            print("Repo has been added to /etc/pacman.conf")
            fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(), "garuda")

    def on_chaotics_clicked(self, widget):
        fn.install_chaotics(self)
        print("Chaotics keyring and mirrors added")
        print("Restart Att and select the repos")
        GLib.idle_add(
            fn.show_in_app_notification, self, "Chaotics keyring and mirrors added"
        )
        fn.update_repos(self)

    def on_chaotics_toggle(self, widget, active):
        if not pmf.repo_exist("[chaotic-aur]"):
            pmf.append_repo(self, fn.chaotics_repo)
            print("Repo has been added to /etc/pacman.conf")
            fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(), "chaotics")

    def on_endeavouros_clicked(self, widget):
        fn.install_endeavouros(self)
        print("EndeavourOS keyring and mirrors added")
        print("Restart Att and select the repo")
        fn.show_in_app_notification(self, "Restart Att and select the repo")
        fn.update_repos(self)

    def on_endeavouros_toggle(self, widget, active):
        if not pmf.repo_exist("[endeavouros]"):
            pmf.append_repo(self, fn.endeavouros_repo)
            print("Repo has been added to /etc/pacman.conf")
            fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(), "endeavouros")

    def on_nemesis_toggle(self, widget, active):
        if not pmf.repo_exist("[nemesis_repo]"):
            pmf.append_repo(self, fn.nemesis_repo)
            print("Repo has been added to /etc/pacman.conf")
            fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(), "nemesis")
        fn.update_repos(self)

    # def on_xerolinux_clicked(self, widget):
    #     fn.install_xerolinux(self)
    #     print("XeroLinux mirrors added")
    #     print("Restart Att and select the repos")
    #     fn.show_in_app_notification(self, "Xerolinux mirrors added")
    #     fn.update_repos(self)

    # def on_xero_toggle(self, widget, active):
    #     if not pmf.repo_exist("[xerolinux_repo]"):
    #         pmf.append_repo(self, fn.xero_repo)
    #         print("Repo has been added to /etc/pacman.conf")
    #         fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
    #     else:
    #         if self.opened is False:
    #             pmf.toggle_test_repos(self, widget.get_active(), "xero")

    # def on_xero_xl_toggle(self, widget, active):
    #     if not pmf.repo_exist("[xerolinux_repo_xl]"):
    #         pmf.append_repo(self, fn.xero_xl_repo)
    #         print("Repo has been added to /etc/pacman.conf")
    #         fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
    #     else:
    #         if self.opened is False:
    #             pmf.toggle_test_repos(self, widget.get_active(), "xero_xl")

    # def on_xero_nv_toggle(self, widget, active):
    #     if not pmf.repo_exist("[xerolinux_nvidia_repo]"):
    #         pmf.append_repo(self, fn.xero_nv_repo)
    #         print("Repo has been added to /etc/pacman.conf")
    #         fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
    #     else:
    #         if self.opened is False:
    #             pmf.toggle_test_repos(self, widget.get_active(), "xero_nv")

    def on_pacman_toggle1(self, widget, active):
        if not pmf.repo_exist("[core-testing]"):
            pmf.append_repo(self, fn.arch_testing_repo)
            print("Repo has been added to /etc/pacman.conf")
            fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(), "testing")

    def on_pacman_toggle2(self, widget, active):
        if not pmf.repo_exist("[core]"):
            pmf.append_repo(self, fn.arch_core_repo)
            print("Repo has been added to /etc/pacman.conf")
            fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(), "core")

    def on_pacman_toggle3(self, widget, active):
        if not pmf.repo_exist("[extra]"):
            pmf.append_repo(self, fn.arch_extra_repo)
            print("Repo has been added to /etc/pacman.conf")
            fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(), "extra")

    def on_pacman_toggle4(self, widget, active):
        if not pmf.repo_exist("[extra-testing]"):
            pmf.append_repo(self, fn.arch_community_testing_repo)
            print("Repo has been added to /etc/pacman.conf")
            fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(), "extra-testing")

    def on_pacman_toggle5(self, widget, active):
        if not pmf.repo_exist("[extra-testing]"):
            pmf.append_repo(self, fn.arch_extra_testing_repo)
            print("Repo has been added to /etc/pacman.conf")
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                "Repo has been added to /etc/pacman.conf",
            )
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(), "community")

    def on_pacman_toggle6(self, widget, active):
        if not pmf.repo_exist("[multilib-testing]"):
            pmf.append_repo(self, fn.arch_multilib_testing_repo)
            print("Repo has been added to /etc/pacman.conf")
            fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(), "multilib-testing")

    # def on_pacman_toggle7(self, widget, active):
    #     if not pmf.repo_exist("[Reborn-OS]"):
    #         pmf.append_repo(self, fn.reborn_repo)
    #         print("Repo has been added to /etc/pacman.conf")
    #         fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
    #     else:
    #         if self.opened is False:
    #             pmf.toggle_test_repos(self, widget.get_active(), "Reborn-OS")

    def on_pacman_toggle7(self, widget, active):
        if not pmf.repo_exist("[multilib]"):
            pmf.append_repo(self, fn.arch_multilib_repo)
            print("Repo has been added to /etc/pacman.conf")
            fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(), "multilib")

    def custom_repo_clicked(self, widget):
        custom_repo_text = self.textview_custom_repo.get_buffer()
        startiter, enditer = custom_repo_text.get_bounds()

        if not len(custom_repo_text.get_text(startiter, enditer, True)) < 5:
            print(custom_repo_text.get_text(startiter, enditer, True))
            pmf.append_repo(self, custom_repo_text.get_text(startiter, enditer, True))
        try:
            fn.update_repos(self)
        except Exception as error:
            print(error)
            print("Is the code correct? - check /etc/pacman.conf")

    def blank_pacman(source, target):
        fn.shutil.copy(fn.pacman, fn.pacman + ".bak")
        if fn.distr == "arch":
            fn.shutil.copy(fn.blank_pacman_arch, fn.pacman)
        if fn.distr == "arcolinux":
            fn.shutil.copy(fn.blank_pacman_arco, fn.pacman)
        if fn.distr == "endeavouros":
            fn.shutil.copy(fn.blank_pacman_eos, fn.pacman)
        if fn.distr == "garuda":
            fn.shutil.copy(fn.blank_pacman_garuda, fn.pacman)
        print("We have now a blank pacman /etc/pacman.conf depending on the distro")
        print("ATT will reboot automatically")
        print(
            "Now add the repositories in the order you would like them to appear in the /etc/pacman.conf"
        )
        fn.restart_program()

    def reset_pacman_local(self, widget):
        if fn.path.isfile(fn.pacman + ".bak"):
            fn.shutil.copy(fn.pacman + ".bak", fn.pacman)
            print("We have used /etc/pacman.conf.bak to reset /etc/pacman.conf")
            fn.show_in_app_notification(
                self, "Default Settings Applied - check in a terminal"
            )

    def reset_pacman_online(self, widget):
        if fn.distr == "arch":
            fn.shutil.copy(fn.pacman_arch, fn.pacman)
        if fn.distr == "arcolinux":
            fn.shutil.copy(fn.pacman_arco, fn.pacman)
        if fn.distr == "endeavouros":
            fn.shutil.copy(fn.pacman_eos, fn.pacman)
        if fn.distr == "garuda":
            fn.shutil.copy(fn.pacman_garuda, fn.pacman)
        print("The online version of /etc/pacman.conf is saved")
        fn.show_in_app_notification(
            self, "Default Settings Applied - check in a terminal"
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

    # =====================================================

    def on_launch_adt_clicked(self, desktop):
        # check if package is installed and update label
        if self.adt_installed is True:
            fn.remove_package(self, "arcolinux-desktop-trasher-git")
            if fn.check_package_installed("arcolinux-desktop-trasher-git") is False:
                self.button_adt.set_label("Install the ArcoLinux Desktop Trasher")
                self.adt_installed = False

        else:
            fn.install_package(self, "arcolinux-desktop-trasher-git")
            if fn.check_package_installed("arcolinux-desktop-trasher-git") is True:
                self.button_adt.set_label("Remove the ArcoLinux Desktop Trasher")
                self.adt_installed = True
        # try:
        #    subprocess.Popen("/usr/local/bin/arcolinux-desktop-trasher")
        #    fn.show_in_app_notification(self, "ArcoLinux Desktop Trasher launched")
        #    print("We started ADT")
        # except:
        #    pass

    def on_click_apply_parallel_downloads(self, widget):
        fixes.set_parallel_downloads(self, widget)

    # ====================================================================
    #                       SERVICES - NSSWITCH
    # ====================================================================

    def on_install_discovery_clicked(self, widget):
        fn.install_discovery(self)
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "Network discovery is installed - a good nsswitch_config is needed",
        )
        print("Network discovery is installed")

    def on_remove_discovery_clicked(self, widget):
        fn.remove_discovery(self)
        GLib.idle_add(fn.show_in_app_notification, self, "Network discovery is removed")
        print("Network discovery is removed")

    def on_click_reset_nsswitch(self, widget):
        if fn.path.isfile(fn.nsswitch_config + ".bak"):
            fn.shutil.copy(fn.nsswitch_config + ".bak", fn.nsswitch_config)

        print("/etc/nsswitch.config reset")
        fn.show_in_app_notification(self, "Nsswitch config reset")

    def on_click_apply_nsswitch(self, widget):
        services.choose_nsswitch(self)

    # ====================================================================
    #                       SERVICES - SAMBA
    # ====================================================================

    def on_click_create_samba_user(self, widget):
        services.create_samba_user(self)

    # def on_click_delete_user(self, widget):
    #     services.delete_user(self)

    def on_click_restart_smb(self, widget):
        services.restart_smb(self)

    def on_click_save_samba_share(self, widget):
        fn.save_samba_config(self)

    def on_click_install_arco_thunar_plugin(self, widget):
        if fn.path.isfile(fn.arcolinux_mirrorlist):
            if fn.check_arco_repos_active() is True:
                fn.install_arco_thunar_plugin(self, widget)
            else:
                print("First activate the ArcoLinux repos")
                fn.show_in_app_notification(self, "First activate the ArcoLinux repos")
        else:
            print("Install the ArcoLinux keys and mirrors")
            fn.show_in_app_notification(self, "Install the ArcoLinux keys and mirrors")

    def on_click_install_arco_caja_plugin(self, widget):
        if fn.path.isfile(fn.arcolinux_mirrorlist):
            if fn.check_arco_repos_active() is True:
                fn.install_arco_caja_plugin(self, widget)
            else:
                print("First activate the ArcoLinux repos")
                fn.show_in_app_notification(self, "First activate the ArcoLinux repos")
        else:
            print("Install the ArcoLinux keys and mirrors")
            fn.show_in_app_notification(self, "Install the ArcoLinux keys and mirrors")

    def on_click_install_arco_nemo_plugin(self, widget):
        if fn.path.isfile(fn.arcolinux_mirrorlist):
            if fn.check_arco_repos_active() is True:
                fn.install_arco_nemo_plugin(self, widget)
            else:
                print("First activate the ArcoLinux repos")
                fn.show_in_app_notification(self, "First activate the ArcoLinux repos")
        else:
            print("Install the ArcoLinux keys and mirrors")
            fn.show_in_app_notification(self, "Install the ArcoLinux keys and mirrors")

    def on_click_apply_samba(self, widget):
        services.choose_smb_conf(self)
        print("Applying selected samba configuration")
        fn.show_in_app_notification(self, "Applying selected samba configuration")

    def on_click_reset_samba(self, widget):
        if fn.path.isfile(fn.samba_config + ".bak"):
            fn.shutil.copy(fn.samba_config + ".bak", fn.samba_config)
            print("We have reset your /etc/samba/smb.conf")
            fn.show_in_app_notification(self, "Original smb.conf is applied")
        if not fn.path.isfile(fn.samba_config + ".bak"):
            print("We have no original /etc/samba/smb.conf.bak file - we can not reset")
            print("Instead choose one from the dropdown")
            fn.show_in_app_notification(self, "No backup configuration present")

    def on_click_install_samba(self, widget):
        fn.install_samba(self)
        print("Samba has been successfully installed")
        fn.show_in_app_notification(self, "Samba has been successfully installed")

    def on_click_uninstall_samba(self, widget):
        fn.uninstall_samba(self)
        print("Samba has been successfully uninstalled")
        fn.show_in_app_notification(self, "Samba has been successfully uninstalled")

    # ====================================================================
    #                       SERVICES - AUDIO
    # ====================================================================

    def on_click_switch_to_pulseaudio(self, widget):
        print("Installing pulseaudio")

        # if fn.distr == "manjaro":
        #     fn.remove_package_dd(self, "manjaro-pulse")

        if fn.check_package_installed("pipewire-pulse"):
            fn.remove_package_dd(self, "pipewire-pulse")
            fn.remove_package_dd(self, "wireplumber")

        try:
            fn.install_package(self, "pulseaudio")  # conflicts with pipewire-pulse
            fn.install_package(
                self, "pulseaudio-bluetooth"
            )  # conflicts with pipewire-pulse
            fn.install_package(self, "pulseaudio-alsa")

            fn.install_package(self, "pavucontrol")

            fn.install_package(self, "alsa-utils")
            fn.install_package(self, "alsa-plugins")
            fn.install_package(self, "alsa-lib")
            fn.install_package(self, "alsa-firmware")
            fn.install_package(self, "gstreamer")
            fn.install_package(self, "gst-plugins-good")
            fn.install_package(self, "gst-plugins-bad")
            fn.install_package(self, "gst-plugins-base")
            fn.install_package(self, "gst-plugins-ugly")

            # if blueberry_installed:
            #     fn.install_package(self, "blueberry")

            # add line for autoconnect
            services.add_autoconnect_pulseaudio(self)

        except Exception as error:
            print(error)

    def on_click_switch_to_pipewire(self, widget):
        print("Installing pipewire")
        blueberry_installed = False

        try:
            if fn.check_package_installed("pulseaudio"):
                fn.remove_package_dd(self, "pulseaudio")
                fn.remove_package_dd(self, "pulseaudio-bluetooth")

            fn.install_package(self, "pipewire")
            fn.install_package(
                self, "pipewire-pulse"
            )  # contains wireplumber - conflicts with pulseaudio and pulseaudio-bluetooth
            fn.install_package(self, "pipewire-alsa")
            # fn.install_package(self, "pipewire-jack")
            # fn.install_package(self, "pipewire-zeroconf")

            fn.install_package(self, "pavucontrol")

            fn.install_package(self, "alsa-utils")
            fn.install_package(self, "alsa-plugins")
            fn.install_package(self, "alsa-lib")
            fn.install_package(self, "alsa-firmware")
            fn.install_package(self, "gstreamer")
            fn.install_package(self, "gst-plugins-good")
            fn.install_package(self, "gst-plugins-bad")
            fn.install_package(self, "gst-plugins-base")
            fn.install_package(self, "gst-plugins-ugly")

            if blueberry_installed:
                fn.install_package(self, "blueberry")

            if fn.check_package_installed("pipewire-media-session"):
                fn.remove_package_dd(self, "pipewire-media-session")
                fn.install_package(self, "pipewire-pulse")
                fn.install_package(self, "wireplumber")

        except Exception as error:
            print(error)

    # ====================================================================
    #                       SERVICES - BLUETOOTH
    # ====================================================================
    # applications
    def on_click_install_bluetooth(self, widget):
        print("Installing bluetooth")
        fn.install_package(self, "bluez")
        fn.install_package(self, "bluez-utils")
        if fn.check_package_installed("bluez"):
            self.enable_bt.set_sensitive(True)
            self.disable_bt.set_sensitive(True)
            self.restart_bt.set_sensitive(True)

    def on_click_remove_bluetooth(self, widget):
        print("Removing bluez")
        fn.remove_package_dd(self, "bluez")
        fn.remove_package_dd(self, "bluez-utils")
        if not fn.check_package_installed("bluez"):
            self.enable_bt.set_sensitive(False)
            self.disable_bt.set_sensitive(False)
            self.restart_bt.set_sensitive(False)

    # def on_click_install_gnome_bt(self, widget):
    #     print("Installing gnome-bluetooth")
    #     fn.install_package(self, "gnome-bluetooth")

    # def on_click_remove_gnome_bt(self, widget):
    #     print("Removing gnome-bluetooth")
    #     fn.remove_package_dd(self, "gnome-bluetooth")

    def on_click_install_blueberry(self, widget):
        print("Installing blueberry")
        fn.install_package(self, "blueberry")

    def on_click_remove_blueberry(self, widget):
        print("Removing blueberry")
        fn.remove_package(self, "blueberry")

    def on_click_install_blueman(self, widget):
        print("Installing blueman")
        fn.install_package(self, "blueman")

    def on_click_remove_blueman(self, widget):
        print("Removing blueman")
        fn.remove_package(self, "blueman")

    def on_click_install_bluedevil(self, widget):
        print("Installing bluedevil")
        fn.install_package(self, "bluedevil")

    def on_click_remove_bluedevil(self, widget):
        print("Removing bluedevil")
        fn.remove_package_s(self, "bluedevil")

    # service
    def on_click_enable_bluetooth(self, widget):
        print("Enabling bluetooth service/socket")
        fn.enable_service("bluetooth")
        fn.show_in_app_notification(self, "Bluetooth has been enabled")

    def on_click_disable_bluetooth(self, widget):
        print("Enabling bluetooth service/socket")
        fn.disable_service("bluetooth")
        fn.show_in_app_notification(self, "Bluetooth has been disabled")

    def on_click_restart_bluetooth(self, widget):
        print("Restart bluetooth")
        fn.restart_service("bluetooth")
        fn.show_in_app_notification(self, "Bluetooth has been restarted")

    # ====================================================================
    #                       SERVICES - CUPS
    # ====================================================================

    def on_click_install_cups(self, widget):
        print("Installing cups")
        fn.install_package(self, "cups")

    def on_click_remove_cups(self, widget):
        print("Removing cups")
        fn.remove_package(self, "cups")

    def on_click_install_cups_pdf(self, widget):
        print("Installing cups-pdf")
        fn.install_package(self, "cups-pdf")

    def on_click_remove_cups_pdf(self, widget):
        print("Removing cups-pdf")
        fn.remove_package(self, "cups-pdf")

    def on_click_enable_cups(self, widget):
        print("Enabling cups service/socket")
        fn.enable_service("cups")

    def on_click_disable_cups(self, widget):
        print("Enabling cups service/socket")
        fn.disable_service("cups")

    def on_click_restart_cups(self, widget):
        print("Restart cups")
        fn.restart_service("cups")

    def on_click_install_printer_drivers(self, widget):
        print("Following printer drivers have been installed")
        fn.install_package(self, "foomatic-db-engine")
        fn.install_package(self, "foomatic-db")
        fn.install_package(self, "foomatic-db-ppds")
        fn.install_package(self, "foomatic-db-nonfree")
        fn.install_package(self, "foomatic-db-nonfree-ppds")
        fn.install_package(self, "gutenprint")
        fn.install_package(self, "foomatic-db-gutenprint-ppds")
        fn.install_package(self, "ghostscript")
        fn.install_package(self, "gsfonts")

    def on_click_remove_printer_drivers(self, widget):
        print("Following printer drivers have been removed")
        fn.remove_package(self, "foomatic-db-engine")
        fn.remove_package(self, "foomatic-db")
        fn.remove_package(self, "foomatic-db-ppds")
        fn.remove_package(self, "foomatic-db-nonfree")
        fn.remove_package(self, "foomatic-db-nonfree-ppds")
        fn.remove_package(self, "gutenprint")
        fn.remove_package(self, "foomatic-db-gutenprint-ppds")
        fn.remove_package(self, "ghostscript")
        fn.remove_package(self, "gsfonts")

    def on_click_install_hplip(self, widget):
        print("Installing Hplip")
        fn.install_package(self, "hplip")

    def on_click_remove_hplip(self, widget):
        print("Removing Hplip")
        fn.remove_package(self, "hplip")

    def on_click_install_system_config_printer(self, widget):
        print("Installing system_config_printer")
        fn.install_package(self, "system-config-printer")

    def on_click_remove_system_config_printer(self, widget):
        print("Removing system_config_printer")
        fn.remove_package(self, "system_config_printer")

    # TODO : how to launch an app as the user
    # def on_click_launch_system_config_printer(self, desktop):
    #     if fn.check_package_installed("system-config-printer"):
    #         try:
    #             subprocess.Popen("/usr/bin/system-config-printer")
    #             GLib.idle_add(
    #                 fn.show_in_app_notification,
    #                 self,
    #                 "System config printer launched",
    #             )
    #             print("We started system-config-printer")
    #         except:
    #             pass
    #     else:
    #         print("First install system-config-printer package")
    #         fn.show_in_app_notification(self, "First install system-config-printer")

    # ====================================================================
    #                       SHELLS EXTRA
    # ====================================================================

    def on_extra_shell_applications_clicked(self, widget):
        if self.expac.get_active():
            fn.install_package(self, "expac")
        if self.ripgrep.get_active():
            fn.install_package(self, "ripgrep")
        if self.yay.get_active():
            fn.install_arco_package(self, "yay-bin")
        if self.paru.get_active():
            fn.install_arco_package(self, "paru-bin")
        if self.bat.get_active():
            fn.install_package(self, "bat")
        if self.downgrade.get_active():
            fn.install_arco_package(self, "downgrade")
        if self.hw_probe.get_active():
            fn.install_arco_package(self, "hw-probe")
        if self.rate_mirrors.get_active():
            fn.install_arco_package(self, "rate-mirrors-bin")
        if self.most.get_active():
            fn.install_package(self, "most")
        print("Software has been installed depending on the repos")
        fn.show_in_app_notification(
            self, "Software has been installed depending on the repos"
        )
        if fn.check_package_installed("expac") is False:
            self.expac.set_active(False)
        if fn.check_package_installed("ripgrep") is False:
            self.ripgrep.set_active(False)
        if fn.check_package_installed("yay-bin") is False:
            self.yay.set_active(False)
        if fn.check_package_installed("paru-bin") is False:
            self.paru.set_active(False)
        if fn.check_package_installed("bat") is False:
            self.bat.set_active(False)
        if fn.check_package_installed("downgrade") is False:
            self.downgrade.set_active(False)
        if fn.check_package_installed("hw-probe") is False:
            self.hw_probe.set_active(False)
        if fn.check_package_installed("rate-mirrors-bin") is False:
            self.rate_mirrors.set_active(False)
        if fn.check_package_installed("most") is False:
            self.most.set_active(False)

    def on_select_all_toggle(self, widget, active):
        if self.select_all.get_active():
            self.expac.set_active(True)
            self.ripgrep.set_active(True)
            self.yay.set_active(True)
            self.paru.set_active(True)
            self.bat.set_active(True)
            self.downgrade.set_active(True)
            self.hw_probe.set_active(True)
            self.rate_mirrors.set_active(True)
            self.most.set_active(True)

    # ====================================================================
    #                       TERMINALS
    # ====================================================================

    def on_clicked_install_alacritty(self, widget):
        fn.install_package(self, "alacritty")

    def on_clicked_install_alacritty_themes(self, widget):
        if fn.check_arco_repos_active() is True:
            fn.install_package(self, "alacritty")
            fn.install_package(self, "ttf-hack")
            fn.install_arco_package(self, "alacritty-themes")
            fn.install_arco_package(self, "base16-alacritty-git")
            print("Alacritty themes installed")
            fn.show_in_app_notification(self, "Alacritty themes installed")

            # if there is no file copy/paste from /etc/skel else alacritty-themes crash
            if not fn.path.isfile(fn.alacritty_config):
                if not fn.path.isdir(fn.alacritty_config_dir):
                    try:
                        fn.mkdir(fn.alacritty_config_dir)
                        fn.permissions(fn.alacritty_config_dir)
                    except Exception as error:
                        print(error)

                fn.shutil.copy(fn.alacritty_arco, fn.alacritty_config)
                fn.permissions(fn.home + "/.config/alacritty")
                print("Alacritty config saved")
        else:
            print("First activate the ArcoLinux repos")
            fn.show_in_app_notification(self, "First activate the ArcoLinux repos")

    def on_clicked_remove_alacritty_themes(self, widget):
        fn.remove_package(self, "alacritty")
        fn.remove_package(self, "ttf-hack")
        fn.remove_package(self, "alacritty-themes")
        fn.remove_package(self, "base16-alacritty-git")
        print("Alacritty themes removed")
        fn.show_in_app_notification(self, "Alacritty themes removed")

    def on_clicked_install_xfce4_terminal(self, widget):
        fn.install_package(self, "xfce4-terminal")

    def on_clicked_remove_xfce4_terminal(self, widget):
        fn.remove_package(self, "xfce4-terminal")

    def on_clicked_install_xfce4_themes(self, widget):
        if fn.check_arco_repos_active() is True:
            fn.install_arco_package(self, "xfce4-terminal-base16-colors-git")
            fn.install_arco_package(self, "tempus-themes-xfce4-terminal-git")
            fn.install_arco_package(self, "prot16-xfce4-terminal")
            print("Xfce4 themes installed")
            fn.show_in_app_notification(self, "Xfce4 themes installed")
        else:
            print("First activate the ArcoLinux repos")
            fn.show_in_app_notification(self, "First activate the ArcoLinux repos")

    def on_clicked_remove_xfce4_themes(self, widget):
        fn.remove_package(self, "xfce4-terminal-base16-colors-git")
        fn.remove_package(self, "tempus-themes-xfce4-terminal-git")
        fn.remove_package(self, "prot16-xfce4-terminal")
        print("Xfce4 themes removed")
        fn.show_in_app_notification(self, "Xfce4 themes removed")

    def on_clicked_reset_xfce4_terminal(self, widget):
        if fn.path.isfile(fn.xfce4_terminal_config + ".bak"):
            fn.shutil.copy(fn.xfce4_terminal_config + ".bak", fn.xfce4_terminal_config)
            fn.permissions(fn.home + "/.config/xfce4/terminal")
            print("xfce4-terminal reset")
            fn.show_in_app_notification(self, "Xfce4-terminal reset")

    def on_clicked_reset_alacritty(self, widget):
        if fn.path.isfile(fn.alacritty_config + ".bak"):
            fn.shutil.copy(fn.alacritty_config + ".bak", fn.alacritty_config)
            fn.permissions(fn.home + "/.config/alacritty")
            print("Alacritty reset")
            fn.show_in_app_notification(self, "Alacritty reset")

    def on_clicked_set_arcolinux_alacritty_theme_config(self, widget):
        if fn.path.isfile(fn.alacritty_config):
            fn.shutil.copy(fn.alacritty_arco, fn.alacritty_config)
            fn.permissions(fn.home + "/.config/alacritty")
            print("Applied the ATT Alacritty theme/config")
            fn.show_in_app_notification(self, "Applied the ATT Alacritty theme/config")

    # ====================================================================
    #                      TERMITE
    # ====================================================================

    def on_clicked_install_termite(self, widget):
        fn.install_arco_package(self, "termite")
        terminals.get_themes(self.term_themes)

    def on_clicked_remove_termite(self, widget):
        fn.remove_package(self, "termite")
        terminals.get_themes(self.term_themes)

    def on_clicked_install_termite_themes(self, widget):
        if fn.check_arco_repos_active() is True:
            fn.install_arco_package(self, "termite")
            fn.install_arco_package(self, "arcolinux-termite-themes-git")
            fn.copy_func("/etc/skel/.config/termite", fn.home + "/.config/", True)
            fn.permissions(fn.home + "/.config/termite")
            terminals.get_themes(self.term_themes)
            print("Termite  themes installed")
            fn.show_in_app_notification(self, "Termite themes installed")
        else:
            print("First activate the ArcoLinux repos")
            fn.show_in_app_notification(self, "First activate the ArcoLinux repos")

    def on_clicked_remove_termite_themes(self, widget):
        fn.remove_package(self, "arcolinux-termite-themes-git")
        terminals.get_themes(self.term_themes)
        print("Termite  themes removed")
        GLib.idle_add(fn.show_in_app_notification, self, "Termite themes removed")

    def on_term_apply(self, widget):
        if self.term_themes.get_active_text() is not None:
            widget.set_sensitive(False)
            terminals.set_config(self, self.term_themes.get_active_text())
            widget.set_sensitive(True)

    def on_term_reset(self, widget):
        if fn.path.isfile(fn.termite_config + ".bak"):
            fn.shutil.copy(fn.termite_config + ".bak", fn.termite_config)
            fn.show_in_app_notification(self, "Default Settings Applied")
            if fn.path.isfile(fn.config):
                settings.write_settings("TERMITE", "theme", "")
                terminals.get_themes(self.term_themes)

    # ====================================================================
    #                      ZSH THEMES
    # ====================================================================

    def on_clicked_install_only_zsh(self, widget):
        fn.install_package(self, "zsh")
        fn.restart_program()

    def on_install_zsh_completions_clicked(self, widget):
        fn.install_package(self, "zsh-completions")

    def on_remove_zsh_completions_clicked(self, widget):
        fn.remove_package(self, "zsh-completions")

    def on_install_zsh_syntax_highlighting_clicked(self, widget):
        fn.install_package(self, "zsh-syntax-highlighting")

    def on_remove_zsh_syntax_highlighting_clicked(self, widget):
        fn.remove_package(self, "zsh-syntax-highlighting")

    def on_arcolinux_zshrc_clicked(self, widget):
        try:
            if fn.path.isfile(fn.zshrc_arco):
                fn.shutil.copy(fn.zshrc_arco, fn.zsh_config)
                fn.permissions(fn.home + "/.zshrc")
            fn.source_shell(self)
        except Exception as error:
            print(error)

        print("ATT ~/.zshrc is applied")
        GLib.idle_add(fn.show_in_app_notification, self, "ATT ~/.zshrc is applied")

    def on_zshrc_reset_clicked(self, widget):
        try:
            if fn.path.isfile(fn.zsh_config + ".bak"):
                fn.shutil.copy(fn.zsh_config + ".bak", fn.zsh_config)
                fn.permissions(fn.home + "/.zshrc")
        except Exception as error:
            print(error)

        print("Your personal ~/.zshrc is applied again - logout")
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "Your personal ~/.zshrc is applied again - logout",
        )

    def on_zsh_apply_theme(self, widget):
        # create a .zshrc if it doesn't exist'
        if not fn.path.isfile(fn.zsh_config):
            fn.shutil.copy(fn.zshrc_arco, fn.zsh_config)
            fn.permissions(fn.home + "/.zshrc")

        if self.zsh_themes.get_active_text() is not None:
            # widget.set_sensitive(False)
            zsh_theme.set_config(self, self.zsh_themes.get_active_text())
            widget.set_sensitive(True)
            print("Applying zsh theme")

    def on_zsh_reset(self, widget):
        if fn.path.isfile(fn.zsh_config + ".bak"):
            fn.shutil.copy(fn.zsh_config + ".bak", fn.zsh_config)
            fn.permissions(fn.home + "/.zshrc")
            fn.permissions(fn.home + "/.zshrc.bak")
            fn.show_in_app_notification(self, "Default settings applied")
            print("Backup has been applied")
        else:
            fn.shutil.copy(
                "/usr/share/athena-tweak-tool/data/arco/.zshrc", fn.home + "/.zshrc"
            )
            fn.permissions(fn.home + "/.zshrc")
            fn.show_in_app_notification(self, "Valid ~/.zshrc applied")
            print("Valid ~/.zshrc applied")

    def tozsh_apply(self, widget):
        fn.change_shell(self, "zsh")

    def install_oh_my_zsh(self, widget):
        fn.install_arco_package(self, "oh-my-zsh-git")
        self.termset.set_sensitive(True)
        self.zsh_themes.set_sensitive(True)
        zsh_theme.get_themes(self.zsh_themes)

    # The intent behind this function is to be a centralised image changer for all portions of ATT that need it
    # Currently utilising an if tree - this is not best practice: it should be a match: case tree.
    # But I have not yet got that working.
    def update_image(
        self, widget, image, theme_type, att_base, image_width, image_height
    ):
        sample_path = ""
        preview_path = ""
        random_option = False
        # THIS CODE IS KEPT ON PURPOSE. DO NOT DELETE.
        # Once Python 3.10 is released and used widely, delete the if statements below the match blocks
        # and use the match instead. It is faster, and easier to maintain.
        #    match "zsh":
        #        case 'zsh':
        #            sample_path = att_base+"/images/zsh-sample.jpg"
        #            preview_path = att_base+"/images/zsh_previews/"+widget.get_active_text() + ".jpg"
        #        case 'qtile':
        #            sample_path = att_base+"/images/zsh-sample.jpg"
        #            previe_path = att_base+"/images/zsh_previews/"+widget.get_active_text() + ".jpg"
        #        case 'i3':
        #            sample_path = att_base+"/images/i3-sample.jpg"
        #            preview_path = att_base+"/themer_data/i3/"+widget.get_active_text() + ".jpg"
        #        case 'awesome':
        #            sample_path = att_base+"/images/i3-sample.jpg"
        #            preview_path = att_base+"/themer_data/awesomewm/"+widget.get_active_text() + ".jpg"
        #        case 'neofetch':
        #            sample_path = att_base + widget.get_active_text()
        #            preview_path = att_base + widget.get_active_text()
        #        case unknown_command:
        #            print("Function update_image passed an incorrect value for theme_type. Value passed was: " + theme_type)
        #            print("Remember that the order for using this function is: self, widget, image, theme_type, att_base_path, image_width, image_height.")
        if theme_type == "zsh":
            sample_path = att_base + "/images/zsh-sample.jpg"
            preview_path = (
                att_base + "/images/zsh_previews/" + widget.get_active_text() + ".jpg"
            )
            if widget.get_active_text() == "random":
                random_option = True
        elif theme_type == "qtile":
            sample_path = att_base + "/images/qtile-sample.jpg"
            preview_path = (
                att_base + "/themer_data/qtile/" + widget.get_active_text() + ".jpg"
            )
        elif theme_type == "leftwm":
            sample_path = att_base + "/images/leftwm-sample.jpg"
            preview_path = (
                att_base + "/themer_data/leftwm/" + widget.get_active_text() + ".jpg"
            )
        elif theme_type == "i3":
            sample_path = att_base + "/images/i3-sample.jpg"
            preview_path = (
                att_base + "/themer_data/i3/" + widget.get_active_text() + ".jpg"
            )
        elif theme_type == "awesome":
            # Awesome section doesn't use a ComboBoxText, but a ComboBox - which has different properties.
            tree_iter = self.awesome_combo.get_active_iter()
            if tree_iter is not None:
                model = self.awesome_combo.get_model()
                row_id, name = model[tree_iter][:2]

            sample_path = att_base + "/images/awesome-sample.jpg"
            preview_path = att_base + "/themer_data/awesomewm/" + name + ".jpg"
        elif theme_type == "neofetch":
            sample_path = att_base + widget.get_active_text()
            preview_path = att_base + widget.get_active_text()
        else:
            # If we are doing our job correctly, this should never be shown to users. If it does, we have done something wrong as devs.
            print(
                "Function update_image passed an incorrect value for theme_type. Value passed was: "
                + theme_type
            )
            print(
                "Remember that the order for using this function is: self, widget, image, theme_type, att_base_path, image_width, image_height."
            )
        # source_pixbuf = image.get_pixbuf()
        if fn.path.isfile(preview_path) and not random_option:
            pixbuf = GdkPixbuf.Pixbuf().new_from_file_at_size(
                preview_path, image_width, image_height
            )
        else:
            pixbuf = GdkPixbuf.Pixbuf().new_from_file_at_size(
                sample_path, image_width, image_height
            )
        image.set_from_pixbuf(pixbuf)

    def remove_oh_my_zsh(self, widget):
        fn.remove_package(self, "oh-my-zsh-git")
        zsh_theme.get_themes(self.zsh_themes)
        self.termset.set_sensitive(False)
        self.zsh_themes.set_sensitive(False)

    # ====================================================================
    #                            PACKAGES
    # ====================================================================#

    def on_click_export_packages(
        self,
        widget,
        packages_obj,
        rb_export_all,
        rb_export_explicit,
        gui_parts,
    ):
        try:
            if not os.path.exists(packages_obj.export_dir):
                fn.makedirs(packages_obj.export_dir)
                fn.permissions(packages_obj.export_dir)
            if fn.check_pacman_lockfile() is True:
                fn.logger.warning(
                    "Export aborted, failed to lock database, pacman lockfile exists at %s"
                )

                fn.messagebox(
                    self,
                    "Export of packages failed",
                    "Failed to lock database, pacman lockfile exists at %s\nIs another pacman process running ?"
                    % fn.pacman_lockfile,
                )

            else:
                vbox_stack = gui_parts[0]
                grid_package_status = gui_parts[1]
                grid_package_count = gui_parts[2]
                vbox_pacmanlog = gui_parts[3]
                textbuffer = gui_parts[4]
                textview = gui_parts[5]
                label_package_status = gui_parts[6]
                label_package_count = gui_parts[7]

                if vbox_pacmanlog.is_visible() is False:
                    vbox_stack.pack_start(grid_package_status, False, False, 0)
                    vbox_stack.pack_start(grid_package_count, False, False, 0)
                    vbox_stack.pack_start(vbox_pacmanlog, False, False, 0)
                    vbox_stack.show_all()

                    grid_package_status.hide()
                    grid_package_count.hide()
                else:
                    grid_package_status.hide()
                    grid_package_count.hide()

                rb_export_selected = None
                if rb_export_all.get_active():
                    rb_export_selected = "export_all"
                if rb_export_explicit.get_active():
                    rb_export_selected = "export_explicit"
                export_ok = packages_obj.export_packages(rb_export_selected, gui_parts)
                if export_ok is False:
                    fn.messagebox(
                        self,
                        "Export failed",
                        "Failed to export list of packages",
                    )
                else:
                    fn.messagebox(
                        self,
                        "Export completed",
                        "Exported to file %s" % packages_obj.default_export_path,
                    )

        except Exception as e:
            fn.logger.error("Exception in on_click_export_packages(): %s" % e)

    def on_message_dialog_yes_response(self, widget):
        fn.logger.info("Ok to proceed to install")
        widget.destroy()

    def on_message_dialog_no_response(self, widget):
        fn.logger.info("Packages install skipped by user")
        widget.destroy()

    def on_click_install_packages(self, widget, packages_obj, gui_parts):
        try:
            if fn.check_pacman_lockfile() is True:
                fn.logger.warning(
                    "Install aborted, failed to lock database, pacman lockfile exists at %s"
                    % fn.pacman_lockfile
                )

                fn.messagebox(
                    self,
                    "Install aborted",
                    "Failed to lock database, pacman lockfile exists at %s\nIs another pacman process running ?"
                    % fn.pacman_lockfile,
                )
            else:
                packages = packages_obj.get_packages_file_content()

                if packages is not None:
                    packages_prompt_dialog = PackagesPromptGui(packages)

                    packages_prompt_dialog.show_all()
                    response = packages_prompt_dialog.run()
                    packages_prompt_dialog.destroy()

                    if response == Gtk.ResponseType.OK:
                        widget.set_sensitive(False)
                        fn.logger.info("Preparing installation")
                        vbox_stack = gui_parts[0]
                        grid_package_status = gui_parts[1]
                        grid_package_count = gui_parts[2]
                        vbox_pacmanlog = gui_parts[3]
                        # textbuffer = gui_parts[4]
                        # textview = gui_parts[5]
                        label_package_status = gui_parts[6]
                        label_package_count = gui_parts[7]

                        if vbox_pacmanlog.is_visible() is False:
                            vbox_stack.pack_start(grid_package_status, False, False, 0)
                            vbox_stack.pack_start(grid_package_count, False, False, 0)
                            vbox_stack.pack_start(vbox_pacmanlog, False, False, 0)
                            vbox_stack.show_all()
                        else:
                            grid_package_status.show()
                            grid_package_count.show()

                        packages_obj.install_packages(packages, widget, gui_parts)
                else:
                    fn.logger.error(
                        "Package list file %s not found"
                        % packages_obj.default_export_path
                    )
                    fn.messagebox(
                        self,
                        "Error package list file not found",
                        "Cannot find %s" % packages_obj.default_export_path,
                    )

        except Exception as e:
            fn.logger.error("Exception in on_click_install_packages(): %s" % e)
            widget.set_sensitive(True)

    # ====================================================================
    #                            BOTTOM BUTTONS
    # ====================================================================

    def on_refresh_att_clicked(self, desktop):
        fn.restart_program()

    def on_close(self, widget, data):
        fn.unlink("/tmp/att.lock")
        Gtk.main_quit()

    def on_reload_att_clicked(self, widget):
        # login
        if fn.check_package_installed("sddm"):
            sddm.pop_box(self, self.sessions_sddm)
        if fn.check_package_installed("lightdm"):
            lightdm.pop_box_sessions_lightdm(self, self.sessions_lightdm)
        # terminal
        if fn.check_package_installed("termite"):
            terminals.get_themes(self.term_themes)
        # themes
        if fn.check_package_installed("arcolinux-leftwm-git"):
            terminals.get_themes(self.term_themes)
        # populate all cursors dropdowns
        if fn.check_package_installed("sddm"):
            sddm.pop_gtk_cursor_names(self, self.sddm_cursor_themes)
        if fn.check_package_installed("lightdm"):
            lightdm.pop_gtk_cursor_names(self, self.cursor_themes_lightdm)
        fixes.pop_gtk_cursor_names(self.cursor_themes)
        # populate cursor themes - some themes include a cursor
        if fn.check_package_installed("sddm"):
            sddm.pop_gtk_cursor_names(self, self.sddm_cursor_themes)
        if fn.check_package_installed("lightdm"):
            lightdm.pop_gtk_cursor_names(self, self.cursor_themes_lightdm)
        fixes.pop_gtk_cursor_names(self.cursor_themes)
        # populate lightdm page
        if fn.check_package_installed("lightdm"):
            lightdm.pop_gtk_theme_names_lightdm(self, self.gtk_theme_names_lightdm)
        # populate lxdm page
        if fn.check_package_installed("lxdm"):
            lxdm.pop_gtk_theme_names_lxdm(self.lxdm_gtk_theme)
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
