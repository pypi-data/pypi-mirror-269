
## Copyright(c)  2023 Yoann Robin
## 
## This file is part of pigadm.
## 
## pigadm is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
## 
## pigadm is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## 
## You should have received a copy of the GNU General Public License
## along with pigadm.  If not, see <https://www.gnu.org/licenses/>.

#############
## Imports ##
#############

import sys
import os

from cartopy.feature import ShapelyFeature
from cartopy.io.shapereader import Reader
from cartopy.crs import PlateCarree

from .__core import pigadmParams


###############
## Functions ##
###############

def path( country , level ):
	return pigadmParams.build_path( country , str(level) )

def feature( country , level = 0 , **kwargs ):
	"""
	pigadm.feature
	==============
	
	Arguments
	---------
	country: [string]
		The country defined by the Alpha-3 code (ISO 3166-1 format).
	level: [integer]
		The level of subdivision. 0 is always the frontier of the country.
		Subdivision depends of the country.
	**kwargs:
		Others keywords arguments are given to the feature.
	
	Returns
	-------
	A 'cartopy.feature.ShapelyFeature'
	
	Notes
	-----
	Original data are available at: https://gadm.org/index.html
	
	"""
	
	shpfile = path( country , level )
	
	## Build feat kwargs
	fkwargs = { "edgecolor" : "black" , "facecolor" : "none" , "linestyle" : "-" if level == 0 else ":" }
	for key in kwargs:
		fkwargs[key] = kwargs[key]
	
	## Build the feature
	feature = ShapelyFeature( geometries = Reader(shpfile).geometries() , crs = PlateCarree() , **fkwargs )
	
	return feature


