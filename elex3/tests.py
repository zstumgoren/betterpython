import json
from os.path import dirname, join


import pytest

# Use relative import to reach into parent directory
from parser import parse_and_clean
from vote_tally import summarize

### Some helper functions/fixtures to load data for test
def load_json(path):
    json_file = open(join(dirname(__file__), 'fixtures', path), 'r')
    return json.load(json_file)

@pytest.fixture
def results():
    json_data = load_json('sample_results_parsed.json')
    results = summarize(json_data)
    return results['President']


### TESTS
def test_name_parsing():
    "Parser should split full candidate name into first and last names"
    path = join(dirname(__file__), 'fixtures/sample_results.csv')
    results = parse_and_clean(path)
    race_key = 'President'
    cand_key = 'GOP-Smith, Joe'
    # Get one county result
    smith = results[race_key][cand_key][0]
    assert smith['first_name'] == 'Joe'
    assert smith['last_name'] == 'Smith'

def test_racewide_vote_total(results):
    "Summary results should be annotated with total votes cast in race"
    assert results['all_votes'] == 31

def test_candiate_vote_totals(results):
    "Candidates votes should reflect total from all counties"
    # Loop through candidates and find Smith rather than relying on
    # default sorting of candidates, which would make this test brittle
    # if the implementation changed.
    smith = [cand for cand in results['candidates'] if cand['last_name'] == 'Smith'][0]
    assert smith['votes'] == 15

def test_winner_has_flag(results):
    "Winner flag should be assigned to candidates with most votes"
    doe = [cand for cand in results['candidates'] if cand['last_name'] == 'Doe'][0]
    assert doe['winner'] == 'X'

def test_loser_has_no_winner_flag(results):
    "Winner flag should not be assigned to candidate who does not have highest vote total"
    smith = [cand for cand in results['candidates'] if cand['last_name'] == 'Smith'][0]
    assert smith['winner'] == ''

def test_tie_race_winner_flags():
    "Winner flag should not be assigned to any candidate in a tie race"
    json_data = load_json('sample_results_parsed_tie_race.json')
    results = summarize(json_data)
    race = results['President']
    for cand in race['candidates']:
        assert cand['winner'] == ''