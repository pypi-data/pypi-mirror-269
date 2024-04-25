# AO3StatScraper

`AO3StatScraper` is a small python package that provides command line scripts
to fetch your AO3 (*Archive Of Our Own*) statistics to store and display them.

## Installation

`AO3StatScraper` is available on [PyPI](https://pypi.org/project/ao3statscraper/), and
can obtained any regular way you'd install a python package, e.g. using `pip`, `conda`, etc.

For example, using `pip`:

On Unix/OSX:

```
python3 -m pip install ao3statscraper
```

On Windows:

```
py -m pip install ao3statscraper
```


Alternately, the source code is available on [gitlab](https://gitlab.com/athenaslilowl1/AO3StatScraper). 
On OSX and Linux, you can install a local version by cloning the repository using git:

```
git clone https://gitlab.com/athenaslilowl1/AO3StatScraper.git
cd AO3StatScraper  # go into the directory
python3 -m pip install .
```



## User Guide

### Getting Started

The main use case for `AO3StatScraper` is to fetch and display your current AO3 statistics using
scripts provided by `AO3StatScraper`. Currently, there are 4 scripts:

- `ao3get` : The main script to fetch your AO3 stats.
- `ao3plot`: Plots the stats stored with `ao3get`
- `ao3_hits_to_kudos`: List all your works in ascending order of their hits/kudos ratio
- `ao3_purge`: Deletes saved stats such that there is a minumum time between the remaining ones


**IMPORTANT**: Before you can run the other scripts, you first need to configure `AO3StatScraper`.
This is done by calling `ao3get`. It will launch the configuration dialogue automatically if it hasn't
been configured yet. You can always re-configure it by invoking `ao3get -c`.




### `ao3get`

This is the main script to fetch and store your AO3 stats. There are several running modes.
When in doubt, invoke `ao3get --help` to see the available options.

The default running mode is `--diff`.

- `--all`: Fetch and store current stats from AO3 into a snapshot, and display stats for all works.
- `--repeat`: Don't fetch new stats, but show the changes between the last two stored stats snapshots.
- `--diff`: Fetch and store current stats from AO3 into a snapshot, and display only stats for works that have changed since the last snapshot. If there were no changes in work stats, it will display only the user's total stats.
- `--config`: Run the configuration dialogue and exit.
- `--remove-last`: Deletes the last snapshot `ao3get` stored and exits. May come in handy if you're nervously re-downloading your stats every minute.
- `--no-write`: This flag modifies the behavious for `--all` and `--diff` running modes. While current stats are fetched from AO3, they won't be written into a snapshot.


Using `ao3get` requires you to log in to your AO3 account. You can either type in your username and password
each time you invoke it, or you can store it with `AO3StatScraper`, locked behind a master password. There
are no restrictions on how sophisticated your master password needs to be, so if you can't be inconvenienced,
you can even leave it empty.


### `ao3plot`

`ao3plot` will display some simple graphs based on the stored snapshots. It never stores snapshots itself,
you will need to do that using `ao3get`. 

By default, `ao3plot` will ask you to select which work you would like to see graphs of stats for. You can
also select to plot your total user statistics.

Alternately, you can skip that dialogue by using the following flags:

- `-u`: Show total user statistics.
- `-i [ID]`: Show the statistics for the work with AO3 ID `[ID]`. For example, if your work is under the link `https://archiveofourown.org/works/24280306`, the ID would be `24280306`.

It is possible that the stats graphs aren't displayed nicely on all screens. If that is the case for you,
you may want to try the `--no-prettify` flag to obtain a bare-bones plot without any prettifications. It
may not look as nice, but at least you should be able to see the data.



### `ao3_hits_to_kudos`

This script just reads in the last stored snapshot and prints out all your works in ascending order of their hits/kudos ratio.



### `ao3_purge`

In case you find yourself in a situation where you feel you have stored way too many snapshots, `ao3_purge` offers
you the option to delete stats snapshots such that there is some minimal time between them. By default, this frequency
is set to 12h. You can provide the frequency you like using the `--frequency` flag.





## Examples

This is example output what `ao3get` will show you when you run it:

![default running mode, diff](webdata/ao3get.png)

It will only list the works that have changes since you last cheked (i.e. stored a snapshot).

But you can also view all your works:

![show all works](webdata/ao3get-all.png)


Plotting the total user statistics with `ao3plot` will show you something like this:

![plotting user stats](webdata/plot-user.png)


Running `ao3plot` for a specific work will give you 2 plots:

![plotting work, Figure 1](webdata/plot-work1.png)
![plotting work, Figure 2](webdata/plot-work2.png)





# Having issues?

Please let me know by raising an issue on [gitlab](https://gitlab.com/athenaslilowl1/AO3StatScraper/-/issues)



# Roadmap and Contributing

This tool was always intended to be a command line tool on my end. Having never programmed a GUI in my life,
I don't intend to start now. However, if anybody is willing to pack this up in a nice simple portable GUI, 
you are very welcome and encouraged to do so! I'll gladly add it to the repository.

I'm using unix exclusively, so there may be issues on other operating systems. Testers and devs on OSX and
windows are also very welcome to let me know what's working and what needs fixing.
