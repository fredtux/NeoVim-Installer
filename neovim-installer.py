#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import exit
from getpass import getuser
from argparse import ArgumentParser
from os import system, listdir, path
from shutil import copy, copytree
from threading import Thread
from concurrent.futures.thread import ThreadPoolExecutor

def copytree2(src, dst, symlinks=False, ignore=None):
    for item in listdir(src):
        s = path.join(src, item)
        d = path.join(dst, item)
        if path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            copy(s, d)

def install():
    print("##### DOWNLOADING AND EXTRACTING NEOVIM #####")
    system("curl -LO https://github.com/neovim/neovim/releases/download/v0.5.1/nvim-macos.tar.gz")
    system("tar xzf nvim-macos.tar.gz")

    print("##### COPYING FILES #####")
    dSrc = "./nvim-osx64/"
    dDest = "/usr/local/"

    with ThreadPoolExecutor(max_workers = 5) as pool:
        pool.submit(copy, dSrc + "bin/nvim", dDest + "/bin/nvim")
       
        system("mkdir -p " + dDest + "/lib/nvim/parser")
        pool.submit(copy, dSrc + "lib/nvim/parser/c.so", dDest + "lib/nvim/parser/c.so")
    
        system("mkdir -p " + dDest + "/libs")
        pool.submit(copytree2, dSrc + "libs/", dDest + "libs/")

        pool.submit(copy, dSrc + "share/man/man1/nvim.1", dDest + "share/man/man1/nvim.1")

        pool.submit(copytree, dSrc + "share/nvim/runtime/", dDest + "share/nvim/runtime/")

    print("##### REMOVING TEMPORARY FILES #####")
    system("rm -f ./nvim-macos.tar.gz")
    system("rm -fr ./nvim-osx64")

def uninstall():
    dPath = "/usr/local/"
    system("rm -f " + dPath + "bin/nvim")
    print("rm -f " + dPath + "bin/nvim")
    system("rm -fr " + dPath + "lib/nvim")
    print("rm -fr " + dPath + "lib/nvim")
    system("rm -f " + dPath + "libs/libiconv.2.dylib")
    print("rm -f " + dPath + "libs/libiconv.2.dylib")
    system("rm -f " + dPath + "libs/libintl.8.dylib")
    print("rm -f " + dPath + "libs/libintl.8.dylib")
    system("rm -f " + dPath + "libs/libutil.dylib")
    print("rm -f " + dPath + "libs/libutil.dylib")
    system("rm -fr " + dPath + "share/nvim")
    print("rm -fr " + dPath + "share/nvim")
    system("rm -f " + dPath + "share/man/man1/nvim.1")
    print("rm -f " + dPath + "share/man/man1/nvim.1")

if __name__ == "__main__":
    parser = ArgumentParser(description="Installer/Uninstaller for NeoVim using MacOS")
    parser.add_argument("-i", "--install", help="Install NeoVim", action="store_true")
    parser.add_argument("-u", "--uninstall", help="Uninstall NeoVim", action="store_true")

    args = parser.parse_args()

    if getuser() != "root":
        print("You have to run the script as root (i.e.: using sudo)")
        exit(1)

    if args.install:
        install()
    elif args.uninstall:
        uninstall()
