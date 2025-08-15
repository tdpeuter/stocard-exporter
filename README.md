# stocard-exporter
Extract loyalty cards from Stocard database

# How to use
1. Get `sync_db` and `sync_db-wal` from device via ADB or any other way (root maybe required).
```
$ adb pull /data/data/de.stocard.stocard/databases/sync_db* .
```
2. Check sync_db by any SQLite viewer, e.g. [DB Browser for SQLite](https://sqlitebrowser.org/) (required to make unsaved changes in db)
3. Copy `collect-cards.py` to same dir and run. Extracted cards will be saved in `./cards` directory.
4. PROFIT!