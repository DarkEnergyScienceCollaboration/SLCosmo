# SLCosmo
[![Build Status](https://travis-ci.org/DarkEnergyScienceCollaboration/SLCosmo.svg?branch=master)](https://travis-ci.org/DarkEnergyScienceCollaboration/SLCosmo)
[![Coverage Status](https://coveralls.io/repos/github/DarkEnergyScienceCollaboration/SLCosmo/badge.svg?branch=master)](https://coveralls.io/github/DarkEnergyScienceCollaboration/SLCosmo?branch=master)

Cosmological parameter inference from samples of time delay lenses, 
initially in the context of the second [Time Delay 
Challenge](http://timedelaychallenge.org). In the simple TDC2 ensemble 
analysis, the inputs are expected to be samples drawn from PDFs for the 
time delays plus likelhood functions for the corresponding Fermat 
potential differences (as could, in principle, be provided by the lens 
modelers); the output in the TDC2 case is a sampled posterior PDF for the 
Hubble constant, H0.

## Demo

* [Round Trip Test](https://github.com/drphilmarshall/SLCosmo/blob/master/notebooks/RoundTrip.ipynb) - put in an H0, generate a mock TDC2 submission, see if we can recover H0. 

## People
* [Phil Marshall](https://github.com/DarkEnergyScienceCollaboration/SLCosmo/issues/new?body=@drphilmarshall) (SLAC)
* Tom Collett (Portsmouth)

## License, etc.

This is open source software, available under the BSD license. If you are interested in this project, please do drop us a line via the hyperlinked contact names above, or by [writing us an issue](https://github.com/DarkEnergyScienceCollaboration/SLCosmo/issues/new).

## Installation, set-up and testing

From bash,
```
$ source <SLCosmo install directory>/setup/setup.sh
$ nosetests <SLCosmo install directory>
```
