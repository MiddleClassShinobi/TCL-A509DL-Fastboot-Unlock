# [GUIDE] TCL A3 A509DL (Tracfone): Free bootloader unlock on Windows

I recently repurposed a TCL A3 as a dedicated Apple Music player. Standard ADB reboot-to-bootloader commands weren't exposing Fastboot, so I worked with ChatGPT to develop a small Python utility that requests Fastboot directly through the MediaTek preloader serial interface. It worked on my handset.

Tested: A509DL / bangkok_TF, stock vLA9 (Android 11), Windows 11. One device tested; other revisions are unverified.

The utility sends a single FASTBOOT mode request; it does not flash partitions or unlock the bootloader by itself. The README documents the subsequent standard Fastboot unlock, prerequisites, warnings, troubleshooting, and verification. My handset returned READYTOOBTSAF, appeared in fastboot devices, and ultimately reported unlocked: yes.

Unlocking may erase all user data and weakens verified boot. Back up your phone and establish a recovery plan first. Only modify a device you own or have permission to modify. This is not a SIM/carrier unlock or FRP bypass. GSI installation is a separate procedure and is not covered by the utility.

Source and instructions: https://github.com/MiddleClassShinobi/TCL-A509DL-Fastboot-Unlock

If anyone else has this phone, please share your model, firmware version, and sanitized results. Do not post serial numbers, IMEI, hardware keys or personal filesystem paths.

Released under the MIT license.
