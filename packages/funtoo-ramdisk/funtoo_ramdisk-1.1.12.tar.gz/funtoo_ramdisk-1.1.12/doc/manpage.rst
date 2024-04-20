=========
 ramdisk
=========

--------------------------------------------------
create a bootable initial ramdisk
--------------------------------------------------

:Author: Daniel Robbins <drobbins@funtoo.org>
:Copyright: Copyright 2023 Daniel Robbins, Funtoo Solutions, Inc.
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0.
:Version: 1.1.12
:Manual section: 8
:Manual group: Funtoo Linux

SYNOPSIS
========

  ``ramdisk`` [build] [*OPTION...*] ``initramfs_outfile``

  ``ramdisk`` list kernels

  ``ramdisk`` list plugins

DESCRIPTION
===========

The Funtoo ramdisk tool, called ``ramdisk`` is a stand-alone tool to create an
initial RAM disk filesystem (initramfs) for booting your Linux system.

The internal initramfs logic is based on the logic found in Gentoo Linux's
genkernel tool, but has been rewritten to be simpler and more efficient.

You can use this tool to create an initramfs to boot to a Funtoo Linux root
ext4 or XFS filesystem, which is what we support in our official installation
documentation at https://www.funtoo.org/Install.

CAPABILITIES
============

* genkernel-style initramfs without the cruft. In comparison to genkernel's
  initramfs, the shell code is about 10x simpler and a lot cleaner and has
  been modernized. About 100 lines of shell script, with another 215 lines
  of functions in a support file.

* Copies over the modules you specify -- and automatically figures out any
  kernel module dependencies, so any depended-upon modules are also copied.
  This eliminates the need to track these dependencies manually.

* Rootless operation. You do not need enhanced privileges to create the
  initramfs.

* You can read the ``linuxrc`` script and actually understand what it does.
  It is written to be easy to understand and adapt. So it's not just short,
  but easy to grasp.

* Enhanced module loading engine on the initramfs which is significantly
  faster than genkernel. This effectively eliminates the "watching the
  stream of useless modules being loaded" issue with genkernel. Modern
  systems with NVMe drives will load just a handful of modules to boot
  -- all without requiring any special action from the user.

* "kpop" functionality allows for building ramdisks with just the modules
  you need. For example, ``ramdisk --kpop=nvme,ext4`` will create a
  ramdisk that can boot on NVMe ext4 root filesystems, and only include
  these necessary modules, leaving all other modules to be loaded by
  your Funtoo Linux system.

* Effective Python-based command to actually build the ramdisk, which is
  called: ``ramdisk``. This gives us an extensible platform for the future.

* Enhanced ini-style system for selecting modules to include on your initramfs.

* Enhanced ini-style system for selecting module groups to autoload on the
  initramfs.

* Support for xz and zstd compression.

ACTIONS
=======

The default action is ``build``, and can be optionally specified, which will
instruct ``ramdisk`` to build an initramfs. Available actions:

build
-----
Create an initramfs. See **OPTIONS** below for all options supported. The ``build``
action requires a destination initramfs path. This will be the literal path and
filename for the output initramfs. Use ``--force`` to overwrite any existing file.

list
----
List various things -- currently supported targets are ``kernels`` and ``plugins``.
``kernels`` will show you a list of available installed kernels on your system for
which you can build a ramdisk, and ``plugins`` will show the available boot-time
plugins that can be enabled to add more functionality to your ramdisk.

OPTIONS
=======

--debug                 Enable debug output.
--backtrace             Display full python backtrace/traceback instead of just a
                        short error summary.
--force                 Overwrite target initramfs if it exists.
--keep                  Keep the temporary directory after execution for investigation/debugging.
--version               Show this program's version number and exit.
--help                  Show this help message and exit.
--fs_foot=<path>        This defaults to ``/``, and specifies the filesystem root to look at
                        for finding both kernel sources (in ``/usr/src``) and kernel modules
                        (in ``/lib/modules``). This option also applies to ``ramdisk list
                        kernels``.
--kernel=<kernel>       Specify what kernel to build a ramdisk for. Use
                        ``ramdisk list kernels`` to display available options. The
                        default setting is to use the current value of the
                        ``/usr/src/linux`` symlink at the filesystem root to determine
                        which kernel to build a ramdisk for.
--compression=<method>  Compression method to use. Default is ``xz``. Also supported: ``zstd``.
--temp_root=<path>      Where to create temporary files. Defaults to ``/var/tmp``.
--plugins=<plugins>     A comma-delimited list of plugins to enable. The ``core`` plugin is
                        always enabled. Type ``ramdisk list plugins`` to see a list of available
                        plugins.
--kmod_config=<cfg>     ``ramdisk`` supports different sets of kernel module configurations, which
                        define what kernel modules get copied to the initramfs, and which ones
                        get auto-loaded by the initramfs at boot. Default value: ``full``. This
                        is currently the only option unless overridden by ``--kpop`` (see below.)
--kpop=<mods>           A comma-delimited list of kernel module names that you are sure, if loaded,
                        will allow your root block device and filesystem to be mounted. For example,
                        ``--kpop=nvme,ext4`` will include just the modules required for booting
                        NVMe disks and mounting your root ext4 filesystem. When this option is used,
                        a special minimal kernel module config is used instead of what is specified
                        via ``--kmod_config`` (see above).

USAGE
=====

In its simplest form, the command can be used as follows, as a regular user::

  $ ramdisk /var/tmp/my-new-initramfs
  $ sudo cp /var/tmp/my-new-initramfs /boot

By default, ``ramdisk`` will use your ``/usr/src/linux`` symlink to determine which
kernel to use to build a ramdisk for. It will parse ``/usr/src/linux/Makefile``,
extract kernel version information, and then find the appropriate directory in
``/lib/modules/<kernel_name>`` for copying modules. You can type:
``ramdisk list kernels`` and ``ramdisk --kernel <kernel_name>`` to build a ramdisk
for a non-default kernel.

Since this is brand-new software, it is highly recommended that you **DO NOT OVERWRITE
YOUR EXISTING, WORKING INITRAMFS THAT YOU CURRENTLY USE TO BOOT YOUR SYSTEM.**

Instead -- create a **NEW BOOT ENTRY** to test your initramfs. In GRUB, you can also
press 'e' to edit an entry and type in the name of the new initramfs to give it a try.


