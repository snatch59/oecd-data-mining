.. OECD Interface documentation master file, created by
   sphinx-quickstart on Mon Nov 20 08:51:29 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


.. |br| raw:: html

   <br />

==================
The OECD Interface
==================

The OECD_ Interface software suite provides a means to discover, download, and
convert SDMX-JSON_ data sets into CSV files. The files can be further processed
to select a subset according to set criteria (e.g. industries with electricity),
with specific fixed (normalized) column types. The suite covers:

* downloading list of all OECD data set IDs and descriptions;
* downloading list of all data set schema;
* downloading all OECD SDMX-JSON data sets;
* converting all time period data sets to un-pivoted CSV files;
* selecting a subset according to set criteria with specific fixed (normalized) column types
* concatenating this subset of fixed column CSV files into an overall master CSV file.

There is also the means to work with just OECD frequency dimension
data, which are a subset of the main time period data sets. This suite covers :

* identifing frequency dimension (annual/quarterly) supporting schema;
* downloading just OECD SDMX-JSON data sets with a frequency dimension;
* converting frequency dimension data sets to multi-indexed CSV files.

The OECD Interface software suite is written for Python 3.5, pandas 0.21.0, and
uses the pandasdmx_ 0.7.0 Python package to convert SDMX-JSON_ files to multi-indexed
CSV files.

.. _OECD: http://www.oecd.org/
.. _pandasdmx: https://pandasdmx.readthedocs.io/en/v0.7.0/
.. _SDMX-JSON: https://data.oecd.org/api/sdmx-json-documentation/

Software Suite
==============

oecd_keyfamilies.py
-------------------

Downloads the XML data structure schema for the data set IDs using the http query
http://stats.oecd.org/RESTSDMX/sdmx.ashx/GetDataStructure/ALL/. The XML schema are
then parsed for the data IDs and descriptions, which are saved in a CSV file.
Any HTTP comms failures are logged.

**Logs:** logs/oecd_keyfamilies.logs |br|
**Data In:** data from OECD server |br|
**Data Out:** OECD_keys/OECD_key_names.csv

oecd_schema.py
--------------

Downloads the XML schema for each of the data set IDs using the http query
http://stats.oecd.org/restsdmx/sdmx.ashx/GetSchema/, and saves as an XML file.
Any HTTP comms failures are logged. Execution should complete in around seven
minutes.

**Logs:** logs/oecd_schama.logs |br|
**Data In:** data from OECD server; OECD_keys/OECD_key_names.csv |br|
**Data Out:** OECD_schema/<dataset id>.xml


oecd_json_get_all.py
--------------------

Downloads the SDMX-JSON data set for each data set ID using the http query
stats.oecd.org/sdmx-json/data/<id>/all/all. The JSON data is saved without
newlines and indentation in order to save space. The program takes three or
four hours to download all the files, mainly due to HTTP timeouts or lack of
server availability.

**Logs:** logs/oecd_datasets.log |br|
**Data In:** data from OECD server; OECD_keys/OECD_key_names.csv |br|
**Data Out:** OECD_json_datasets/<dataset id>.json

oecd_json_convert_fullset.py
----------------------------

Iterates through the OECD_json_datasets directory attemting to load each data set
ID JSON file into pandasdmx. Those failing to load due to KeyError or Unicode
Errors are logged in the appropriate error CSV file. Those data sets with a time
period (which also includes the subset of those with a frequency dimension)
are converted to pandas DataFrames and saved to a CSV file.

**Logs:** error_reports/key_errors.csv; error_reports/unicode_errors.csv, error_reports/no_time_period.csv |br|
**Data In:** OECD_json_datasets/<id>.json |br|
**Data Out:** OECD_csv_datasets/<id>.csv

oecd_csv_criteria_merge.py
--------------------------

Analyses, selects and merges CSV data sets that match a set of criteria, as
follows:

Stage 1. Reads each data set CSV file in the OECD_csv_datasets directory, and
looks for evidence of a column matching one of the column criteria. A DataFrame
of candidate (matching column) data sets is created.

Stage 2. Iternates through the candidate DataFrames and produces a new DataFrame
for each, consisting only of rows that match a content criteria for the column
of interest. If the resulting DataFrame is not empty (i.e. content was found),
then stage 3 is carried out on that DataFrame.

Stage 3. This standardises the column names to a given template (YEAR, series,
INDUSTRY, MEASURE, NATION). First there is a tuple-column clean-up, followed by
the column rename, and a futher clean up and rename  of alternate industry
and country column names. Finally any additional columns that are not in the
template are merged together as tuples under the MEASURE column. If the
MEASURE column does not exist it is created. Each data set reaching this stage
is saved with an _C in the file name.

Stage 4. This takes all the _C files from stage 3, loads them, and concatenates
them into a single data set and saved as oecd_merged.csv.

**Logs:** none |br|
**Data In:** OECD_csv_datasets/<id>.csv |br|
**Data Out:** OECD_csv_processed/<id>_C.csv, OECD_csv_processed/oecd_merged.csv

Typical Workflow
================

As a program can rely on the output of another program, they should be run in
the following order:

1. oecd_keyfamilies.py
2. oecd_schema.py (*optional*)
3. oecd_json_get_all.py
4. ocecd_json_convert_fullset.py
5. oecd_csv_criteria_merge.py

Utilities
=========

Additions to the main software suite for diagnostic purposes, or for working
on a smaller number of data sets.

identify_freq_schema.py
-----------------------

Parses the XML schema for each data set ID to see if it supports a frequency
dimension such as annual, quarterly, etc. Data set IDs that support a frequency
dimension are stored in a CSV file.

**Logs:** none |br|
**Data In:** OECD_keys/OECD_key_names.csv; OECD_schema/<dataset id>.xml |br|
**Data Out:** OECD_keys/FREQ_key_names.csv

oecd_json_get_freq.py
---------------------

Only downloads the SDMX-JSON data set for each data set ID having a frequency domain,
using the http query stats.oecd.org/sdmx-json/data/<id>/all/all. The JSON data
is saved without newlines and indentation in order to save space.

**Logs:** logs/oecd_datasets.log |br|
**Data In:** data from OECD server; OECD_keys/FREQ_key_names.csv |br|
**Data Out:** OECD_json_datasets/<dataset id>.json

oecd_json_convert_freq.py
-------------------------

Uses the previously generated list of SDMX-JSON files supporting the frequency
domain to read in the corresponding JSON files, load them into pandasdmx,
produce a pandas data frame for annual data, and save to a multi-indexed CSV
file.

**Logs:** error_reports/freq_unicode_errors.csv; error_reports/freq_key_errors.csv |br|
**Data In:** OECD_json_datasets/<dataset id>.json; OECD_keys/FREQ_key_names.csv  |br|
**Data Out:** OECD_csv_datasets_A/<dataset id>_A.csv

oecd_json_get_timedout.py
-------------------------

Downloads the SDMX-JSON data set for each data set ID having previously been
noted as unavailable due to a request timeout,
using the http query stats.oecd.org/sdmx-json/data/<id>/all/all.

NOTE: if a data set is successfully retrieved it is not removed from
timed_out.csv. At the moment this has to be corrected manually. timed_out.csv
and http500.csv are also manually created at the moment.

**Logs:** logs/timedout.log |br|
**Data In:** data from OECD server; error_reports/timed_out.csv |br|
**Data Out:** OECD_json_datasets/<dataset id>.json

Issues and Limitations
======================

OECD Data Availability
----------------------

Potentially there are 1198 OECD data sources available. However,  at time of
writing 101 are not accessible due to the server not being available (HTTP error
500), and 55 are not accessible due to the HTTP data request timing out (a total
of 156 data sources not available). Unavailable data sources have been marked up
in a spreadsheet.

pandasdmx
---------

The 0.7.0 version of the pandasdmx Python package, though able to load all
time period SDMX-JSON data (excluding the KeyError issues) is only able to
convert to pandas DataFrames those with a frequency dimension present. However,
frequency dimension data sets only account for 219 data sources, of which only
128 of these are available from the OECD data server due to accessibility issues.
This leaves 979 data sources without a frequency dimension. To solve this
in-house code was written to convert all time period data to pandas DataFrames
allowing access to 835 data sets.

The following is a summary of know issues with pandasdmx 0.7.0:

Unicode Errors
~~~~~~~~~~~~~~

pandasdmx throws a Unicode exception for 63 data sets. One is due to malformed
JSON (use of non-escaped double quotes), the rest are in Portuguese, caused by
a capital A with an inflexion. Apart from the malformed JSON data set, there is
no move to fix this as the Portuguese data is a duplicate of data available in
English.

KeyError exception
~~~~~~~~~~~~~~~~~~

pandasdmx is unable to read in data due to throwing a KeyError exception for
some non-frequency dimension data sets.

Unable to create DataFrame
~~~~~~~~~~~~~~~~~~~~~~~~~~

pandasdmx is unable to create a pandas DataFrame for non-frequency
dimension data sets. However in-house code has been written to convert the
JSON-SDMX data loaded into pandasdmx into pandas DataFrames.
