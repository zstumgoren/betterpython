"""
In this second pass at the election_results.py script, 
we chop up the code into functions.

USAGE:

    python election_results.py

OUTPUT:

    summary_results.csv

"""
import csv
import urllib.request
from operator import itemgetter
from collections import defaultdict


# Primary function that orchestrates all steps in the pipeline
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

#### Helper Functions ####
### These funcs perform the major steps of our application ###

def download_results(path):
    """Download CSV of fake Virginia election results from GDocs"""
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR66f495XUWKbhP48Eh1PtQ9mN_pbHTh2m-nma9sv0banZSORUJKcugDNKFzuUBhJ5tcsUMN6moYAHb/pub?gid=0&single=true&output=csv"
    urllib.request.urlretrieve(url, path)

def parse_and_clean(path):
    """Parse downloaded results file and perform various data clean-ups


    RETURNS:

        Nested dictionary keyed by race, then candidate.
        Candidate value is an array of dicts containing county level results.

    """
    # Create reader for ingesting CSV as array of dicts
    reader = csv.DictReader(open(path, 'r'))

    # Use defaultdict to automatically create non-existent keys with an empty dictionary as the default value.
    # See https://docs.python.org/3.8/library/collections.html#collections.defaultdict
    results = defaultdict(dict)

    # Initial data clean-up
    for row in reader:
        # Parse name into first and last
        row['last_name'], row['first_name'] = [name.strip() for name in row['candidate'].split(',')]
        # Convert total votes to an integer
        row['votes'] = int(row['votes'])

        # Store county-level results by slugified office and district (if there is one), 
        # then by candidate party and raw name
        race_key = row['office'] 
        if row['district']:
            race_key += "-%s" % row['district']
        # Create unique candidate key from party and name, in case multiple candidates have same
        cand_key = "-".join((row['party'], row['candidate']))
        # Below, setdefault initializes empty dict and list for the respective keys if they don't already exist.
        race = results[race_key]
        race.setdefault(cand_key, []).append(row)

    return results


def summarize(results):
    """Tally votes for Races and candidates and assign winner flag.

    RETURNS:

        Dictionary of results

    """
    summary = defaultdict(dict)

    for race_key, cand_results in results.items():
        all_votes = 0
        cands = []
        for cand_key, results in cand_results.items():
            # Populate a new candidate dict using one set of county results
            cand = {
                'first_name': results[0]['first_name'],
                'last_name': results[0]['last_name'],
                'party': results[0]['party'],
                'winner': '',
            }
            # Calculate candidate total votes
            cand_total_votes = sum([result['votes'] for result in results])
            cand['votes'] = cand_total_votes
            # Add cand totals to racewide vote count
            all_votes += cand_total_votes
            # And stash the candidate's data
            cands.append(cand)

        # sort cands from highest to lowest vote count
        sorted_cands = sorted(cands, key=itemgetter('votes'), reverse=True)

        # Determine winner, if any
        first = sorted_cands[0]
        second = sorted_cands[1]

        if first['votes'] != second['votes']:
            first['winner'] = 'X'

        # Get race metadata from one set of results
        result = list(cand_results.values())[0][0]
        # Add results to output
        summary[race_key] = {
            'all_votes': all_votes,
            'date': result['date'],
            'office': result['office'],
            'district': result['district'],
            'candidates': sorted_cands,
        }

    return summary


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


# Q: What on earth is this __name__ == __main__ thing?
# A: Syntax that let's you execute a module as a script.
# http://docs.python.org/2/tutorial/modules.html#executing-modules-as-scripts
if __name__ == '__main__':
    main()
