#!/usr/bin/env python
from urllib.request import urlretrieve


def download_results(path):
    """Download CSV of fake Virginia election results from GDocs

    Downloads the file to the root of the repo (/path/to/refactoring101/).

    NOTE: This will only download the file if it doesn't already exist
    This approach is simplified for demo purposes. In a real-life application,
    you'd likely have a considerable amount of additional code
    to appropriately handle HTTP timeouts and other real-world scenarios.
    For example, you might retry a request several times after a timeout, and then
    send an email alert that the site is non-responsive.

    """
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR66f495XUWKbhP48Eh1PtQ9mN_pbHTh2m-nma9sv0banZSORUJKcugDNKFzuUBhJ5tcsUMN6moYAHb/pub?gid=0&single=true&output=csv"
    urlretrieve(url, path)


if __name__ == '__main__':
    download_results('fake_va_elec_results.csv')
