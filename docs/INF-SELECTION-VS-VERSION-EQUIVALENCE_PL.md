## Model wyboru INF i równoważności funkcjonalnej w sterownikach Windows

### Terminologia

- **INF**: deklaracyjny plik instalacyjny definiujący dopasowanie urządzeń i reguły instalacji
- **Pakiet sterownika (driver package)**: kompletny zestaw sterownika obejmujący INF, pliki binarne (.sys/.dll) oraz katalog podpisów
- **Wybór sterownika**: proces, w którym Windows wybiera pakiet sterownika na podstawie dopasowania i polityk systemowych

---

## Przegląd

Model sterowników Windows (SetupAPI + Windows Update) nie używa numerów wersji INF jako głównego kryterium instalacji ani aktualizacji sterownika.

Zamiast tego wybór pakietu sterownika opiera się na:

- dopasowaniu Hardware ID (HWID)
- dopasowaniu Compatible ID
- podpisie cyfrowym i poziomie zaufania (WHQL / Microsoft / OEM)
- polityce źródła sterownika (inbox, OEM, Windows Update)
- ograniczeniach zgodności systemowej

---

## Kluczowe pojęcie: równoważność funkcjonalna INF

Dwa pliki INF o różnych wersjach (np. 10.1.1.38 vs 10.1.1.44) mogą być traktowane jako **funkcjonalnie równoważne**, jeśli:

- definiują identyczne pokrycie HWID i Compatible ID
- prowadzą do identycznego wyniku bindowania urządzenia
- nie zmieniają zachowania instalacji ani konfiguracji systemu

W takim przypadku:

> Windows nie traktuje różnicy wersji INF jako kryterium wyboru sterownika.

---

## Ważna implikacja

Wyższa wersja INF nie oznacza:

- lepszego wsparcia sprzętowego
- lepszej wydajności
- wyższego priorytetu instalacji
- preferencji w Windows Update

Numer wersji INF pełni głównie rolę:

- metadanych wydania
- identyfikatora pakietu
- elementu dokumentacyjnego, nie decyzyjnego

---

## Rola klasy INF (doprecyzowanie)

Klasa urządzenia definiowana w INF (Class / ClassGuid):

- służy do kategoryzacji urządzeń
- wpływa na grupowanie kompatybilnych sterowników
- jest częścią kontekstu dopasowania

Nie stanowi jednak niezależnego poziomu rankingu w procesie wyboru sterownika.

---

## Dlaczego sterowniki mogą się zmieniać podczas aktualizacji systemu

Podczas aktualizacji systemu Windows lub czystej instalacji może dojść do zmiany sterownika z powodu:

- polityki migracji sterowników
- priorytetu sterowników inbox
- reguł zgodności systemowej
- wymuszenia bazowego zestawu sterowników

Jest to część procesu:

:contentReference[oaicite:1]{index=1}

i działa niezależnie od Windows Update.

---

## Różnica: Windows Update vs Windows Setup

### Windows Update (czas działania systemu)
- wybiera sterowniki na podstawie dopasowania i polityki
- nie stosuje logiki wersji jako kryterium
- zachowuje istniejący stan, jeśli jest równoważny

### Windows Setup (aktualizacja systemu)
- może zastąpić sterowniki podczas migracji
- może preferować sterowniki inbox lub bazowe
- może zmienić stan sterownika ze względów zgodności

Są to dwa różne mechanizmy decyzyjne.

---

## Podsumowanie

Windows Update instaluje pakiety sterowników na podstawie logiki dopasowania i zmiany stanu systemu, a nie numeru wersji INF.

Jeżeli dwa pakiety INF są funkcjonalnie równoważne w danym kontekście sprzętowym, są traktowane jako zamienne niezależnie od różnic w wersji.

Zmiana sterownika może jednak nastąpić podczas aktualizacji systemu, co wynika z polityki migracji i warstw bazowych Windows Setup, a nie z Windows Update.

Autor: Marcin Grygiel aka FirstEver ([LinkedIn](https://www.linkedin.com/in/marcin-grygiel))

---

## 📘 Przydatne linki


- [Najnowsze Wersje](https://github.com/FirstEverTech/Universal-Intel-Chipset-Updater/blob/main/Intel_Chipset_Drivers_Latest.md)
- [Updater Tool](https://github.com/FirstEverTech/Universal-Intel-Chipset-Updater)
- [Link do oficjalnego Intel Chipset Device Software](https://www.intel.com/content/www/us/en/download/19347/chipset-inf-utility.html)
- [Link w wyszukiwarkce Intela do Chipset INF Utility](https://www.intel.com/content/www/us/en/search.html?q=Chipset%20INF%20Utility)
- [Issue Tracker](https://github.com/FirstEverTech/Universal-Intel-Chipset-Updater/issues)
