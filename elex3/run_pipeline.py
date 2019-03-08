#!/usr/bin/env python
"""
This script orchestrates all steps in the data pipeline.

USAGE:

    python run_pipeline.py

OUTPUT:

    summary_results.csv containing racewide totals for each race/candidate pair.

"""
import csv

from scraper import download_results
from parser import parse_and_clean
from vote_tally import summarize
from reports import write_csv


def main():
    raw_data = 'fake_va_elec_results.csv'
    summary_csv = 'summary_results.csv'
    print("Downloading raw election data: {}".format(raw_data))
    download_results(raw_data)
    print("Cleaning data...")
    results = parse_and_clean(raw_data)
    print("Tallying votes and assigning winners...")
    summarized_results = summarize(results)
    print("Generating report: {}".format(summary_csv))
    write_csv(summarized_results, summary_csv)

if __name__ == '__main__':
    main()
