# defense
This is under review.

[![Open in Code Ocean](https://codeocean.com/codeocean-assets/badge/open-in-code-ocean.svg)](https://codeocean.com/capsule/a01e51d9-0f62-40c5-bc9e-b4c8b16b421e/tree)

DOI: https://doi.org/10.24433/CO.7896039.v1

This is under review.

The goal of this project is to visualize military spending of countries.

Using a SIPRI dataset, milspend can visualize military spending of up to four countries.

The SIPRI dataset is downloadable from:

https://sipri.org/sites/default/files/SIPRI-Milex-data-1949-2020_0.xlsx

or the latest dataset from:

https://www.sipri.org/sites/default/files/SIPRI-Milex-data-1949-2022.xlsx

The number of the vertical axis indicates the US dollars in millions.

<img src='https://github.com/y-takefuji/defense/raw/main/result.png' width=640 height=480>

# How to install milspend on Linux, MacOS, or WSL on Windows
You may need matplotlib library.

$ pip install matplotlib

$ pip install -U milspend


# How to install milspend if you have a trouble.
$ pip install milspend --force-reinstall --no-cache-dir --no-binary :all:

# How to run milspend
Milspend program allows user to specify up to four countries to plot military spending of the specified countries.
For example, the following command can display military spending of the US, China, Russia and Japan in the graph.

For 0.0.1 and 0.0.2 with 1949-2020 dataset: Seperate countries with spaces.

$ milspend USA China Russia Japan

<img src='https://github.com/y-takefuji/defense/raw/main/uscnrujp.png' height=480 width=640>
The following command can display military spending of Japan and South Korea.


For 0.0.3 with with 1949-2022: Enclose up to four countries in single quotes and separate them with colons.

$ milspend 'Japan:Korea, South'

<img src='https://github.com/y-takefuji/defense/raw/main/jpkr.png' height=480 width=640>


