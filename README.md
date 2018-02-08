# Player Unknown's Battlegrounds (PUBG) Crate Expected Values

Python 3 program to download pricing data from the Steam [market](https://steamcommunity.com/market/) and calculate the [Expected Value](https://en.wikipedia.org/wiki/Expected_value) of opening a [PUBG](http://store.steampowered.com/app/578080/PLAYERUNKNOWNS_BATTLEGROUNDS/) crate compared to selling the crate on the Steam market.

For some crates, the containing item probability is [published](https://steamcommunity.com/games/578080/announcements/detail/1576688908203724690) (Biker and Desperado).  For other crates (Survivor and Wanderer), data was found online from a secondary [source](https://www.pubg-stats.net/depot/crates).  These probabilities could be innacurate.

The pricing data download from the Steam market is throttled to 1 request every 3 seconds.  Thus, the initial run time of the program is > 5 minutes.

## Install

1. Clone this repo
1. Create a virtual environment: `python -m venv env` (using Python3)
1. Activate virtual environment: 
    - `source env/bin activate` (LINUX)
    - `.\env\Scripts\activate` (WIN)
1. Install prerequisits: `pip install -r requirements.txt`

## Run

1. `python get_price_data.py`
