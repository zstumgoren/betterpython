#!/usr/bin/env python
import csv

from vote_tally import summarize


def write_csv(summary, csv_path):
    """Generates CSV from summary election results data

    USAGE:

        write_summary(summary_dict, csv_path)

    """
    with open(csv_path, 'w') as fh:
        # Limit output to cleanly parsed, standardized values
        fieldnames = [
            'date',
            'office',
            'district',
            'last_name',
            'first_name',
            'party',
            'all_votes',
            'votes',
            'winner',
        ]
        writer = csv.DictWriter(fh, fieldnames, extrasaction='ignore', quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for results in summary.values():
            cands = results.pop('candidates')
            for cand in cands:
                results.update(cand)
                writer.writerow(results)

if __name__ == '__main__':
    summarized_results = summarize('results.json')
    outfile = 'summary_results.csv'
    print("Generating results {}".format(outfile))
    write_csv(summarized_results, outfile)