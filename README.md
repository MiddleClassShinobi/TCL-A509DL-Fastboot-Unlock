# TCL A3 A509DL — Fastboot entry and bootloader unlock

A small Windows-tested Python utility that requests Fastboot mode from the MediaTek preloader on a TCL A3 A509DL (Tracfone). Developed while repurposing an old phone as an Android music player.

## Verified configuration

- TCL A3 A509DL, product `bangkok_TF`, stock firmware vLA9 (Android 11)
- Windows 11, Python 3.13, PySerial 3.5
- MediaTek PreLoader USB VCOM (`0E8D:2000`), COM8 on the test PC
- Tested November 18, 2026 on one handset. Other firmware, models, and OSes are unverified.

The original script is included unchanged. It polls for the selected serial port for up to 45 seconds, sends a single ASCII `FASTBOOT` mode request, and reads the response. It does not issue flash, erase, or Download Agent commands; it does not itself unlock the bootloader. The standard Fastboot command is a separate step.

## Warnings

Only use this on a device you own or have permission to modify. Back up all data before proceeding. Unlocking normally erases user data and weakens verified boot protections. ROM flashing is a separate, risky procedure and can make the device unbootable. Have a reliable stock recovery plan before modifying partitions. This is not a SIM/carrier unlock or an FRP bypass. Do not assume support for any other device or firmware revision.

## Prerequisites

- Enable Developer options, OEM unlocking, and USB debugging in stock Android. If OEM unlocking is unavailable, do not assume this procedure will work.
- Install Python, the appropriate MediaTek USB VCOM driver, and Google's [Android SDK Platform-Tools](https://developer.android.com/tools/releases/platform-tools).
- Use a data-capable USB cable. Determine the actual MediaTek preloader COM port in Windows Device Manager (it may appear briefly when connecting the powered-off handset). Close other applications using that port.

## 1. Enter Fastboot

In Command Prompt, navigate to the folder containing `tcl_fastboot_probe.py` and install the dependency:

```cmd
py -m pip install -r requirements.txt
```

Power off and disconnect the phone. Start the script using your observed COM port (COM8 is only the tested example):

```cmd
py tcl_fastboot_probe.py COM8
```

Connect the powered-off phone via USB without holding buttons. The tested response was `READYTOOBTSAF`. An acknowledgement is not proof of Fastboot; verify it with the following commands from the Platform-Tools directory (or with Fastboot on your PATH):

```cmd
fastboot devices
fastboot getvar product
fastboot getvar unlocked
```

Confirm the detected product is `bangkok_TF` and that only your intended device is connected. If the device is not detected or the product differs, stop. A forbidden-mode response is not a success; do not continue to unlock.

## 2. Unlock the bootloader

**The next command can erase all user data.** Proceed only after backing up your phone and accepting the security implications.

```cmd
fastboot flashing unlock
```

Follow any confirmation displayed by the phone, then check:

```cmd
fastboot getvar unlocked
```

On the test handset, the unlock command was issued twice before checking; the final result was `unlocked: yes`. If the first attempt did not unlock and the phone still offers the normal unlock flow, review the device screen and retry once. Do not loop the command or assume an `OKAY` response by itself means the phone is unlocked. Stop if unlock is rejected.

Once unlocked:

```cmd
fastboot reboot
```

After Android starts and USB debugging is authorized again if needed, confirm:

```cmd
adb shell getprop ro.boot.flash.locked
adb shell getprop ro.boot.vbmeta.device_state
adb shell getprop ro.boot.verifiedbootstate
```

Observed results: `0`, `unlocked`, and `orange`, respectively. See [verified-session.txt](verified-session.txt) for a redacted excerpt of the successful session.

## Scope and limitations

The test phone later ran a Generic System Image (GSI) and Apple Music with portable microSD storage. This repository documents the Fastboot-entry/unlock portion only, not a complete ROM installation guide. Entering Fastboot was also verified a second time. Returning to userspace Fastboot (fastbootd) was a separate challenge and is not implemented by this script.

There is no claim of a universal MediaTek unlock, a security-fuse modification, or compatibility with other firmware versions. The successful test does not establish that this is the first published implementation. The Python file has been preserved as tested; no new hardware test was performed while packaging this release.

## Troubleshooting

- Timeout: check the observed COM port, VCOM driver, USB cable, and that the phone was fully off when connected.
- Forbidden response (`METAFORB`): stop; your firmware may not allow this mode request.
- Fastboot not detected: check the Windows Fastboot driver and Platform-Tools installation. Do not run unlocking commands until the intended handset is detected.

## Project status

Initial release candidate; one device tested. Please report model, firmware revision, Windows version, and the sanitized response when reporting results. Never post IMEI, serial number, hardware keys or personal filesystem paths.

Released under the MIT License; see [LICENSE](LICENSE).
