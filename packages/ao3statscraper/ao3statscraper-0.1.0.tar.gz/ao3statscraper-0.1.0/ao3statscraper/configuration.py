#!/usr/bin/env python3


import os
import platform
import yaml
import pathlib
from getpass import getpass

from .utils import clear_terminal
from .pw import get_credentials, read_secrets, store_secrets


class PlottingConfig(object):
    """
    Configuration for the plotting script.
    """

    def __init__(self):
        self.prettify = True
        return


class Config(object):
    store_login = None
    username = "Your AO3 Username"
    password = "Don't type your password in plain text"

    ao3dir = None
    datadir = None
    conffile = None
    pklfile = None

    plotting = None

    def __init__(self, reset_conffile=False):
        """
        Initialize configuration.
        If `reset_conffile` is True, then write a new config file from scratch
        and exit.
        """

        # TODO: storing stuff in .ao3statscraper is probably not the way to go on windows

        # Get config directory
        userdir = pathlib.Path.home()
        ao3dir = os.path.join(userdir, ".ao3statscraper")
        self.ao3dir = ao3dir

        # Make sure it exists.
        try:
            os.mkdir(ao3dir)
        except FileExistsError:
            pass

        self.plotting = PlottingConfig()

        # Set full paths for config files.
        conffilename = "ao3statscraper.conf.yml"
        conffile = os.path.join(ao3dir, conffilename)
        self.conffile = conffile
        pklfilename = "ao3statscraper.conf.pkl"
        pklfile = os.path.join(ao3dir, pklfilename)
        self.pklfile = pklfile

        if not os.path.exists(conffile):
            clear_terminal()
            input(
                "Didn't find a configuration file. We need to set one up. Hit any key to coninue.\n"
            )
            self.setup_config_file()
        else:
            if reset_conffile:
                self.setup_config_file()
                quit()

        # get contents of config file.
        self._read_config_file()

        # Make sure everything is set.
        self._check_config()

        return

    def _check_config(self):
        """
        Check that no attributes are None. Mainly intended as a dev tool to make
        sure everything's intialized properly.
        """

        d = self.__dir__()

        for key in d:
            if key.startswith("__"):
                continue
            if getattr(self, key) is None:
                raise ValueError(f"Attribute {key} not initialized.")
        return

    def set_credentials(self, username, password):
        """
        Store username and password.
        """

        self.username = username
        self.password = password

        return

    def setup_config_file(self):
        """
        Set up permanent configuration and dump them in the configure file.
        """

        clear_terminal()
        print("Welcome to the configuration setup for the AO3 Stat Scraper.")
        print(
            f"After this setup, a configuration file will be written in `{self.conffile}`"
        )
        print("You can freely modify it on your own without calling this dialogue.")
        print(
            "Select a directory to store downloaded statistics. Hit Enter to use default."
        )
        datadir = input(f"(default: '{self.ao3dir}')\n")

        clear_terminal()
        print("Optionally, you can store your AO3 login on your local machine.")
        print("Your username and password will be encrypted and locked with a ")
        print("master password that you'll be asked to set next.")
        print("(If you forget the master password, you'll need to re-run this")
        print("configuration dialogue. You can do that by running `ao3get -c`)")
        store_login_str = "b"
        a = 0
        while not store_login_str.startswith(("n", "N", "y", "Y")):
            if a > 0:
                print("Invalid input.")
            store_login_str = input(
                "Do you want to store your AO3 login on your local machine? [y/n]\n"
            )
            a += 1
            if a > 10:
                print("Too many attempts. Exiting.")
                quit()

        store_login = True
        if store_login_str.startswith(("n", "N")):
            store_login = False

        if store_login:
            # Grab master password.
            clear_terminal()
            master_pwd = getpass(
                "Enter a master password (not your AO3 login password):\n"
            )
            clear_terminal()
            master_pwd2 = getpass("Enter the password again:\n")

            if master_pwd != master_pwd2:
                print("Error: Passwords do not match.")
                quit()

            # Grab AO3 credentials.
            username, password = get_credentials()
            # And store them.
            self.set_credentials(username, password)
            store_secrets(master_pwd, username, password, self.pklfile)

        if datadir == "":
            datadir = self.ao3dir

        try:
            os.mkdir(datadir)
        except FileExistsError:
            pass

        # Store the config
        self.datadir = datadir
        self.store_login = store_login

        # Now write the config file.
        confdict = {}
        global_conf = {
            "data_directory": self.datadir,
            "store_login": self.store_login,
        }

        confdict = {
            "Globals": global_conf,
        }

        ymlfp = open(self.conffile, "w")
        yaml.dump(confdict, ymlfp)
        ymlfp.close()

        return

    def _read_config_file(self):
        ymlfp = open(self.conffile, "r")
        confdata = yaml.load(ymlfp, Loader=yaml.Loader)
        ymlfp.close()

        try:
            self.datadir = confdata["Globals"]["data_directory"]
            self.store_login = confdata["Globals"]["store_login"]
        except KeyError:
            print("ERROR: Some fields are missing from your config file.")
            print("It might be out of date.")
            print("Re-generate it using `ao3get -c`")
            quit(1)

        return

    def prep_scrape(self):
        """
        Ensure everything is set for a scrape.
        """

        if self.store_login:
            master_pwd = getpass(
                "Enter master password (not your AO3 login password):\n"
            )
            username, password = read_secrets(master_pwd, self.pklfile, retry=True)
        else:
            username, password = get_credentials()

        self.set_credentials(username, password)

        return
