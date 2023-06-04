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
The pyOBIS python package provides easy access to taxonomic occurrence records harvested from thousands of datasets. The package uses the API from the Ocean Biodiversity Information System (OBIS), a global open-access data and information clearinghouse on marine data for biodiversity for science, conservation, and sustainable development. Included in the pyOBIS package are built-in functions for accessing data on occurrences, taxon, nodes, checklists and datasets. The package provides easy export of data to Pandas DataFrame to help researchers focus more on analysis rather than data mining, and several included Jupyter notebooks demonstrate example analyses that can be used as a starting point for addressing research questions related to global and local distributions of species across space and time. Coupled together with other libraries like pyDwcViz, it forms an ecosystem of analysing Darwin Core Data with super ease through built-in functions.

# Statement of need

## Main Features
Here are just a few of things pyOBIS can do:
* Easy handling of OBIS data, easy fetching without handling the raw API response directly.
* Built-in functions for occurrence, taxon, node, checklist and dataset endpoints of OBIS API.
* Provides easy export of data to Pandas DataFrame, and helps researchers focus more on analysis rather than data mining.

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

# Figures
![Absolute Depth for Lepidochelys kempii over time.\label{fig:time-series-turtle}](https://github.com/ayushanand18/pyobis/assets/36472216/b6e66f31-7bbd-49c9-8186-3ab1a58e57c0)

pyOBIS can be used to do super-useful time series analysis for instance, absolute depth of Sea Turtle species, Lepidochelys kempii between 1990-2011 as shown in figure \autoref{fig:time-series-turtle}. From this analysis, the following observations can be made:
* The average depth has increased over the years, this means the species is looking for cooler waters to escape the heating waters. (This can be observed from the magenta-colored line which depicts the 5-year rolling average.)
* The species has witnessed a slight compression, i.e., minimal and maximal depth have come closer. For a brief period, it compressed significantly (around 2006) this might be due to data constraints or maybe some seasonal current. After that it has regained a lot but still the average difference in minimal and maximal depth is lower than early 2000s.
* However, necessary precautions to avoid sampling bias must be taken into consideration.

# Acknowledgements
We acknowledge the help of `Pandas`, `Matplotlib`, and `requests` python package, and all the authors for their contributions building this package, performing the associated analysis and drafting this manuscripts.

# References
