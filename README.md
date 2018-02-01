# oecd-data-mining

The Organisation for Economic Co-operation and Development (OECD)
Interface software suite provides a means to discover, download,
and convert OECD SDMX-JSON data sets into CSV files. The files can be further
processed to select a subset according to set criteria (e.g. industries
with electricity), with specific fixed (normalized) column types. The
suite covers:

* downloading list of all OECD data set IDs and descriptions;
* downloading list of all data set schema;
* downloading all OECD SDMX-JSON data sets;
* converting all time period data sets to un-pivoted CSV files;
* selecting a subset according to set criteria with specific fixed (normalized) column types
* concatenating this subset of fixed column CSV files into an overall master CSV file.

There is also the means to work with just OECD frequency dimension data,
which are a subset of the main time period data sets. This suite covers :

* identifing frequency dimension (annual/quarterly) supporting schema;
* downloading just OECD SDMX-JSON data sets with a frequency dimension;
* converting frequency dimension data sets to multi-indexed CSV files.

The OECD Interface software suite is written for Python 3.5, pandas 0.21.0,
and uses the pandasdmx 0.7.0 Python package to convert SDMX-JSON files
to multi-indexed CSV files.

**The full online documentation is to be found here, and lays out the
workflow for using these utilities:
https://snatch59.github.io/oecd-data-mining/**
