Changelog
=========

1.3.0 (2022-11-22)
-----------------------
- MAJOR:
    - none
- MINOR:
    - making UI simpler and more intuitive by a refactored OOP approach.
    - data is now returned as a response object with its own parameters and methods.
    - one-click method to every response object to convert it into a pandas DataFrame.
- PATCH:
    - various README improvements including better description of modules and their suggested use.

iobis/pyobis dev
-----------------------
- MAJOR:
    - none
- MINOR:
    - array handling added to taxonid occurrence search
    - progress bar added to downloads
    - new biodiversity notebook added
- PATCH:
     - added conda forge badge to README
     - various README improvements
     - fixes for google colab badge links

1.2.6 (2022-09-05)
-----------------------
- fixing PyPI publishing via github actions (https://github.com/iobis/pyobis/pull/85)
- Occurrences.search function update to bring in consistency in response (https://github.com/iobis/pyobis/pull/86)

1.2.5 (2022-09-05)
-----------------------
- updated analysis notebooks after feature upgrade (https://github.com/iobis/pyobis/pull/81)

1.2.4 (2022-08-30)
-----------------------
- made all modules class-ified i.e. creating response classes for each module.
    + defined two new functions for almost all modules
    + `get_search_url` method for getting the corresponding OBIS API URL for a request: defined for all modules and methods.
    + `get_mapper_url` method for getting the corresponding OBIS Mapper URL for a request: only for some modules.

1.1.4 (2022-08-30)
-----------------------
- rm obisissues (issue https://github.com/iobis/pyobis/issues/72)

1.1.3 (2022-7-24)
-----------------------
- adding a progress bar while fetching occurrence records
    + added a progress bar to `occurrences.search()` function to make the process more informative to the end user.

1.0.3 (2022-7-22)
-----------------------
- resolved issue: package throwing error for MoFs with occurrence records
    + Added a null-check function when accessing MoF records. Previously, accessing MoF records for species without any occurrence records resulted in an error.

1.0.2 (2022-7-22)
-----------------------
- resolved issue: MoF accessibility (duplicate columns)
    + resolved duplicate column issue when fetching MoF records. Some columns like scientificName and eventID were being repeated when performing inner_join on normalized and non-normalized DataFrame.

1.0.1 (2022-7-21)
-----------------------
- resolved occurrence pagination bug wherein subsequent records were not being fetched
    + fixed the bug while fetching occurrence records iteratively, w/ and w/o user-specified limits

1.0.0 (2022-7-10)
-----------------------
- updated all modules to the new OBIS API v3
    + updated checklist, nodes, occurrences, and taxa module
- removed resources, added dataset module

0.1.0 (2016-12-12)
-----------------------
- first push to pypi
- finished off all OBIS API routes

0.0.6.9000 (2016-5-12)
-----------------------
- Updated modules with missing methods
- Added modules: groups, resources
- Removed taxon module, just a taxa module now that has all taxa/taxon methods
- Updated docs

0.0.1 (2015-12-11)
------------------
- in the works...not on pypi yet
