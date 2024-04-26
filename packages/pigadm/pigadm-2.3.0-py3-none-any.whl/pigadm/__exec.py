
## Copyright(c) 2023 Yoann Robin
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

##############
## Packages ##
##############

import sys,os
import datetime as dt
import logging


#############
## Imports ##
#############

from .__core import pigadmParams
from .__curses_doc import print_doc


##################
## Init logging ##
##################

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


###############
## Functions ##
###############

def run_pigadm():
	
	pigadmParams.run()
	

def start_pigadm(argv):
	
	## Time counter
	walltime0 = dt.datetime.utcnow()
	
	## User input
	pigadmParams.init_from_user_input(*argv)
	
	## Init logs
	pigadmParams.init_logging()
	
	## Logging
	logger.info(pigadmParams.LINE)
	logger.info( r"         _                    _             " )
	logger.info( r"  _ __  (_)  __ _   __ _   __| | _ __ ___   " )
	logger.info( r" | '_ \ | | / _` | / _` | / _` || '_ ` _ \  " )
	logger.info( r" | |_) || || (_| || (_| || (_| || | | | | | " )
	logger.info( r" | .__/ |_| \__, | \__,_| \__,_||_| |_| |_| " )
	logger.info( r" |_|        |___/                           " )
	logger.info(pigadmParams.LINE)
	logger.info( "Start: {}".format( str(walltime0)[:19] + " (UTC)") )
	logger.info(pigadmParams.LINE)
	
	## Serious functions start here
	try:
		## Check inputs
		pigadmParams.check()
		
		## Init temporary
		pigadmParams.init_tmp()
		
		## List of all input
		logger.info("Input parameters:")
		for key in pigadmParams.keys():
			if key in ["LINE"]: continue
			logger.info( " * {:{fill}{align}{n}}".format( key , fill = " ",align = "<" , n = 10 ) + ": {}".format(pigadmParams[key]) )
		logger.info(pigadmParams.LINE)
		
		## If abort, stop execution
		if pigadmParams.abort:
			raise pigadmParams.error
		
		## User asks help
		if pigadmParams.help:
			print_doc()
		
		## Run
		run_pigadm()
		
	except Exception as e:
		logger.error( f"Error: {e}" )
	
	## End
	walltime1 = dt.datetime.utcnow()
	logger.info(pigadmParams.LINE)
	logger.info( "End: {}".format(str(walltime1)[:19] + " (UTC)") )
	logger.info( "Wall time: {}".format(walltime1 - walltime0) )
	logger.info(pigadmParams.LINE)

