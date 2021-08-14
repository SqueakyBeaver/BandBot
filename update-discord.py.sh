#!/bin/sh
git clone https://github.com/Rapptz/discord.py
cd discord.py
pip install -U .
cd ..
rm -rf discord.py
