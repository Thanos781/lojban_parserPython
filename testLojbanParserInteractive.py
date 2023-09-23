#!/usr/bin/env python3

import lojbanParser
import sys
from datetime import datetime

if __name__ == '__main__':
	argv = sys.argv[1:]
	for arg in argv:
		if not arg.startswith("-"):
			print("Error: input file not accepted in interactive mode.")
			sys.exit(1)
		# end if not arg.startswith("-"):
	# end for arg in argv:

	parser = lojbanParser.LojbanParser()
	parser.setparameters(*argv)

	while True:
		txt = ""
		noinpout = False
		print(">>>", end = "", flush = True)
		for txtp in sys.stdin:
			if len(txtp) > 1:
				txt += txtp
				noinpout = False
			else: # if len(txtp) > 1:
				if noinpout:
					break
				# end if noinpout:
				noinpout = True
			# end if len(txtp) > 1:
		# end for txtp in sys.stdin:
		txt = txt.strip()

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

		print("Space used: {:d} bytes for tokens, {:d} bytes for strings.".format(\
			parser.tokspace, parser.stringspace), file = sys.stderr) 
		print("Time for parsing: {:s}.".format(str(endtimep - starttimep)), file = sys.stderr) 
	# end while True:

# end if __name__ == '__main__':
