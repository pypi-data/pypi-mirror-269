#!/usr/bin/env python
# coding: utf-8

import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.environ.get("XAHAUD_HOST", "0.0.0.0")
PORT = os.environ.get("XAHAUD_PORT", "6006")
XAHAUD_ENV = os.environ.get("XAHAUD_ENV", "standalone")
server_url = f"ws://{HOST}:{PORT}"
if XAHAUD_ENV == "testnet" or XAHAUD_ENV == "mainnet":
    server_url = f"wss://{HOST}"
