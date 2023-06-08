---
title: 'pyOBIS: easy access to taxonomic occurrence records harvested from thousands of datasets'
tags:
  - Python
  - oceanography
  - marine data
authors:
  - name: Scott Chamberlain
    equal-contrib: true
  - name: Ayush Anand
    equal-contrib: true
    affiliation: 1
  - name: Tylar Murray
    corresponding: true
    affiliation: 2
  - name: Filipe Fernandes
    corresponding: true
  - name: Mathew Biddle
    corresponding: true
    affiliation: 3
affiliations:
 - name: National Institute of Technology Durgapur, India
   index: 1
 - name: IMaRS University of South Florida, US
   index: 2
 - name: National Oceanic and Atmospheric Administration, National Ocean Service, Integrated Ocean Observing System, US
   index: 3
date: 9 May 2023
bibliography: paper.bib
---

# Summary
The pyOBIS python package provides easy access to taxonomic occurrence records harvested from thousands of datasets.
The package uses the API from the Ocean Biodiversity Information System (OBIS),
a global open-access data and information clearinghouse on marine data for biodiversity for science, conservation,
and sustainable development.
OBIS has more than 107 million occurrence records, making availibility of ocean data possible but accesibility remains a challenge.
pyOBIS solves the challenge by providing built-in functions for accessing data on occurrences, taxons, nodes, checklists, and dataset metadatas.
Users can download, visualize, segment, process and export data to any format of your choice with its built-in tools or rich ecosystem of libraries in python.
Coupled together with other libraries like [pyDwcViz](https://github.com/marinebon/py-dwc-viz),
it forms an ecosystem of analysing Darwin Core Data with super ease through built-in functions.

# Introduction
OBIS is a global open-access data and information warehouse on marine biodiversity data.
It contains occurrence records, dataset metadatas, environmental data around species occurrences,
and many more biogeographic pointers.
The package provides easy export of data to Pandas DataFrame to help researchers focus more on analysis rather than data mining,
and several included Jupyter notebooks demonstrate example analyses that can be used as a starting point for addressing research questions related to global and local distributions of species across space and time.


# Why pyOBIS?
pyOBIS is intuitively split into different modules for querying IUCN red lists,
newly added species, datasets added, information on OBIS nodes, occurrence records,
MeasurementOrFacts, eDNA records, etc and searchable through unique IDs, taxa, scientific names,
geolocation, timestamps, and others.
The Taxa IDs used by OBIS is adopted from annotations by the WoRMS team thereby maintaining a uniform and universal identification convention.

## Main Features
pyOBIS python package improvess accessibility of data available through OBIS
and helps reduce efforts in manipulating and visualizing Darwin Core Data.
Some of the key features of pyOBIS are:
* **Easy handling of OBIS data**

  Users can easily fetch data without handling the API directly.
  The comprehensive documentation and built-in funtions provides support to both beginners and experienced researchers in handling Darwin Core Data.
  Response is always returned as a custom object with pre-defined methods to export to a `pandas` DataFrame,
  generate live API URL to plugin to any additional software, and
  build an OBIS Mapper URL for direct one-click visualization on the OBIS Mapper portal.

* **Smart download, processing and export of data**

  pyOBIS provides an interactive progress bar while fetching large occurrence records.
  It also provides an estimated size of the request and the expected time to taken for the download.
  pyOBIS un-nests entangled occurrence data, and increases readibility for beginner users.
  It provides easy export of data to Pandas DataFrame,
  so that researchers can export it to any format like `csv`, `excel`, `JSON` making data handling and compatibility
  with other software super-easy.

* **Richer support with sister packages**

  pyOBIS when coupled with sister packages e.g. `pyDwcViz` can be utilized to perform many important computations easily.
  With one-line function and plug-and-play use,
  users can generate biodiversity indices such as `ES50` and `Shannon's Index`,
  get environment statistics from occurrence records queried for specified geo-spatial region of interest,
  taxa, or other paramters,
  generate interactive distribution plots with taxanomic heirarchy easily,
  and many other possible use cases.

# Figures
![Absolute Depth for Lepidochelys kempii over time.\label{fig:time-series-turtle}](https://github.com/ayushanand18/pyobis/assets/36472216/b6e66f31-7bbd-49c9-8186-3ab1a58e57c0)

pyOBIS can be used to do super-useful time series analysis for instance, absolute depth of Sea Turtle species, Lepidochelys kempii between 1990-2011 as shown in figure \autoref{fig:time-series-turtle}. From this analysis, the following observations can be made:
* The average depth has increased over the years, this means the species is looking for cooler waters to escape the heating waters. (This can be observed from the magenta-colored line which depicts the 5-year rolling average.)
* The species has witnessed a slight compression, i.e., minimal and maximal depth have come closer. For a brief period, it compressed significantly (around 2006) this might be due to data constraints or maybe some seasonal current. After that it has regained a lot but still the average difference in minimal and maximal depth is lower than early 2000s.
* However, necessary precautions to avoid sampling bias must be taken into consideration.

# Conclusion


# Acknowledgements
We acknowledge the help of `Pandas`, `Matplotlib`, and `requests` python package, and all the authors for their contributions building this package, performing the associated analysis and drafting this manuscripts.

# References

# Citations
Citations to entries in paper.bib should be in
[rMarkdown](http://rmarkdown.rstudio.com/authoring_bibliographies_and_citations.html)
format.

If you want to cite a software repository URL (e.g. something on GitHub without a preferred
citation) then you can do it with the example BibTeX entry below for @fidgit.

For a quick reference, the following citation commands can be used:
- `@author:2001`  ->  "Author et al. (2001)"
- `[@author:2001]` -> "(Author et al., 2001)"
- `[@author1:2001; @author2:2001]` -> "(Author1 et al., 2001; Author2 et al., 2002)"
