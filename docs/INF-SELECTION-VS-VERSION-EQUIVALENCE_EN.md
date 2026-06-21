## INF Selection and Functional Equivalence in Windows Driver Model

### Terminology
- **INF**: declarative installation file defining device matching and installation rules
  (INF file)
- **Driver package**: complete driver bundle including INF, binaries (.sys/.dll), and catalog files
- **Driver selection**: process by which Windows selects a driver package based on matching and policy rules

---

## Overview

The Windows Driver Model (SetupAPI + Windows Update) does not use INF version numbers as a primary decision factor for driver installation or upgrades.

Instead, driver package selection is based on:

- Hardware ID (HWID) matching
- Compatible ID matching
- Driver signing and trust level (WHQL / Microsoft / OEM)
- Driver source policy (inbox, OEM, Windows Update)
- System compatibility constraints

---

## Key concept: functional equivalence of INF files

Two INF files with different versions (e.g. 10.1.1.38 vs 10.1.1.44) may still be treated as **functionally equivalent** if:

- They define identical HWID and Compatible ID coverage
- They produce the same device binding outcome
- They do not change installation behavior or system configuration

In such cases:

> Windows does not perform a driver package upgrade or downgrade, even if a higher INF version is available.

---

## Important implication

A higher INF version does not imply:

- better hardware support
- improved performance
- higher installation priority
- preference in Windows Update selection

INF version is primarily:

- a release metadata field
- a tracking and packaging identifier
- not part of the driver selection decision logic

---

## Role of INF Class (clarification)

The INF-defined device class (Class / ClassGuid):

- is used for device categorization
- influences how compatible drivers are grouped
- is part of the matching context

However:

> It is NOT a standalone ranking factor in driver selection.

---

## Why Windows does not replace drivers

Windows installs or replaces a driver package only when there is a **state change**, meaning:

- a better HWID or Compatible ID match exists
- a different driver is required for correct binding
- system compatibility or policy conditions change
- a higher-ranked match is available based on selection logic

If two INF files produce the same system state, they are treated as interchangeable.

---

## Conclusion

Windows Update installs driver packages based on **matching logic and system state changes**, not INF version ordering.

If two INF packages are functionally equivalent in a given hardware context, they are treated as interchangeable regardless of version differences.

Author: Marcin Grygiel aka FirstEver ([LinkedIn](https://www.linkedin.com/in/marcin-grygiel))

---

## 📘 Useful Links


- [Intel Chipset INF Files List](https://github.com/FirstEverTech/Universal-Intel-Chipset-Updater/blob/main/Intel_Chipset_INFs_Latest.md)
- [Intel Chipset Device Software Link](https://www.intel.com/content/www/us/en/download/19347/chipset-inf-utility.html)
- [Intel Chipset INF Utility Search](https://www.intel.com/content/www/us/en/search.html#q=Chipset%20INF%20Utility)
- [Issue Tracker](https://github.com/FirstEverTech/Universal-Intel-Chipset-Updater/issues)
