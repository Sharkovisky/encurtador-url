from app import app, db, os
from flask import render_template, request, redirect, session
from app.models.tables import Usuario, Link, LinksProibidos, Denuncias
import string, random, requests, time, re, urllib.parse
from itertools import product
from flask_login import login_required, current_user
from urllib.parse import urlparse

def load_blacklist():
    blacklist_file = "blacklist.txt"
    if os.path.exists(blacklist_file):
        with open(blacklist_file, "r", encoding="utf-8") as file:
            return {line.strip().lower() for line in file}
    return set()

BLACKLIST = load_blacklist()

def is_blocked(url):
    """Verifica se a URL contém um domínio proibido"""
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()
    return domain in BLACKLIST
