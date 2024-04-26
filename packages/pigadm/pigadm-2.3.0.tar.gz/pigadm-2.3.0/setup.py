
## Copyright(c) 2022, 2023 Yoann Robin
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


## Start by import release details
import os

cpath = os.path.dirname(os.path.abspath(__file__)) ## current-path
with open( os.path.join( cpath , "pigadm" , "__release.py" ) , "r" ) as f:
    lines = f.readlines()
exec("".join(lines))

## Required elements
package_dir      = { "pigadm" : os.path.join( cpath , "pigadm" ) }
requires         = [ "sys" , "os" , "tempfile" , "urllib" , "progressbar2" , "zipfile" , "cartopy" ]
scripts          = ["scripts/pigadm"]
keywords         = ["GADM","shapefile","cartopy"]
platforms        = ["linux","macosx"]
packages         = [
    "pigadm",
    ]
classifiers      = [
	"Development Status :: 5 - Production/Stable",
	"License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
	"Natural Language :: English",
	"Operating System :: MacOS :: MacOS X",
	"Operating System :: POSIX :: Linux",
	"Programming Language :: Python :: 3",
	"Topic :: Scientific/Engineering :: Mathematics"
	]

## Now the setup
from setuptools import setup

setup(  name             = name,
        version          = version,
        description      = description,
        long_description = long_description,
        author           = authors[0],
        author_email     = authors_email[0],
        url              = src_url,
        packages         = packages,
        package_dir      = package_dir,
        requires         = requires,
        scripts          = scripts,
        license          = license,
        keywords         = keywords,
        platforms        = platforms
    )


