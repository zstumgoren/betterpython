# Write Better Python

- [Overview](#overview)
- [Setup](#setup)
- [Instructions](#instructions)
  - [Phase 1](#phase-1)
  - [Phase 2](#phase-2)
- [Parting words](#parting-words)

## Overview

Tutorial on using functions and modules to improve code readability and design, as part of a multi-step data pipeline.

> Created for the [Write Better Python][] session at [NICAR 2019] conference in Newport Beach, CA.

[Write Better Python]: https://tinyurl.com/betterpython
[NICAR 2019]: https://www.ire.org/events-and-training/event/3433/4087/

The tutorial steps through several iterations of code that downloads, cleans and summarizes some [fake election data][].

The repo contains three different versions of the code:

* `elex1/election_results.py` - a single gnarly, tear-inducing script
* `elex2/election_results.py` - a reworking of the original script in `elex1/` that uses functions to better organize the code
* [elex3](elex3/README.md) - a series of modules that can be run as stand-alone scripts, and an "orchestrator" script to run the full pipeline (`elex3/run_pipeline.py`)

## Setup

* Install Python 3.6-3.8 (or possibly higher?)
* Download or [clone][] this repo

[clone]: https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository

## Instructions

### Phase 1

Carefully review `elex1/election_results.py`.

Open a terminal and try running the code:

```bash
cd elex1/
python election_results.py
```

Review the CSVs it generates. Can you figure out what the code is doing? If not, don't worry. That's the point! The code is super convoluted and intended to make your brain hurt!

**Your mission is to rewrite this code so that a mere mortal can read and quickly understand it.**

In this first phase, we highly recommend printing the code -- yes printing ! -- on large paper in color (if you have the luxury).

Use a marker or pencil to circle areas of code that you think are
related, such as code that is standardizing data, tallying
votes, etc.

Give the circled sections of code a short but human-friendly
name. Those names will become the names of your *functions*.

Functions are reusable bits of code typically dedicated to a particular
task. Think of them as the action verbs of programming.

> If you're new to functions, you may want to take a detour and work through the [W3Schools Functions tutorial][].

[W3Schools Functions tutorial]: https://www.w3schools.com/python/python_functions.asp

Once you're comfortable with functions, here are some useful tidbits
to keep in mind as you rework `elex1/election_results.py`:

* Functions can take inputs and return outputs
* Functions can call other functions

Armed with that knowledge, try rewriting the script so that it uses
functions. This is basically a job in reorganizing code. For example,
you might create a `download` function that downloads the source CSV file and returns the file path to the locally downloaded file. That path can
then be fed as an argument to the next function.

In this way, you can group code into related functions and "chain" them together, with the input of one function coming from the output of the prior function.

Try reworking the code to see if you can apply functions and make it
more readable **while still producing the exact same results.**

### Bonus points

It's common in many programming languages to create a
`main` function, which is used to call "helper" functions and chain them together.

For example, the `main` function could call `download`, passing it the URL for the source data and saving the local file path returned by `download` to a variable. `main` can then pass that variable to the next function in your program.

Take a second pass at your program and try using `main` to call and chain together your new "helper" functions.

Using a `main` function to *orchestrate* your script can dramatically
improve it's readability. Just don't forget to call `main` at the
bottom of your script:

```python
# elex1/election_results.py
# The new and improved version!

# Higher up in the script you should have helper functions and a main function

# Just don't forget! Call main at the bottom of the script
main()
```

If you got through all of that, take a few moments to appreciate your
fancy new script. Grab a glass of wine and enjoy. Are you happy with
your new code? Are you already seeing ways to make it *even* better?

Now head on to Phase 2 and see if we came up with a similar solution.

### Phase 2

Navigate to the `elex2/` folder on your command line and run the script.

```python
cd elex2/
python election_results.py
```

It should produce the same results as Phase 1.

> Does our `elex2/election_results.py` look similar to the script you produced in Phase 1? Are there aspects you like better about ours? Yours?

OK, reflection time is over.

Now we're going to further improve our code by organizing our functions into well-named modules.

> If you don't know about modules, now's a good time to visit the [W3Schools Modules tutorial][].

[W3Schools Modules tutorial]: https://www.w3schools.com/python/python_modules.asp

Ok, ready? In this section, your job is to simply create well-named
modules and move your helper functions into the appropriate module.
Earlier we described functions as action verbs. It can be helpful
to think of modules as nouns or containers.

For example, you might consider creating a module called `scraper.py`
and put your `download` function in that module. Then you can call `download` 
at the bottom of the file in the same way that we called `main`.

```python
# scraper.py

def download(url):
  # do stuff to download
  pass
  
download()
```

Then in the terminal:

```bash
cd elex2/
python scraper.py
```

Rinse and repeat this process until `election_results.py` no longer
exists and you have two or more new modules that work that can perform each step in
your data "pipeline".

Notice that you can now run each of the steps (aka modules) independently? In this toy example, that may not seem like a big deal, but consider
how happy you'll be if the download process takes a minute, or 10 minutes, or...

Giving yourself the ability to execute discrete steps in your pipeline can be a huge time-saver!

But here's the downside: Now you need to remember or document the order in which to run the scripts. Wouldn't it be nice if you could run them all at once in addition to one at a time?

The good news is that there's a simple way to do that: Create one final module to import and run the functions from your new modules.

#### Interlude

To create an orchestrator module, or script, that can import your other code and run it all at once is easy. But it's not a bad idea to throw one final Python idiom into the mix: `if __name__ == '__main__':`. 

This is a gnarly bit of syntax that is widely used. It lets you [create "executable" modules that contain importable code](https://docs.python.org/3.8/tutorial/modules.html#executing-modules-as-scripts). It gives you the ability to execute some default behavior such as `download` when you run `python scraper.py`. But it also allows you to import code (ie `download`) from the module **without triggering that default behavior.**

It's a fancy little two-step that lets you avoid running the same code twice if you're importing functionality from one module and using it another.

Let's add this new idiom to `scraper.py`:

```python
# scraper.py

def download(url):
    # donwload and stuff
    pass

if __name__ == '__main__':
    url = "https://example.com" # Clearly this is an example and not the real URL!
    download(url)
```

With the above change, you can now (1) trigger the download by running `python scraper.py` *or* (2) import `download` from another module **without** triggering the download automatically.

So you can do something such as below without causing the download to occur twice.

```python
# some_other_module.py
from scraper import download

# use the download function and do other stuff
```

The above strategy may seem like overkill for our toy example, but it's a huge win when dealing with larger data files or high volumes of downloads (or both).

Apply this strategy to all of your modules and you've set the stage to create an "orchestrator" module that can run your entire data pipeline in the most efficient way possible. That's up next in the below `Bonus Points` section. Keep on truckin!

### Bonus points

In the functions section in [Phase 1](#phase-1), we learned how a `main` function can help "orchestrate" other helper functions and make our code more readable.

In a similar fashion, you might want to create a single module that can
import and run the code from all of your other modules.

We created an orchestrator script called `run_pipeline.py` and it contains, among other things, the import for the `download` function. Guess what else it contains? Yep, a `main` function!

But no more hints. Try creating your own `run_pipeline.py`. We'll wait...

OK, so you're done. Does your new orchestrator module improve the code? In particular, does it make it easier to
understand the separate steps in the overall pipeline and how they fit together?

Have you noticed a newfound freedom to run the entire pipeline at once or each step individually?

Before you run off for that last glass of wine, compare your code to our
final version in `elex3`.

Yours is better than ours right? Good. We think so too.

## Parting words

Code is never finished, only abandoned. Hopefully this exercise gave you
a first-hand feel for how to write code that is more reliable and
friendly to other humans (including future "you").

Happy coding!

[fake election data]: https://docs.google.com/spreadsheets/d/e/2PACX-1vR66f495XUWKbhP48Eh1PtQ9mN_pbHTh2m-nma9sv0banZSORUJKcugDNKFzuUBhJ5tcsUMN6moYAHb/pub?gid=0&single=true&output=csv
