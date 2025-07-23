[app]
title = BugHunt
package.name = bughunt
package.domain = org.example.bughunt

# Ambil versi langsung dari main.py
version.regex = __version__ = ['"](.*)['"]
version.filename = %(source.dir)s/main.py

source.dir = .
source.include_exts = py,png,jpg,kv,atlas
requirements = python3,kivy

orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
