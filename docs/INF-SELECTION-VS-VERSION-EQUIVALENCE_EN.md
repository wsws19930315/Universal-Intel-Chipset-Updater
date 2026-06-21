## INF Selection and Driver Ranking Model in Windows (v2.0)

### Terminology

- **INF**: declarative file defining device matching and installation rules
- **Driver package**: complete driver bundle including INF, binaries (.sys/.dll), and catalog
- **Driver selection**: process of selecting a driver package based on SetupAPI ranking

---

## Overview

The Windows driver selection system (SetupAPI + Windows Update) does not rely on INF version as a primary decision factor.

Instead, selection is based on a multi-layer ranking model:

- Hardware ID (HWID) match strength
- Compatible ID match strength
- Driver feature set (INF capabilities and installation sections)
- Driver signing and trust level (WHQL / Microsoft / OEM)
- Driver source policy (inbox, OEM, Windows Update)

---

## Driver ranking model (correct structure)

Windows driver selection uses a structured ranking system:

### 1. Match strength layer (primary)
- Exact HWID match
- Compatible ID match
- Partial / generic match

### 2. Feature / capability layer
- INF-defined installation behavior
- supported OS / architecture sections
- conditional install logic

### 3. Signature / trust layer
- WHQL certification
- Microsoft-signed vs OEM-signed drivers
- policy enforcement level

### 4. Tie-break layer
When all above factors are equal:

- DriverVer (date + version) may act as a tie-breaker

---

## Important clarification: DriverVer role

DriverVer is NOT a primary ranking factor.

It is only used when:

- HWID match score is identical
- feature score is identical
- signature level is identical

In that case:

> newer DriverVer may be preferred as a tie-breaker

---

## INF functional equivalence

Two INF files (e.g. 10.1.1.38 vs 10.1.1.44) may still be functionally equivalent if:

- they define identical HWID coverage
- they produce identical device binding results
- they do not change installation behavior

In such cases:

> no upgrade or downgrade occurs unless ranking conditions differ

---

## INF version vs decision logic

INF version number:

- is metadata
- is not part of primary ranking logic
- does not define compatibility
- does not override match strength

However:

> DriverVer date/version can influence final selection only in tie-break scenarios

---

## OS upgrade vs runtime behavior

### Windows Update (runtime system)
- fully ranking-driven
- DriverVer only used in tie-break cases
- preserves stable driver state if no better match exists

### Windows Setup (OS upgrade)
- may apply driver migration policies
- may replace drivers with inbox baseline drivers
- may enforce compatibility fallback rules

These are separate decision systems.

---

## Conclusion

Windows driver selection is primarily based on matching strength, feature capabilities, and signing trust.

DriverVer (date/version) is only used as a secondary tie-break factor when all other ranking dimensions are equal.

INF version itself is not a primary decision factor, but it is not entirely irrelevant in strict tie-break conditions.

Author: Marcin Grygiel aka FirstEver ([LinkedIn](https://www.linkedin.com/in/marcin-grygiel))

---

## 📘 Useful Links


- [Intel Chipset INF Files List](https://github.com/FirstEverTech/Universal-Intel-Chipset-Updater/blob/main/Intel_Chipset_INFs_Latest.md)
- [Intel Chipset Device Software Link](https://www.intel.com/content/www/us/en/download/19347/chipset-inf-utility.html)
- [Intel Chipset INF Utility Search](https://www.intel.com/content/www/us/en/search.html#q=Chipset%20INF%20Utility)
- [Issue Tracker](https://github.com/FirstEverTech/Universal-Intel-Chipset-Updater/issues)
