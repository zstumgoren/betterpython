# Using modules

In this section of the code, we organized the functions from `election_results.py` into separate Python [modules][]:

* `scraper.py`
* `parser.py`
* `vote_tally.py`
* `reports.py`

## Modules as scripts

Each module can be run individually as a script because we applied the `if __name__ == '__main__'` [idiom][] at bottom. For example, here are the last few lines of `parser.py`:

```
if __name__ == '__main__':
    import json
    data = parse_and_clean('fake_va_elec_results.csv')
    print(json.dumps(data, indent=4))
```

## Tying it together

We also created the script called `run_pipeline.py`, which imports our re-usable functions from each module and runs all the steps in the pipeline. 

Such a script is what would likely run as a scheduled job, perhaps as part of a daily web scrape.

## Why bother?

This type of code strategy allows you to incrementally build out a data pipeline. It frees you from having to re-run every step in the pipeline as you build out the code, which can save on development time and keep you in the good graces of web admins, for instance, whose site you may be scraping.

Finally, it gives you the freedom -- yes, freedom -- to focus on one problem at a time before tying together all the pieces.


[modules]: https://docs.python-guide.org/writing/structure/#modules
[idiom]: https://stackoverflow.com/questions/419163/what-does-if-name-main-do