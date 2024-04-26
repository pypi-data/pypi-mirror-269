
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

#############
## Imports ##
#############

import sys
import os
import urllib.request
import zipfile
import progressbar

import logging
import datetime as dt
import argparse
import tempfile
import dataclasses
from pathlib import Path

from .__plot import plot_GADM

class DownloadBar:
	
	def __init__( self ):
		self.bar = None
	
	def __enter__( self ):
		return self
	
	def __exit__( self , *args ):
		print("")
	
	def update( self , b = 1 , bsize = 1 , tsize = None ):
		
		if self.bar is None and tsize is not None:
			self.bar = progressbar.DataTransferBar( max_value = tsize )
		
		if self.bar is not None:
			self.bar.update( min( b * bsize , tsize ) , force = True )



@dataclasses.dataclass
class PiGADMParams:##{{{
	
	abort         : bool                = False
	error         : Exception | None    = None
	help          : bool                = False
	log           : tuple[str,str|None] = (30,None)
	LINE          : str                 = "=" * 80
	iopath        : Path                = Path( os.environ.get( "XDG_DATA_HOME" , Path.home() / ".local" / "share" ) ) / "pigadm"
	version_major : int                 = 4
	version_minor : int                 = 1
	
	tmp_base : str | None                         = None
	tmp_gen  : tempfile.TemporaryDirectory | None = None
	tmp      : str | None                         = None
	
	cmd : str       | None = None
	arg : list[str] | None = None
	
	def init_from_user_input( self , *argv ):##{{{
		
		## Parser
		parser = argparse.ArgumentParser( add_help = False )
		parser.add_argument( "CMD" , nargs = '*' )
		parser.add_argument( "-h" , "--help" , action = "store_const" , const = True , default = False )
		parser.add_argument( "--log" , nargs = '*' , default = ("WARNING",None) )
		parser.add_argument( "--tmp" , default = None )
		
		## Transform in dict
		kwargs = vars(parser.parse_args(argv))
		
		## And store in the class
		for key in kwargs:
			if key in ["CMD"]:
				try:
					self.cmd = kwargs[key][0]
					self.arg = kwargs[key][1:]
				except:
					pass
				continue
			
			if key not in self.__dict__:
				raise Exception( f"Parameter '{key}' not present in the class" )
			self.__dict__[key] = kwargs[key]
			
		
	##}}}
	
	def init_tmp(self):##{{{
		
		if self.tmp is None:
			self.tmp_base = tempfile.gettempdir()
		else:
			self.tmp_base = self.tmp
		
		now               = str(dt.datetime.utcnow())[:19].replace("-","").replace(":","").replace(" ","-")
		prefix            = f"PYGADM_{now}_"
		self.tmp_gen      = tempfile.TemporaryDirectory( dir = self.tmp_base , prefix = prefix )
		self.tmp          = self.tmp_gen.name
	##}}}
	
	def init_logging(self):##{{{
		
		if len(self.log) == 0:
			self.log = ("INFO",None)
		elif len(self.log) == 1:
			
			try:
				level = int(self.log[0])
				lfile = None
			except:
				try:
					level = getattr( logging , self.log[0].upper() , None )
					lfile = None
				except:
					level = "INFO"
					lfile = self.log[0]
			self.log = (level,lfile)
		
		level,lfile = self.log
		
		## loglevel can be an integer
		try:
			level = int(level)
		except:
			level = getattr( logging , level.upper() , None )
		
		## If it is not an integer, raise an error
		if not isinstance( level , int ): 
			raise Exception( f"Invalid log level: {level}; nothing, an integer, 'debug', 'info', 'warning', 'error' or 'critical' expected" )
		
		self.log = (level,self.log[1])
		
		##
		log_kwargs = {
			"format" : '%(message)s',
#			"format" : '%(levelname)s:%(name)s:%(funcName)s: %(message)s',
			"level"  : level
			}
		
		if lfile is not None:
			log_kwargs["filename"] = lfile
		
		logging.basicConfig(**log_kwargs)
		logging.captureWarnings(True)
		
	##}}}
	
	def url( self , country ):##{{{
		return f"https://geodata.ucdavis.edu/gadm/gadm{self.version}/shp/gadm{self.version_major}{self.version_minor}_{country}_shp.zip"
	##}}}
	
	def check_path(self):##{{{
		if not os.path.isdir(self.iopath / f"gadm{self.version}"):
			os.makedirs(self.iopath / f"gadm{self.version}")
	##}}}
	
	def check(self):##{{{
		
		## Check the command
		if not self.cmd in ["load","list","path","plot",None]:
			raise Exception( f"Bad command '{self.cmd}', available commands are 'load', 'list', 'path'" )
		
		if self.cmd in ["load","path","plot"] and len(self.arg) == 0:
			raise Exception( f"Empty arguments for '{self.cmd}' command" )
			
		if self.cmd in ["path"] and not (len(self.arg) == 2):
			raise Exception( f"Empty arguments for '{self.cmd}' command" )
		
	##}}}
	
	def keys(self):##{{{
		keys = [key for key in self.__dict__]
		keys.sort()
		return keys
	##}}}
	
	def __getitem__( self , key ):##{{{
		return self.__dict__.get(key)
	##}}}
	
	## Properties ##{{{
	
	@property
	def version(self):
		return f"{self.version_major}.{self.version_minor}"
	##}}}
	
	def _run_load(self):##{{{
		
		if self.tmp is None:
			self.init_tmp()
		
		for country in self.arg:
			
			## Output
			zfile = f"gadm{self.version_major}{self.version_minor}_{country}_shp.zip"
			opath = self.iopath / f"gadm{self.version}" / country
			
			## Download file
			if self.log[1] is None and self.log[0] < 30:
				with DownloadBar() as dwb:
					urllib.request.urlretrieve( self.url(country) , os.path.join( self.tmp , zfile ) , reporthook = dwb.update )
			else:
				urllib.request.urlretrieve( self.url(country) , os.path.join( self.tmp , zfile ) )
			
			
			## Remove old files
			if os.path.isdir(opath):
				for f in os.listdir(opath):
					os.remove( os.path.join( opath , f ) )
			else:
				os.makedirs(opath)
			
			## And extract zip
			with zipfile.ZipFile( os.path.join( self.tmp , zfile ) , "r" ) as zobj:
				zobj.extractall( path = opath )
		
	##}}}
	
	def _run_list(self):##{{{
		
		countries = os.listdir( self.iopath / f"gadm{self.version}")
		countries.sort()
		
		for country in countries:
			files = [f for f in os.listdir( self.iopath / f"gadm{self.version}" / country ) if f.split(".")[-1] == "shp" ]
			files.sort()
			print( f"{country}: " + ", ".join([ f.split("_")[-1].split(".")[0] for f in files]) )
		
		
	##}}}
	
	def build_path( self , country , level ):##{{{
		
		if not country in os.listdir( self.iopath / f"gadm{self.version}"):
			if self.arg is not None:
				arg = tuple(self.arg)
			self.arg = [country]
			self._run_load()
			if arg is not None:
				self.arg = tuple(arg)
		
		files = [f for f in os.listdir( self.iopath / f"gadm{self.version}" / country ) if f.split(".")[-1] == "shp" ]
		files.sort()
		levels = [ f.split("_")[-1].split(".")[0] for f in files]
		
		if not level in levels:
			raise Exception( f"Level '{level}' not available for country '{country}'" )
		
		return self.iopath / f"gadm{self.version}" / country / files[levels.index(level)]
	##}}}
	
	def _run_path(self):##{{{
		
		country = self.arg[0]
		level   = self.arg[1]
		
		
		print( self.build_path( country , level ) )
	
	##}}}
	
	def _run_plot(self):##{{{
		plot_GADM(self)
	##}}}
	
	def run( self ):##{{{
		
		if self.cmd == "load":
			self._run_load()
		if self.cmd == "list":
			self._run_list()
		if self.cmd == "path":
			self._run_path()
		if self.cmd == "plot":
			self._run_plot()
	##}}}
	
##}}}

pigadmParams = PiGADMParams()
pigadmParams.check_path()


