#!/usr/bin/env python3

import lojbanParser
import sys
from datetime import datetime

if __name__ == '__main__':
	starttime = datetime.now()
	txt = ""
	argv = sys.argv[1:]
	infile = None
	for arg in argv:
		if not arg.startswith("-"):
			if not infile:
				infile = arg
			else: # if not infile:
				print("Error: multiple input files (infile=" + infile + " current arg=" + arg+ ".")
				sys.exit(1)
			# end if not infile:
		# end if not arg.startswith("-"):
	# end for arg in argv:
	if infile:
		del argv[argv.index(infile)]
	else: # if infile:
		print("No input file given.")
		sys.exit(1)
	# end if infile:
	try:
		with open(infile, "r") as file:
			txt = file.read()
		# end with open(infile, "r") as file:
	except Exception as e:
		print(e)
		sys.exit(1)
	# end try except Exception as e:

	parser = lojbanParser.LojbanParser()
	parser.setparameters(*argv)
	starttimep = datetime.now()
	t = parser.parseString(txt)
	endtimep = datetime.now()
	if t:
		if parser.treemode:
			parser.tprint(t)
		elif parser.rulemode:
			parser.rprint(t)
		else:
			parser.print(t)
	endtime = datetime.now()
	print("Space used: {:d} bytes for tokens, {:d} bytes for strings.".format(\
		parser.tokspace, parser.stringspace), file = sys.stderr) 
	print("Time for parsing: {:s}.".format(str(endtimep - starttimep)), file = sys.stderr) 
	print("Time total      : {:s}.".format(str(endtime - starttime)), file = sys.stderr) ## TODO removed for DEBUG

# end if __name__ == '__main__':
