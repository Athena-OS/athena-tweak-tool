# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================
# pylint:disable=C0103,C0116,C0411,C0413,I1101,R1705,W0621,W0611,W0622
import gi

# from yaml import DirectiveToken

#gi.require_version("Gtk", "3.0")

from os import rmdir, unlink, walk, execl, getpid, system, stat, readlink
from os import path, getlogin, mkdir, makedirs, listdir
from distro import id
import os
from gi.repository import GLib, Gtk
import sys
import threading
import shutil
import psutil
import datetime
import subprocess
import logging
import time
from queue import Queue
import pwd

# =====================================================
#              BEGIN DECLARATION OF VARIABLES
# =====================================================

distr = id()

sudo_username = getlogin()
home = "/home/" + str(sudo_username)

config = home + "/.config/athena-tweak-tool/settings.ini"
config_dir = home + "/.config/athena-tweak-tool/"
desktop = ""
icons_default = "/usr/share/icons/default/index.theme"

# dnf cache directory
dnf_cache_dir = "/var/cache/dnf/"

# logging setup
logger = logging.getLogger("logger")
# create console handler and set level to debug
ch = logging.StreamHandler()

logger.setLevel(logging.INFO)
ch.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter(
    "%(asctime)s:%(levelname)s > %(message)s", "%Y-%m-%d %H:%M:%S"
)
# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


# =====================================================
#              END DECLARATION OF VARIABLES
# =====================================================
# =====================================================
# =====================================================
# =====================================================
# =====================================================
#               BEGIN GLOBAL FUNCTIONS
# =====================================================


def get_lines(files):
    try:
        if path.isfile(files):
            with open(files, "r", encoding="utf-8") as f:
                lines = f.readlines()
                f.close()
            return lines
    except Exception as error:
        print(error)
    # get position in list


def get_position(lists, value):
    data = [string for string in lists if value in string]
    if len(data) != 0:
        position = lists.index(data[0])
        return position
    return 0


# get positions in list


def get_positions(lists, value):
    data = [string for string in lists if value in string]
    position = []
    for d in data:
        position.append(lists.index(d))
    return position


# get variable from list


def _get_variable(lists, value):
    data = [string for string in lists if value in string]

    if len(data) >= 1:
        data1 = [string for string in data if "#" in string]

        for i in data1:
            if i[:4].find("#") != -1:
                data.remove(i)
    if data:
        data_clean = [data[0].strip("\n").replace(" ", "")][0].split("=")
    return data_clean


# Check  value exists remove data


def check_value(list, value):
    data = [string for string in list if value in string]
    if len(data) >= 1:
        data1 = [string for string in data if "#" in string]
        for i in data1:
            if i[:4].find("#") != -1:
                data.remove(i)
    return data


# check backups


def check_backups(now):
    if not path.exists(home + "/" + bd + "/Backup-" + now.strftime("%Y-%m-%d %H")):
        makedirs(home + "/" + bd + "/Backup-" + now.strftime("%Y-%m-%d %H"), 0o777)
        permissions(home + "/" + bd + "/Backup-" + now.strftime("%Y-%m-%d %H"))


# check process is running


def check_if_process_is_running(processName):
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=["pid", "name", "create_time"])
            if processName == pinfo["name"]:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


# copytree


def copytree(self, src, dst, symlinks=False, ignore=None):  # noqa
    if not path.exists(dst):
        makedirs(dst)
    for item in listdir(src):
        s = path.join(src, item)
        d = path.join(dst, item)
        if path.exists(d):
            try:
                shutil.rmtree(d)
            except Exception as error:
                print(error)
                unlink(d)
        if path.isdir(s):
            try:
                shutil.copytree(s, d, symlinks, ignore)
            except Exception as error:
                print(error)
                print("ERROR2")
                self.ecode = 1
        else:
            try:
                shutil.copy2(s, d)
            except:  # noqa
                print("ERROR3")
                self.ecode = 1


# check if file exists


def file_check(file):
    if path.isfile(file):
        return True

    return False


# check if path exists


def path_check(path):
    if os.path.isdir(path):
        return True

    return False


# check if directory is empty


def is_empty_directory(path):
    if os.path.exists(path) and not os.path.isfile(path):
        if not os.listdir(path):
            # print("Empty directory")
            return True
        else:
            # print("Not empty directory")
            return False


# check if value is true or false in file


def check_content(value, file):
    try:
        with open(file, "r", encoding="utf-8") as myfile:
            lines = myfile.readlines()
            myfile.close()

        for line in lines:
            if value in line:
                if value in line:
                    return True
                else:
                    return False
        return False
    except:
        return False


# check if package is installed or not
def check_package_installed(package):  # noqa
    try:
        subprocess.check_output(
            "rpm -q " + package, shell=True, stderr=subprocess.STDOUT
        )
        # package is installed
        return True
    except subprocess.CalledProcessError:
        # package is not installed
        return False


# check if service is active


def check_service(service):  # noqa
    try:
        command = "systemctl is-active " + service + ".service"
        output = subprocess.run(
            command.split(" "),
            check=True,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        status = output.stdout.decode().strip()
        if status == "active":
            # print("Service is active")
            return True
        else:
            # print("Service is inactive")
            return False
    except Exception:
        return False


def check_socket(socket):  # noqa
    try:
        command = "systemctl is-active " + socket + ".socket"
        output = subprocess.run(
            command.split(" "),
            check=True,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        status = output.stdout.decode().strip()
        if status == "active":
            # print("Service is active")
            return True
        else:
            # print("Service is inactive")
            return False
    except Exception:
        return False


# list normal users


def list_users(filename):  # noqa
    try:
        data = []
        with open(filename, "r", encoding="utf-8") as f:
            for line in f.readlines():
                if "1001" in line.split(":")[2]:
                    data.append(line.split(":")[0])
                if "1002" in line.split(":")[2]:
                    data.append(line.split(":")[0])
                if "1003" in line.split(":")[2]:
                    data.append(line.split(":")[0])
                if "1004" in line.split(":")[2]:
                    data.append(line.split(":")[0])
                if "1005" in line.split(":")[2]:
                    data.append(line.split(":")[0])
            data.sort()
            return data
    except Exception as error:
        print(error)


# check if user is part of the group


def check_group(group):
    try:
        groups = subprocess.run(
            ["sh", "-c", "id " + sudo_username],
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        for x in groups.stdout.decode().split(" "):
            if group in x:
                return True
            else:
                return False
    except Exception as error:
        print(error)


def check_systemd_boot():
    if (
        path_check("/boot/loader") is True
        and file_check("/boot/loader/loader.conf") is True
    ):
        return True
    else:
        return False


def get_user_env_from_proc(user):
    try:
        # Grab a PID from a known session process
        pid = subprocess.check_output(["pgrep", "-u", user, "gnome-session"]).decode().splitlines()[0]
        environ_path = f"/proc/{pid}/environ"
        with open(environ_path, "rb") as f:
            env_vars = dict(
                line.decode().split("=", 1) for line in f.read().split(b"\0") if b"=" in line
            )
        return {
            "DISPLAY": env_vars.get("DISPLAY", ":0"),
            "XAUTHORITY": env_vars.get("XAUTHORITY", f"/home/{user}/.Xauthority"),
            "DBUS_SESSION_BUS_ADDRESS": env_vars.get("DBUS_SESSION_BUS_ADDRESS"),
            "XDG_CURRENT_DESKTOP": env_vars.get("XDG_CURRENT_DESKTOP"),
            "XDG_RUNTIME_DIR": env_vars.get("XDG_RUNTIME_DIR", f"/run/user/{os.getuid()}"),
        }
    except Exception as e:
        print("Failed to extract environment:", e)
        return None


def install_package(self, package, manager):
    if manager == "dnf":
        command = "dnf -y install " + package
    elif manager == "rpm-ostree":
        command = "rpm-ostree install " + package

    # if more than one package - checf fails and will install
    if check_package_installed(package):
        print(package + " is already installed - nothing to do")
        GLib.idle_add(
            show_in_app_notification,
            self,
            package + " is already installed - nothing to do",
        )
    else:
        try:
            print(command)
            result = subprocess.call(
                command.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            if result == 0:
                print(package + " is now installed")
                GLib.idle_add(show_in_app_notification, self, package + " is now installed")
            else:
                print(f"Failed to install {package}. Exit code: {result}")
                GLib.idle_add(
                    show_in_app_notification,
                    self,
                    f"Failed to install {package}. Exit code: {result}",
                )
        except Exception as error:
            print(error)


def clear_skel_directory(path="/etc/skel"):
    # Ensure the provided path is indeed /etc/skel or a user-defined path
    if not os.path.exists(path):
        print(f"The directory {path} does not exist.")
        return

    # Iterate over all the items in the directory
    for item in os.listdir(path):
        item_path = os.path.join(path, item)

        # Check if the item is a file or a directory and remove it
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)  # Remove the file or symlink
                print(f"Removed file: {item_path}")
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)  # Remove the directory and its content
                print(f"Removed directory: {item_path}")
        except Exception as e:
            print(f"Failed to remove {item_path}. Reason: {e}")


def remove_file(file_path):
    if os.path.exists(file_path):
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)
                return f"File '{file_path}' has been removed successfully."
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
                return f"Directory '{file_path}' has been removed successfully."
        except OSError as e:
            return f"Error removing '{file_path}': {e.strerror}"
    else:
        return f"'{file_path}' does not exist."


def remove_package(self, package, manager):
    if manager == "dnf":
        command = "dnf remove -y " + package
    elif manager == "rpm-ostree":
        command = "rpm-ostree uninstall " + package

    if check_package_installed(package):
        print(command)
        try:
            result = subprocess.call(
                command.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            if result == 0:
                print(package + " is now removed")
                GLib.idle_add(show_in_app_notification, self, package + " is now removed")
            else:
                print(f"Failed to remove {package}. Exit code: {result}")
                GLib.idle_add(
                    show_in_app_notification,
                    self,
                    f"Failed to remove {package}. Exit code: {result}",
                )
        except Exception as error:
            print(error)
    else:
        print(package + " is already removed")
        GLib.idle_add(show_in_app_notification, self, package + " is already removed")


def enable_login_manager(self, loginmanager):
    if check_package_installed(loginmanager):
        try:
            command = "systemctl enable " + loginmanager + ".service -f"
            print(command)
            subprocess.call(
                command.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            print(loginmanager + " has been enabled - reboot")
            GLib.idle_add(
                show_in_app_notification,
                self,
                loginmanager + " has been enabled - reboot",
            )
        except Exception as error:
            print(error)
    else:
        print(loginmanager + " is not installed")
        GLib.idle_add(
            show_in_app_notification, self, loginmanager + " is not installed"
        )


def add_autologin_group(self):
    com = subprocess.run(
        ["sh", "-c", "su - " + sudo_username + " -c groups"],
        check=True,
        shell=False,
        stdout=subprocess.PIPE,
    )
    groups = com.stdout.decode().strip().split(" ")
    # print(groups)
    if "autologin" not in groups:
        command = "groupadd autologin"
        try:
            subprocess.call(
                command.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
        except Exception as error:
            print(error)
        try:
            subprocess.run(
                ["gpasswd", "-a", sudo_username, "autologin"], check=True, shell=False
            )
        except Exception as error:
            print(error)


# =====================================================
#              CHANGE SHELL
# =====================================================


def change_shell(self, shell):
    command = "sudo chsh " + sudo_username + " -s /bin/" + shell
    subprocess.call(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    print("Shell changed to " + shell + " for the user - logout")
    GLib.idle_add(
        show_in_app_notification,
        self,
        "Shell changed to " + shell + " for user - logout",
    )


# =====================================================
#               CONVERT COLOR
# =====================================================


def rgb_to_hex(rgb):
    if "rgb" in rgb:
        rgb = rgb.replace("rgb(", "").replace(")", "")
        vals = rgb.split(",")
        return "#{0:02x}{1:02x}{2:02x}".format(
            clamp(int(vals[0])), clamp(int(vals[1])), clamp(int(vals[2]))
        )
    return rgb


def clamp(x):
    return max(0, min(x, 255))


# =====================================================
#               COPY FUNCTION
# =====================================================


def copy_func(src, dst, isdir=False):
    if isdir:
        subprocess.run(["cp", "-Rp", src, dst], check=True, shell=False)
    else:
        subprocess.run(["cp", "-p", src, dst], check=True, shell=False)



# =====================================================
#               MESSAGEBOX
# =====================================================


def messagebox(self, title, message):
    md2 = Gtk.MessageDialog(
        parent=self,
        flags=0,
        message_type=Gtk.MessageType.INFO,
        buttons=Gtk.ButtonsType.OK,
        text=title,
    )
    md2.format_secondary_markup(message)
    md2.run()
    md2.destroy()


# =====================================================
#               NOTIFICATIONS
# =====================================================


def show_in_app_notification(self, message):
    if self.timeout_id is not None:
        GLib.source_remove(self.timeout_id)
        self.timeout_id = None

    self.notification_label.set_markup(
        '<span foreground="white">' + message + "</span>"
    )
    self.notification_revealer.set_reveal_child(True)
    self.timeout_id = GLib.timeout_add(3000, timeOut, self)


def timeOut(self):
    close_in_app_notification(self)


def close_in_app_notification(self):
    self.notification_revealer.set_reveal_child(False)
    GLib.source_remove(self.timeout_id)
    self.timeout_id = None


def do_pulse(data, prog):
    prog.pulse()
    return True


# =====================================================
#               PERMISSIONS
# =====================================================


def test(dst):
    for root, dirs, filesr in walk(dst):
        # print(root)
        for folder in dirs:
            pass
            # print(dst + "/" + folder)
            for file in filesr:
                pass
                # print(dst + "/" + folder + "/" + file)
        for file in filesr:
            pass
            # print(dst + "/" + file)


def permissions(dst):
    try:
        groups = subprocess.run(
            ["sh", "-c", "id " + sudo_username],
            check=True,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        group = None
        for x in groups.stdout.decode().split(" "):
            if "gid" in x.lower():  # match gid and GID
                try:
                    g = x.split("(")[1]
                    group = g.replace(")", "").strip()
                    break
                except IndexError:
                    raise ValueError("Unexpected format in 'id' command output.")

        # Ensure the group is retrieved
        if not group:
            raise ValueError(f"Could not determine group for user {sudo_username}.")

        subprocess.call(["chown", "-R", sudo_username + ":" + group, dst], shell=False)
    except Exception as error:
        print(error)

def findgroup():
    try:
        groups = subprocess.run(
            ["sh", "-c", "id " + sudo_username],
            check=True,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        group = None
        for x in groups.stdout.decode().split(" "):
            if "gid" in x.lower():  # match gid and GID
                try:
                    g = x.split("(")[1]
                    group = g.replace(")", "").strip()
                    break
                except IndexError:
                    raise ValueError("Unexpected format in 'id' command output.")

        # Ensure the group is retrieved
        if not group:
            raise ValueError(f"Could not determine group for user {sudo_username}.")
        print("[INFO] : Group = " + group)

    except Exception as error:
        print(error)


# =====================================================
#               RESTART PROGRAM
# =====================================================


def restart_program():
    if path.exists("/tmp/att.lock"):
        unlink("/tmp/att.lock")
        python = sys.executable
        execl(python, python, *sys.argv)


# =====================================================
#               SERVICES - GENERAL FUNCTIONS CUPS
# =====================================================


def enable_service(service):
    try:
        command = "systemctl enable " + service + ".service -f --now"
        subprocess.call(
            command.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print("We enabled the following service : " + service)
    except Exception as error:
        print(error)


def restart_service(service):
    try:
        command = "systemctl reload-or-restart " + service + ".service"
        subprocess.call(
            command.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print("We restarted the following service (if avalable) : " + service)
    except Exception as error:
        print(error)


def disable_service(service):
    try:
        command = "systemctl stop " + service
        subprocess.call(
            command.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        command = "systemctl disable " + service
        subprocess.call(
            command.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print("We stopped and disabled the following service " + service)
    except Exception as error:
        print(error)


def find_active_audio():
    output = subprocess.run(["pactl", "info"], check=True, stdout=subprocess.PIPE)

    pipewire_active = check_value(output, "pipewire")

    if pipewire_active == True:
        return pipewire_active
    else:
        return pipewire_active


def run_as_user(script):
    subprocess.call(["su - " + sudo_username + " -c " + script], shell=False)


# def install_extra_shell(package):
#     install = "pacman -S " + package + " --needed --noconfirm"
#     print(install)
#     try:
#         subprocess.call(
#             install.split(" "),
#             shell=False,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.STDOUT,
#         )
#     except Exception as error:
#         print(error)


# =====================================================
# 
# =====================================================

# update textview with pacman progress
def update_progress_textview(self, line):
    try:
        if len(line) > 0:
            self.textbuffer.insert(
                self.textbuffer.get_end_iter(),
                " %s" % line,
                len(" %s" % line),
            )

    except Exception as e:
        logger.error("Exception in update_progress_textview(): %s" % e)
    finally:
        self.messages_queue.task_done()
        text_mark_end = self.textbuffer.create_mark(
            "end", self.textbuffer.get_end_iter(), False
        )
        # scroll to the end of the textview
        self.textview.scroll_mark_onscreen(text_mark_end)


# update the package install status label called from outside the main thread
def update_package_status_label(label, text):
    label.set_markup(text)


# keep track of messages added to the queue, and updates the textview in almost realtime
def monitor_messages_queue(self):
    try:
        while True:
            message = self.messages_queue.get()
            GLib.idle_add(
                update_progress_textview,
                self,
                message,
                priority=GLib.PRIORITY_DEFAULT,
            )
    except Exception as e:
        logger.error("Exception in monitor_messages_queue(): %s" % e)
