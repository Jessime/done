# Done

Not another TODO app.

## Description

### Purpose

I've never found TODO lists particularly motivating.
That's not to say they aren't useful,
I just don't get the satisfaction of checking things off the list that some people do.
Part of the issue here is that TODO lists are dynamic. 
You add something to a TODO list, you complete half of it, 
and realize that to do the other half you have to get a bunch of other stuff done.
All of the sudden you end up with JIRA to manage your TODOs. 

On the other hand, what you've already _done_ is static.
Once you write it down, you don't have to worry about changing it. 
Additionally, I happen to find being forced to log my accomplishments very motivating.
If I know I'm going to have to write down what I did at the end of the day,
I want that list to be impressive (if only to myself).

### Features

These features are roughly ordered in terms of their importance:

* Your accomplishments are hierarchically aggregated over time. 
It's as easy to write weekly or monthly notes as daily ones.
* Data is version controlled and backed up to GitLab. 
You'll always have a backup of your data.
* Things are free form. 
There's no specified way to input data. 
Write about your day however you want.
* File management is automatic. Just type `done` and start writing.

## Installation

For now, the easiest thing to do is clone the repo and add an alias that points to `main.py`.
This will hopefully improve over time.

## Usage

Most of the time, you just need to run `main.py`.

### Flags

* `--day`, or `-d`. Specify this flag with an integer if you want to write about a day other than today.
For example, to write about yesterday, run `-d 1`. 
The integer indicates how many days before today you want to edit.
* `--week` or `-w`. Aggregate all of the days of from the week, and write about the week.
* `--month` or `-m`. Aggregate all of the weeks of from the month, and write about the month.
* `--year` or `-y`. Aggregate all of the weeks of from the month, and write about the month.
* `--save` or `-s`. Pass a file path to save that file to GitLab. 

## Warning

I'm writing this program for myself, and making changes on an "as needed" basis.
For example, I suspect I'll get around to writing the `year` function in January.
Linux support will come whenever I start using Ubuntu again. And so on.