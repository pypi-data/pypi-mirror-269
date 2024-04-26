
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
import warnings

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as mplg

from cartopy.feature import ShapelyFeature
from cartopy.io.shapereader import Reader

import cartopy.crs as ccrs
import cartopy.feature as cf


###############
## Functions ##
###############

def plot_GADM( pigadmParams ):
	
	warnings.simplefilter("ignore")
	
	mpl.rcdefaults()
	mpl.rcParams['font.size'] = 9
	mpl.rcParams['axes.linewidth']  = 0.5
	mpl.rcParams['lines.linewidth'] = 0.5
	mpl.rcParams['patch.linewidth'] = 0.5
	mpl.rcParams['xtick.major.width'] = 0.5
	mpl.rcParams['ytick.major.width'] = 0.5
	
	
	try:
		country = pigadmParams.arg[0]
		level   = pigadmParams.arg[1]
	except:
		raise Exception( f"Invalid input arguments: '{pigadmParams.arg}'" )
	
	shpfile = pigadmParams.build_path( country , str(level) )
	
	## Build feat kwargs
	fkwargs = { "edgecolor" : "red" , "facecolor" : "none" , "linestyle" : "-" }
	
	## Find extent
	bounds = np.array( [ g.bounds for g in Reader(shpfile).geometries() ] )
	bmax = bounds.max( axis = 0 )
	bmin = bounds.min( axis = 0 )
	extent = [min([bmax[0],bmax[2],bmin[0],bmin[2]]),max([bmax[0],bmax[2],bmin[0],bmin[2]]),min([bmax[1],bmax[3],bmin[1],bmin[3]]),max([bmax[1],bmax[3],bmin[1],bmin[3]])]
	dx     = 0.1 * (extent[1] - extent[0])
	dy     = 0.05 * (extent[3] - extent[2])
	extent[0] = extent[0] - dx
	extent[1] = extent[1] + dx
	extent[2] = extent[2] - dy
	extent[3] = extent[3] + dy
	
	extent[0] = max( extent[0] , -180 )
	extent[1] = min( extent[1] ,  180 )
	extent[2] = max( extent[2] ,  -90 )
	extent[3] = min( extent[3] ,   90 )
	
	## Build the feature
	feature = ShapelyFeature( geometries = Reader(shpfile).geometries() , crs = ccrs.PlateCarree() , **fkwargs )
	
	## Projection
	lon0,lon1,lat0,lat1 = extent
	if (lat1 - lat0 < 30) and abs(extent[3]) < 80:
		try:
			projection = ccrs.LambertConformal( central_longitude = (lon0+lon1) / 2 , central_latitude = (lat0+lat1) / 2 , standard_parallels = [ (lat0+lat1) / 4 , 3 * (lat0+lat1) / 4 ] )
		except:
			projection = ccrs.PlateCarree()
	else:
		projection = ccrs.PlateCarree()
	##
	scale = "10m"
	if min( [lat1-lat0,(lon1-lon0) / 2] ) > 30:
		scale = "50m"
	if min( [lat1-lat0,(lon1-lon0) / 2] ) > 60:
		scale = "110m"
	f_country = cf.NaturalEarthFeature( "cultural" , "admin_0_boundary_lines_land" , scale )
	f_land    = cf.NaturalEarthFeature( "physical" , "land"   , scale )
	f_ocean   = cf.NaturalEarthFeature( "physical" , "ocean"  , scale )
	
	##
	fig = plt.figure( dpi = 120 )
	grid = mplg.GridSpec( 2 , 1 )
	ax  = fig.add_subplot( grid[1,0] , projection = projection )
	ax.add_feature( feature , zorder = 2 )
	ax.add_feature( f_country , zorder = 1 , edgecolor = "grey" , facecolor = "none" , linestyle = ":" )
	ax.add_feature( f_land    , zorder = 1 , edgecolor = "grey" , facecolor = "none" )
	ax.add_feature( f_land    , zorder = 0 , edgecolor = "none"  , facecolor = cf.COLORS["land"] )
	ax.add_feature( f_ocean   , zorder = 0 , edgecolor = "none"  , facecolor = cf.COLORS["water"] )
	ax.set_extent( extent , crs = ccrs.PlateCarree() )
	ax.set_title( f"{country} level {level}" , fontdict = { "family" : "monospace" , "weight" : "bold" , "size" : 15 } )
	
	mm = 1. / 25.4
	pt = 1. / 72
	width = 120*mm
	
	try:
		ratio = ax.get_data_ratio() * ax.get_aspect()
	except:
		ratio = ax.get_data_ratio()
	
	h_ax  = width * ratio
	h_top = 20*pt
	
	grid.set_width_ratios([1])
	grid.set_height_ratios([h_top,h_ax])
	
	fig.set_figheight(h_top+h_ax)
	fig.set_figwidth(width)
	plt.subplots_adjust( left = 0 , right = 1 , bottom = 0 , top = 1 , hspace = 0 , wspace = 0 )
	
	try:
		plt.savefig( pigadmParams.arg[2] , dpi = 600 )
	except:
		plt.show()
	plt.close(fig)



