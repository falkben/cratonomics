# Cratonomics

## Player Unknown's Battlegrounds (PUBG) Crate Expected Values

Python 3 program to download pricing data from the Steam [market](https://steamcommunity.com/market/) and calculate the [Expected Value](https://en.wikipedia.org/wiki/Expected_value) of opening a [PUBG](http://store.steampowered.com/app/578080/PLAYERUNKNOWNS_BATTLEGROUNDS/) crate compared to selling the crate on the Steam market.

For some crates, the containing item probability is published: [Biker / Desperado](https://steamcommunity.com/games/578080/announcements/detail/1576688908203724690),  [Raider / Triumph](https://steamcommunity.com/games/578080/announcements/detail/1653258341515442673) and [Militia / Fever](https://steamcommunity.com/games/578080/announcements/detail/2742000471562664977).  For other crates (Survivor / Wanderer), data was found online from a secondary [source](https://www.pubg-stats.net/depot/crates).  These probabilities could be innacurate.

Downloading pricing data from the Steam market is throttled to 1 request every 3 seconds.  Thus, the initial run time of the program is > 5 minutes.

This program saves the data into a locally running [mongoDB](https://www.mongodb.com/download-center) server.

## Install

1. Clone this repo
1. Create a virtual environment: `python -m venv env` (using Python3)
1. Activate virtual environment
    - Linux
        - `source env/bin activate`
    - Windows
        - `.\env\Scripts\activate`
1. Install prerequisits: `pip install -r requirements.txt`

## Run

1. `python get_price_data.py`
1. `python print_EVs.py`

## Output

```shell
> python print_EVs.py
Current time: Thu Feb 15 04:46:04 2018
Crate              Open EV ($)    Crate ($)    Key ($)    Price age (min)
---------------  -------------  -----------  ---------  -----------------
DESPERADO CRATE          -0.70         0.18       2.90              15.85
BIKER CRATE               0.21         0.86       0.00              14.62
SURVIVOR CRATE            0.09         0.48       0.00              13.09
WANDERER CRATE            0.10         0.60       0.00              11.51
```