# pyGCSS

## Description

GCSS agent for collaboration with Geo2Tag GeoMongo and Smart-M3 Smart Space platforms. pyGCSS based on M3 Python API and
Geo2Tag GeoMongo HTTP requests.

## Source

* GCSSCore - gcss core, main methods
* GeoMongo - Ge2Tag Core (HTTP/REST requests)
* M3Core - Smart-M3 Python Core API
* M3Utility - Additional Smart-M3 Python API
* M3Tests - Smart-M3 examples
* examples - project examples

## Installation

* Install all additional packages for the platforms;
* Install last version of Smart-M3 with M3 Python API; Use Virtuoso storage for high performance.
* Install Geo2Tag GeoMongo platform

## Launch

* Launch Geo2Tag platform: ./local_deploy.sh or ./oauth_test_local_deploy.sh
* Launch Smart-M3: redsibd --storage-virtuoso-p=="dsn='VOS', host='127.0.0.1', user='dba', password='virtuoso'" && sib-tcp

## pyGCSS commands

TODO

## Links
 
* Smart-M3 sources: https://github.com/smart-m3
* Smart-M3 sourceforge: 
* Geo2Tag GeoMongo sources: https://bitbucket.org/osll/geomongo
