# Write Better Python

Tutorial on using functions and modules to improve code readability and design, as part of a multi-step data pipeline.

> Created for the [Write Better Python][] session at [NICAR 2019] conference in Newport Beach, CA.

[Write Better Python]: https://tinyurl.com/betterpython
[NICAR 2019]: https://www.ire.org/events-and-training/event/3433/4087/

The tutorial steps through several iterations of code that downloads, cleans and summarizes some [fake election data](https://tinyurl.com/fake-election-data). Along the way we add some basic test coverage so we can more confidently change the code.

The directories in this repo contain:

* elex1 - a single gnarly, tear-inducing script
* elex2 - a single script that uses functions and adds some test coverage
* [elex3](elex3/README.md) - a series of modules that can be run as stand-alone scripts, and an "orchestrator" script to run the full pipeline

