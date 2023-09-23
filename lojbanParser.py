#######################################################################
# imports

import sys
import inspect
import weakref
from io import StringIO

#######################################################################
## LojbanException
#######################################################################

class LojbanException(Exception):
	""" 
	class LojbanException defines Exceptions which are thrown during code 
	execution.
	It uses the method inspect to retrieve the information of the point 
	where the exception occurred. This information includes file name, 
	class name, method name, and line number.
	""" 
	def __init__(self, obj = None, msg = ""):
		self._classname = ""
		if not obj is None:
			self._classname = obj.__class__.__qualname__
		# end if not obj is None:
		(self._filename, self._linenumber, self._functionname) = \
			inspect.getframeinfo(inspect.currentframe().f_back)[:3]
		self._msg = msg
	# end def __init__(self):
 
	def __str__(self):
		return "LojbanException at ({:s} {:s}:{:s} {:d}): {:s}".format(\
			self._filename, self._classname, self._functionname, \
			self._linenumber, self._msg)
	# end def __str__(self):

	def __repr__(self):
		return self.__str__()
	# end def __repr__(self):

	@property
	def filename(self):
		return self._filename
	# end def filename(self):

	@property
	def classname(self):
		return self._classname
	# end def classname(self):

	@property
	def functionname(self):
		return self._functionname
	# end def functionname(self):

	@property
	def linenumber(self):
		return self._linenumber
	# end def linenumber(self):

	@property
	def msg(self):
		return self._msg
	# end def msg(self):
# end class LojbanException(Exception):

#######################################################################
## Parameters
#######################################################################

class Parameters:
	"""
	The parameters of the application which are set through command line
	arguments. The method setparameters parses the arguments and sets the
	values of the parameters.
	
	The parameters of the application and their usage are:
	1. Related to output generation:
		-dv prints each valsi as read.
		-dL prints each token as lexed by the compounder.
		-dR prints each compounder reduction as attempted.
		-dl prints each token as lexed by the YACC parser.
		-dr prints each YACC reduction as executed.
		-de prints each elidable terminator as inserted.
		-d* is equivalent to all other -d options together.

		-t produces a dump of the internal tree in TAB-separated columns:
			column 1 is a node number;
			column 2 is a rule/selma'o name;
			column 3 is a word for terminals;
			columns 3-n are numbers of subnodes for non-terminals;
			there are no forward references to nodes.

		-p outputs the text as a Prolog datum, with rule/selma'o names
			used as functors.

		-f outputs a full parse: normally, tree nodes with one
			child are omitted (most useful with -t or -p).
			
		-m MAXLINE: sets maximum number of characters per line for output.
			MAXLINE should be an integer. Zero of negative values for no limit.
			Defaults to 75.
			
	2. Related to application operation mode
		-e omits the insertion of elidables.

		-c displays cmavo and exits.
		
	3. Related to processing of the input
		--maxdepth MAXDEPTH sets maximum parsing tree depth
			MAXDEPTH should be an integer. 
			Zero of negative values for default value (200).
		
		--redmax REDMAX sets maximum number of parsing reductions
			REDMAX should be an integer. 
			Zero of negative values for default value (100).

		-d sets grammar debug mode on
		
		-g sets grammar error logging mode on
		
		--tfile FILE sets grammar error logging file.
			Used only when grammar error logging mode is on (default "grammar.tmp").
	"""
	def __init__(self):
		self._D_valsi = self._D_cpd_lex = False
		self._D_cpd_reduce = self._D_lex = False
		self._D_reduce = self._D_elidable = False
		self._treemode = self._simplemode = False
		self._elidemode = self._singlemode = False
		self._rulemode = self._mkcmavo = False
		self._maxline = 75
		self._yymaxdepth = 200
		self._yyredmax = 100
		self._yydebug = False
		self._yytflag = False
		self._yytfilen = "grammar.tmp"
	# end def __init__(self):

	def __str__(self):
		return "Parameters: " + \
			"D_valsi=" + str("True" if self._D_valsi else "False") + \
			" D_cpd_lex=" + str("True" if self._D_cpd_lex else "False") + \
			" D_cpd_reduce=" + str("True" if self._D_cpd_reduce else "False") + \
			" D_lex=" + str("True" if self._D_lex else "False") + \
			" D_reduce=" + str("True" if self._D_reduce else "False") + \
			" D_elidable=" + str("True" if self._D_elidable else "False") + \
			" treemode=" + str("True" if self._treemode else "False") + \
			" simplemode=" + str("True" if self._simplemode else "False") + \
			" elidemode=" + str("True" if self._elidemode else "False") + \
			" singlemode=" + str("True" if self._singlemode else "False") + \
			" rulemode=" + str("True" if self._rulemode else "False") + \
			" mkcmavo=" + str("True" if self._mkcmavo else "False") + \
			" maxline=" + str(self._maxline) + \
			" yymaxdepth=" + str(self._yymaxdepth) + \
			" yyredmax=" + str(self._yyredmax) + \
			" yydebug=" + str("True" if self._yydebug else "False") + \
			" yytflag=" + str("True" if self._ else "False") + \
			" yytfilen=" + str(self._yytfilen)
	# end def __str__(self):

	def ___repr__(self):
		return self.__str__()
	# end def ___repr__(self):

	def setparameters(self, *argv):
		"""
		Parses the command line arguments and sets the corresponding parameters.
		"""
		if len(argv) < 1:
			return
		# end if len(argv) < 1:
		iarg = 0
		while iarg < len(argv):
			arg = argv[iarg]
			if arg == "-dv": 
				self._D_valsi= True
				iarg = iarg + 1
			elif arg == "-dL": 
				self._D_cpd_lex= True
				iarg = iarg + 1
			elif arg == "-dR": 
				self._D_cpd_reduce= True
				iarg = iarg + 1
			elif arg == "-dl": 
				self._D_lex= True
				iarg = iarg + 1
			elif arg == "-dr": 
				self._D_reduce= True
				iarg = iarg + 1
			elif arg == "-de": 
				self._D_elidable= True
				iarg = iarg + 1
			elif arg == "-d*": 
				self._D_valsi = self._D_cpd_lex = \
					self._D_cpd_reduce = self._D_lex = \
					self._D_reduce = self._D_elidable= True
				iarg = iarg + 1
			elif arg == "-t":
				self._treemode = True
				iarg = iarg + 1
			elif arg == "-s":
				self._simplemode = True
				iarg = iarg + 1
			elif arg == "-e":
				self._elidemode = True
				iarg = iarg + 1
			elif arg == "-f":
				self._singlemode = True
				iarg = iarg + 1
			elif arg == "-p":
				self._rulemode = True
				iarg = iarg + 1
			elif arg == "-c":
				self._mkcmavo = True
				iarg = iarg + 1
			elif arg == "-m":
				iarg = iarg + 1
				if iarg < len(argv):
					try:
						self._maxline = int(argv[iarg])
						if self._maxline < 1:
							self._maxline = sys.maxsize
						# end if self._maxline < 1:
					except ValueError as e:
						raise LojbanException(self, "Error: invalid value " + str(argv[iarg]) +" for maxline (should be an integer).")
					# end try except ValueError as e:
				else: # if iarg < len(argv):
						raise LojbanException(self, "Error: argument maxline (-m) requires an integer value.")
				# end if (iarg + 1) < len(argv):
			elif arg == "--maxdepth":
				iarg = iarg + 1
				if iarg < len(argv):
					try:
						self._yymaxdepth = int(argv[iarg])
						if self._yymaxdepth < 1:
							self._yymaxdepth = 200
						# end if self._yymaxdepth < 1:
					except ValueError as e:
						raise LojbanException(self, "Error: invalid value " + str(argv[iarg]) +" for maxdepth (should be an integer).")
					# end try except ValueError as e:
				else: # if iarg < len(argv):
						raise LojbanException(self, "Error: argument maxdepth (--maxdepth) requires an integer value.")
				# end if (iarg + 1) < len(argv):
			elif arg == "--redmax":
				iarg = iarg + 1
				if iarg < len(argv):
					try:
						self._yyredmax = int(argv[iarg])
						if self._yyredmax < 1:
							self._yyredmax = 100
						# end if self._yyredmax < 1:
					except ValueError as e:
						raise LojbanException(self, "Error: invalid value " + str(argv[iarg]) +" for redmax (should be an integer).")
					# end try except ValueError as e:
				else: # if iarg < len(argv):
						raise LojbanException(self, "Error: argument redmax (--redmax) requires an integer value.")
				# end if (iarg + 1) < len(argv):
			elif arg == "-d":
				self._yydebug = True
			elif arg == "-g":
				self._yytflag = True
			elif arg == "--tfile":
				iarg = iarg + 1
				if iarg < len(argv):
					self._yytfilen = argv[iarg]
				else: # if iarg < len(argv):
						raise LojbanException(self, "Error: argument tmpfile (--tfile) requires a string value.")
				# end if (iarg + 1) < len(argv):
			else:
				raise LojbanException(self, "Error: unknown argument: " + str(arg))
			# end if arg
		# end for arg in argv:
	# end def setparameters(self, *argv):

	@property
	def D_valsi(self):
		return self._D_valsi
	# end def D_valsi(self):

	@property
	def D_cpd_lex(self):
		return self._D_cpd_lex
	# end def D_cpd_lex(self):

	@property
	def D_cpd_reduce(self):
		return self._D_cpd_reduce
	# end def D_cpd_reduce(self):

	@property
	def D_lex(self):
		return self._D_lex
	# end def D_lex(self):

	@property
	def D_reduce(self):
		return self._D_reduce
	# end def D_reduce(self):

	@property
	def D_elidable(self):
		return self._D_elidable
	# end def D_elidable(self):

	@property
	def elidemode(self):
		return self._elidemode
	# end def elidemode(self):

	@property
	def rulemode(self):
		return self._rulemode
	# end def rulemode(self):

	@property
	def simplemode(self):
		return self._simplemode
	# end def simplemode(self):

	@property
	def singlemode(self):
		return self._singlemode
	# end def singlemode(self):

	@property
	def treemode(self):
		return self._treemode
	# end def treemode(self):

	@property
	def yydebug(self):
		return self._yydebug
	# end def yydebug(self):

	@property
	def yymaxdepth(self):
		return self._yymaxdepth
	# end def yymaxdepth(self):

	@property
	def yyredmax(self):
		return self._yyredmax
	# end def yyredmax(self):

	@property
	def yytflag(self):
		return self._yytflag
	# end def yytflag(self):
	
	@property
	def yytfilen(self):
		return self._yytfilen
	# end def yytfilen(self):

	@property
	def maxline(self):
		return self._maxline
	# end def maxline(self):
	
	@property
	def mkcmavo(self):
		return self._mkcmavo
	# end def mkcmavo(self):
# end class Parameters:

#######################################################################
## Constants
#######################################################################

class Constants:
	"""
	This class contains:
		Application constants for cmavo, selmao types and lexer IDs.
		Utility methods based on constant values (rulename, isC, isV, get_vowels)
	"""
	def __init__(self):
		pass
	# end def __init__(self):

	@staticmethod
	def rulename(ruleid):
		"""
		Returns the rule name given its ID.
		"""
		_rulename = { \
			0 : "EOT", \
			10000 :  "text_0", \
			1 :  "text_A_1", \
			2 :  "text_B_2", \
			3 :  "text_C_3", \
			4 :  "paragraphs_4", \
			10 :  "paragraph_10", \
			11 :  "paragraph_A_11", \
			12 :  "paragraph_B_12", \
			20 :  "utterance_20", \
			30 :  "prenex_30", \
			32 :  "free_modifier_32", \
			33 :  "free_modifier_A_33", \
			34 :  "discursive_bridi_34", \
			35 :  "vocative_35", \
			36 :  "parenthetical_36", \
			40 :  "sentence_40", \
			41 :  "sentence_A_41", \
			42 :  "statement_42", \
			50 :  "bridi_tail_50", \
			51 :  "bridi_tail_A_51", \
			52 :  "bridi_tail_B_52", \
			53 :  "bridi_tail_C_53", \
			54 :  "gek_bridi_tail_54", \
			71 :  "tail_terms_71", \
			80 :  "terms_80", \
			81 :  "term_81", \
			82 :  "modifier_82", \
			83 :  "term_set_83", \
			90 :  "sumti_90", \
			91 :  "sumti_A_91", \
			92 :  "sumti_B_92", \
			93 :  "sumti_C_93", \
			94 :  "sumti_D_94", \
			95 :  "sumti_E_95", \
			96 :  "sumti_F_96", \
			110 :  "description_110", \
			111 :  "sumti_tail_111", \
			112 :  "sumti_tail_A_112", \
			121 :  "relative_clauses_121", \
			122 :  "relative_clause_122", \
			130 :  "selbri_130", \
			131 :  "selbri_A_131", \
			132 :  "selbri_B_132", \
			133 :  "selbri_C_133", \
			134 :  "selbri_D_134", \
			135 :  "selbri_E_135", \
			136 :  "selbri_F_136", \
			137 :  "GUhEK_selbri_137", \
			150 :  "tanru_unit_150", \
			151 :  "tanru_unit_A_151", \
			152 :  "tanru_unit_B_152", \
			160 :  "linkargs_160", \
			161 :  "links_161", \
			300 :  "quantifier_300", \
			310 :  "MEX_310", \
			311 :  "MEX_A_311", \
			312 :  "MEX_B_312", \
			313 :  "MEX_C_313", \
			330 :  "rp_expression_330", \
			332 :  "rp_operand_332", \
			370 :  "operator_370", \
			371 :  "operator_A_371", \
			372 :  "operator_B_372", \
			374 :  "MEX_operator_374", \
			381 :  "operand_381", \
			382 :  "operand_A_382", \
			383 :  "operand_B_383", \
			385 :  "operand_C_385", \
			400 :  "anaphora_400", \
			404 :  "cmene_404", \
			405 :  "cmene_A_405", \
			407 :  "bridi_valsi_407", \
			408 :  "bridi_valsi_A_408", \
			410 :  "para_mark_410", \
			411 :  "indicators_411", \
			412 :  "indicators_A_412", \
			413 :  "indicator_413", \
			415 :  "DOI_415", \
			416 :  "COI_416", \
			417 :  "COI_A_417", \
			421 :  "JOIK_EK_421", \
			422 :  "JOIK_JEK_422", \
			425 :  "NU_425", \
			426 :  "NU_A_426", \
			432 :  "quote_arg_432", \
			433 :  "quote_arg_A_433", \
			434 :  "ZOI_quote_434", \
			435 :  "ZO_quote_435", \
			436 :  "LOhU_quote_436", \
			440 :  "SEI_440", \
			443 :  "CO_443", \
			444 :  "CEI_444", \
			445 :  "NA_445", \
			447 :  "TUhE_447", \
			448 :  "LIhU_gap_448", \
			450 :  "gap_450", \
			451 :  "front_gap_451", \
			452 :  "MEX_gap_452", \
			453 :  "KEI_gap_453", \
			454 :  "TUhU_gap_454", \
			456 :  "VAU_gap_456", \
			457 :  "DOhU_gap_457", \
			458 :  "FEhU_gap_458", \
			459 :  "SEhU_gap_459", \
			460 :  "NUhU_gap_460", \
			461 :  "BOI_gap_461", \
			462 :  "sub_gap_462", \
			463 :  "LUhU_gap_463", \
			464 :  "GEhU_gap_464", \
			465 :  "MEhU_gap_465", \
			466 :  "KEhE_gap_466", \
			467 :  "BEhO_gap_467", \
			468 :  "TOI_gap_468", \
			469 :  "KUhO_gap_469", \
			470 :  "left_bracket_470", \
			471 :  "right_bracket_gap_471", \
			472 :  "LOhO_gap_472", \
			473 :  "TEhU_gap_473", \
			474 :  "right_br_no_free_474", \
			480 :  "SE_480", \
			481 :  "FA_481", \
			482 :  "NAhE_482", \
			483 :  "qualifier_483", \
			486 :  "subscript_486", \
			490 :  "mod_head_490", \
			491 :  "tag_491", \
			801 :  "utterance_ordinal_801", \
			802 :  "EK_802", \
			803 :  "EK_BO_803", \
			804 :  "EK_KE_804", \
			805 :  "JEK_805", \
			806 :  "JOIK_806", \
			807 :  "GEK_807", \
			808 :  "GUhEK_808", \
			809 :  "NAhE_BO_809", \
			810 :  "NA_KU_810", \
			811 :  "I_BO_811", \
			812 :  "number_812", \
			813 :  "GIhEK_BO_813", \
			814 :  "GIhEK_KE_814", \
			815 :  "tense_modal_815", \
			816 :  "GIK_816", \
			817 :  "lerfu_string_817", \
			818 :  "GIhEK_818", \
			819 :  "I_819", \
			821 :  "JEK_BO_821", \
			822 :  "JOIK_BO_822", \
			823 :  "JOIK_KE_823", \
			824 :  "PA_MOI_824", \
			906 :  "utt_ordinal_root_906", \
			911 :  "EK_root_911", \
			926 :  "JEK_root_926", \
			931 :  "JOIK_root_931", \
			932 :  "interval_932", \
			956 :  "I_root_956", \
			957 :  "simple_JOIK_JEK_957", \
			961 :  "number_root_961", \
			971 :  "simple_tag_971", \
			972 :  "simple_tense_modal_972", \
			973 :  "simple_tense_modal_A_973:", \
			974 :  "modal_974", \
			975 :  "modal_A_975", \
			977 :  "tense_A_977", \
			978 :  "tense_B_978", \
			979 :  "tense_C_979", \
			981 :  "GIK_root_981", \
			986 :  "lerfu_string_root_986", \
			987 :  "lerfu_word_987", \
			991 :  "GIhEK_root_991", \
			1030 :  "time_1030", \
			1031 :  "time_A_1031", \
			1032 :  "time_B_1032", \
			1033 :  "time_offset_1033", \
			1034 :  "time_interval_1034", \
			1035 :  "time_direction_1035", \
			1040 :  "space_1040", \
			1041 :  "space_motion_1041", \
			1042 :  "space_A_1042", \
			1043 :  "space_B_1043", \
			1044 :  "space_C_1044", \
			1045 :  "space_offset_1045", \
			1046 :  "space_intval_1046", \
			1047 :  "space_intval_A_1047", \
			1048 :  "space_direction_1048", \
			1050 :  "interval_modifier_1050", \
			1051 :  "interval_property_1051", \
			1052 :  "event_mod_1052", \
			1053 :  "event_mod_A_1053", \
			# 0 :  "YYSTYPE", \
			501 :  "A", \
			502 :  "BAI", \
			503 :  "BA'E", \
			504 :  "BE", \
			505 :  "BEI", \
			506 :  "BE'O", \
			507 :  "BI'I", \
			508 :  "BO", \
			509 :  "BRIVLA", \
			511 :  "BU", \
			513 :  "BY", \
			514 :  "CA'A", \
			515 :  "CAI", \
			516 :  "CEI", \
			517 :  "CMENE", \
			518 :  "CO", \
			519 :  "COI", \
			520 :  "CU", \
			521 :  "CU'E", \
			524 :  "DA'O", \
			525 :  "DOI", \
			526 :  "DO'U", \
			527 :  "FA", \
			528 :  "FA'A", \
			529 :  "FA'O", \
			530 :  "FE'E", \
			531 :  "FE'U", \
			532 :  "FI'O", \
			533 :  "FOI", \
			535 :  "FU'E", \
			536 :  "FU'O", \
			537 :  "GA", \
			538 :  "GE'U", \
			539 :  "GI", \
			541 :  "GI'A", \
			542 :  "GOI", \
			543 :  "GO'A", \
			544 :  "GU'A", \
			545 :  "I", \
			546 :  "JA", \
			547 :  "JAI", \
			548 :  "JOI", \
			550 :  "KE'E", \
			551 :  "KE", \
			552 :  "KEI", \
			554 :  "KI", \
			555 :  "KO'A", \
			556 :  "KU", \
			557 :  "KU'O", \
			558 :  "LA", \
			559 :  "LAU", \
			561 :  "LA'E", \
			562 :  "LE", \
			565 :  "LE'U", \
			566 :  "LI", \
			567 :  "LI'U", \
			568 :  "LO'O", \
			569 :  "LO'U", \
			571 :  "LU", \
			573 :  "LU'U", \
			574 :  "ME", \
			575 :  "ME'U", \
			577 :  "MO'I", \
			578 :  "NA", \
			581 :  "NAI", \
			583 :  "NA'E", \
			584 :  "NI'O", \
			585 :  "NOI", \
			586 :  "NU", \
			587 :  "NU'I", \
			588 :  "NU'U", \
			592 :  "PU", \
			593 :  "RA'O", \
			594 :  "ROI", \
			595 :  "SA", \
			596 :  "SE", \
			597 :  "SEI", \
			598 :  "SE'U", \
			601 :  "SI", \
			602 :  "SOI", \
			603 :  "SU", \
			604 :  "TA'E", \
			605 :  "TEI", \
			606 :  "TO", \
			607 :  "TOI", \
			610 :  "TU'E", \
			611 :  "TU'U", \
			612 :  "UI", \
			613 :  "VA", \
			614 :  "VAU", \
			615 :  "VE'A", \
			616 :  "VI'A", \
			617 :  "XI", \
			618 :  "Y", \
			621 :  "ZA'O", \
			622 :  "ZE'A", \
			623 :  "ZEI", \
			624 :  "ZI", \
			625 :  "ZI'E", \
			626 :  "ZO", \
			627 :  "ZOI", \
			628 :  "ZO'U", \
			651 :  "BOI", \
			655 :  "FU'A", \
			656 :  "GA'O", \
			657 :  "JO'I", \
			658 :  "KU'E", \
			661 :  "MAI", \
			662 :  "MA'O", \
			663 :  "MOI", \
			664 :  "MO'E", \
			665 :  "NA'U", \
			666 :  "NI'E", \
			667 :  "NU'A", \
			672 :  "PA", \
			673 :  "PE'O", \
			675 :  "TE'U", \
			677 :  "VEI", \
			678 :  "VE'O", \
			679 :  "VU'U", \
			697 :  "any", \
			698 :  "any", \
			699 :  "anyt'ing", \
			905 :  "lexer_A (utterance ordinal)", \
			910 :  "lexer_B (ek)", \
			915 :  "lexer_C (ek with BO)", \
			916 :  "lexer_D (ek with KE)", \
			925 :  "lexer_E (jek)", \
			930 :  "lexer_F (joik)", \
			935 :  "lexer_G (gek)", \
			940 :  "lexer_H (guhek)", \
			945 :  "lexer_I (NAhE BO)", \
			950 :  "lexer_J (NA KU)", \
			955 :  "lexer_K (i with BO)", \
			960 :  "lexer_L (number)", \
			965 :  "lexer_M (gihek with BO)", \
			966 :  "lexer_N (gihek with KE)", \
			970 :  "lexer_O (tense/modal)", \
			980 :  "lexer_P (gik)", \
			985 :  "lexer_Q (lerfu string)", \
			990 :  "lexer_R (gihek)", \
			995 :  "lexer_S (i or ijek)", \
			1000 :  "lexer", \
			1005 :  "lexer_U (jek with BO)", \
			1010 :  "lexer_V (joik with BO)", \
			1015 :  "lexer_W (joik with KE)", \
			1020 :  "lexer", \
			1025 :  "lexer_Y (numeric selbri)" \
			}
		return _rulename[ruleid] if ruleid in _rulename else ""
	# end def rulename(ruleid):

	@staticmethod
	def isC(c):
		"""
		Checks is a character is consonant.
		"""
		return c in "bcdfgjklmnprstvxz"
	# end def isC(c):

	@staticmethod
	def isV(c):
		"""
		Checks if a character is a vowel.
		"""
		return c in "aeiouy"
	# end def isV(c):

	@staticmethod
	def isindicator(tok):
		"""
		Checks if the token is an indicator according to its type.
		"""
		if tok().ttype in [Constants.UI_612, Constants.CAI_515, Constants.Y_618, \
			Constants.DAhO_524, Constants.FUhO_536, Constants.FUhE_535, \
			Constants.NAI_581]:
			return True
		# end if 
		return False
	# end def isindicator(tok):

	@staticmethod
	def get_vowels(text):
		"""
		Returns the type of token based on the character sequence.
		"""
		text0 = None
		try:
			text0 = text[0]
		except IndexError as e:
			text0 = None
		# end try except IndexError as e:
		text1 = None
		try:
			text1 = text[1]
		except IndexError as e:
			text1 = None
		# end try except IndexError as e:
		text2 = None
		try:
			text2 = text[2]
		except IndexError as e:
			text2 = None
		# end try except IndexError as e:
		text3 = None
		try:
			text3 = text[3]
		except IndexError as e:
			text3 = None
		# end try except IndexError as e:
		try:
			if text0 == "a": 
				if text1 is None:
					return Constants.A
				elif text1 == "'": 
					if text2 == "a":
						return Constants.UNK_M1 if text3 else Constants.AhA
					elif text2 == "e":
						return Constants.UNK_M1 if text3 else Constants.AhE
					elif text2 == "i":
						return Constants.UNK_M1 if text3 else Constants.AhI
					elif text2 == "o":
						return Constants.UNK_M1 if text3 else Constants.AhO
					elif text2 == "u":
						return Constants.UNK_M1 if text3 else Constants.AhU
					else:
						return Constants.UNK_M1
				elif text1 == "i":
					return Constants.UNK_M1 if text2 else Constants.AI
				elif text1 == "u":
					return Constants.UNK_M1 if text2 else Constants.AU
				else:
					return Constants.UNK_M1
			elif text0 == "e": 
				if text1 is None:
					return Constants.E
				elif text1 == "'": 
					if text2 == "a":
						return Constants.UNK_M1 if text3 else Constants.EhA
					elif text2 == "e":
						return Constants.UNK_M1 if text3 else Constants.EhE
					elif text2 == "i":
						return Constants.UNK_M1 if text3 else Constants.EhI
					elif text2 == "o":
						return Constants.UNK_M1 if text3 else Constants.EhO
					elif text2 == "u":
						return Constants.UNK_M1 if text3 else Constants.EhU
					else:
						return Constants.UNK_M1
				elif text1 == "i":
					return Constants.UNK_M1 if text2 else Constants.EI
				else:
					return Constants.UNK_M1
			elif text0 == "i": 
				if text1 is None:
					return Constants.I
				elif text1 == "'": 
					if text2 == "a":
						return Constants.UNK_M1 if text3 else Constants.IhA
					elif text2 == "e":
						return Constants.UNK_M1 if text3 else Constants.IhE
					elif text2 == "i":
						return Constants.UNK_M1 if text3 else Constants.IhI
					elif text2 == "o":
						return Constants.UNK_M1 if text3 else Constants.IhO
					elif text2 == "u":
						return Constants.UNK_M1 if text3 else Constants.IhU
					else:
						return Constants.UNK_M1
				elif text1 == "a":
					return Constants.UNK_M1 if text2 else Constants.IA
				elif text1 == "e":
					return Constants.UNK_M1 if text2 else Constants.IE
				elif text1 == "i":
					return Constants.UNK_M1 if text2 else Constants.II
				elif text1 == "o":
					return Constants.UNK_M1 if text2 else Constants.IO
				elif text1 == "u":
					return Constants.UNK_M1 if text2 else Constants.IU
				else:
					return Constants.UNK_M1
			elif text0 == "o": 
				if text1 is None:
					return Constants.O
				elif text1 == "'": 
					if text2 == "a":
						return Constants.UNK_M1 if text3 else Constants.OhA
					elif text2 == "e":
						return Constants.UNK_M1 if text3 else Constants.OhE
					elif text2 == "i":
						return Constants.UNK_M1 if text3 else Constants.OhI
					elif text2 == "o":
						return Constants.UNK_M1 if text3 else Constants.OhO
					elif text2 == "u":
						return Constants.UNK_M1 if text3 else Constants.OhU
					else:
						return Constants.UNK_M1
				elif text1 == "i":
					return Constants.UNK_M1 if text2 else Constants.OI
				else:
					return Constants.UNK_M1
			elif text0 == "u": 
				if text1 is None:
					return Constants.U
				elif text1 == "'": 
					if text2 == "a":
						return Constants.UNK_M1 if text3 else Constants.UhA
					elif text2 == "e":
						return Constants.UNK_M1 if text3 else Constants.UhE
					elif text2 == "i":
						return Constants.UNK_M1 if text3 else Constants.UhI
					elif text2 == "o":
						return Constants.UNK_M1 if text3 else Constants.UhO
					elif text2 == "u":
						return Constants.UNK_M1 if text3 else Constants.UhU
					else:
						return Constants.UNK_M1
				elif text1 == "a":
					return Constants.UNK_M1 if text2 else Constants.UA
				elif text1 == "e":
					return Constants.UNK_M1 if text2 else Constants.UE
				elif text1 == "i":
					return Constants.UNK_M1 if text2 else Constants.UI
				elif text1 == "o":
					return Constants.UNK_M1 if text2 else Constants.UO
				elif text1 == "u":
					return Constants.UNK_M1 if text2 else Constants.UU
				else:
					return Constants.UNK_M1
			elif text0 == "y":
				if text1 is None:
					return Constants.Y
				elif text != "y'y":
					return Constants.YhY
				else:
					return Constants.UNK_M1
			else:
				return Constants.UNK_M1
		except IndexError as e:
			return Constants.UNK_M1
		# end try except IndexError as e:
	# end def get_vowels(text):

	# constants for selmao
	A_501 = 501
	BAI_502 = 502
	BAhE_503 = 503
	BE_504 = 504
	BEI_505 = 505
	BEhO_506 = 506
	BIhI_507 = 507
	BO_508 = 508
	BRIVLA_509 = 509
	BU_511 = 511
	BY_513 = 513
	CAhA_514 = 514
	CAI_515 = 515
	CEI_516 = 516
	CMENE_517 = 517
	CO_518 = 518
	COI_519 = 519
	CU_520 = 520
	CUhE_521 = 521
	DAhO_524 = 524
	DOI_525 = 525
	DOhU_526 = 526
	FA_527 = 527
	FAhA_528 = 528
	FAhO_529 = 529
	FEhE_530 = 530
	FEhU_531 = 531
	FIhO_532 = 532
	FOI_533 = 533
	FUhE_535 = 535
	FUhO_536 = 536
	GA_537 = 537
	GEhU_538 = 538
	GI_539 = 539
	GIhA_541 = 541
	GOI_542 = 542
	GOhA_543 = 543
	GUhA_544 = 544
	I_545 = 545
	JA_546 = 546
	JAI_547 = 547
	JOI_548 = 548
	KEhE_550 = 550
	KE_551 = 551
	KEI_552 = 552
	KI_554 = 554
	KOhA_555 = 555
	KU_556 = 556
	KUhO_557 = 557
	LA_558 = 558
	LAU_559 = 559
	LAhE_561 = 561
	LE_562 = 562
	LEhU_565 = 565
	LI_566 = 566
	LIhU_567 = 567
	LOhO_568 = 568
	LOhU_569 = 569
	LU_571 = 571
	LUhU_573 = 573
	ME_574 = 574
	MEhU_575 = 575
	MOhI_577 = 577
	NA_578 = 578
	NAI_581 = 581
	NAhE_583 = 583
	NIhO_584 = 584
	NOI_585 = 585
	NU_586 = 586
	NUhI_587 = 587
	NUhU_588 = 588
	PU_592 = 592
	RAhO_593 = 593
	ROI_594 = 594
	SA_595 = 595
	SE_596 = 596
	SEI_597 = 597
	SEhU_598 = 598
	SI_601 = 601
	SOI_602 = 602
	SU_603 = 603
	TAhE_604 = 604
	TEI_605 = 605
	TO_606 = 606
	TOI_607 = 607
	TUhE_610 = 610
	TUhU_611 = 611
	UI_612 = 612
	VA_613 = 613
	VAU_614 = 614
	VEhA_615 = 615
	VIhA_616 = 616
	XI_617 = 617
	Y_618 = 618
	ZAhO_621 = 621
	ZEhA_622 = 622
	ZEI_623 = 623
	ZI_624 = 624
	ZIhE_625 = 625
	ZO_626 = 626
	ZOI_627 = 627
	ZOhU_628 = 628
	BOI_651 = 651
	FUhA_655 = 655
	GAhO_656 = 656
	JOhI_657 = 657
	KUhE_658 = 658
	MAI_661 = 661
	MAhO_662 = 662
	MOI_663 = 663
	MOhE_664 = 664
	NAhU_665 = 665
	NIhE_666 = 666
	NUhA_667 = 667
	PA_672 = 672
	PEhO_673 = 673
	TEhU_675 = 675
	VEI_677 = 677
	VEhO_678 = 678
	VUhU_679 = 679
	any_words_697 = 697
	any_word_698 = 698
	anything_699 = 699
	# constants for lexers
	lexer_A_905 = 905
	lexer_B_910 = 910
	lexer_C_915 = 915
	lexer_D_916 = 916
	lexer_E_925 = 925
	lexer_F_930 = 930
	lexer_G_935 = 935
	lexer_H_940 = 940
	lexer_I_945 = 945
	lexer_J_950 = 950
	lexer_K_955 = 955
	lexer_L_960 = 960
	lexer_M_965 = 965
	lexer_N_966 = 966
	lexer_O_970 = 970
	lexer_P_980 = 980
	lexer_Q_985 = 985
	lexer_R_990 = 990
	lexer_S_995 = 995
	lexer_T_1000 = 1000
	lexer_U_1005 = 1005
	lexer_V_1010 = 1010
	lexer_W_1015 = 1015
	lexer_X_1020 = 1020
	lexer_Y_1025 = 1025
	## These defines are for unknown and experimental cmavo. ##
	UNK_M1 = -1
	XAI_M2 = -2
	# additional constants for character sequences
	A = 0
	AhA = 1
	AhE = 2
	AhI = 3
	AhO = 4
	AhU = 5
	AI = 6
	AU = 7
	E = 8
	EhA = 9
	EhE = 10
	EhI = 11
	EhO = 12
	EhU = 13
	EI = 14
	I = 15
	IhA = 16
	IhE = 17
	IhI = 18
	IhO = 19
	IhU = 20
	O = 21
	OhA = 22
	OhE = 23
	OhI = 24
	OhO = 25
	OhU = 26
	OI = 27
	U = 28
	UhA = 29
	UhE = 30
	UhI = 31
	UhO = 32
	UhU = 33
	Y = 34
	# /* Used only in vowel tables: */
	IA = 35
	IE = 36
	II = 37
	IO = 38
	IU = 39
	UA = 40
	UE = 41
	UI = 42
	UO = 43
	UU = 44
	YhY = 45	

	vowel_cmavo = ( \
		A_501, UI_612, UI_612, UI_612, UI_612, UI_612, UI_612, \
		UI_612, A_501, UI_612, UI_612, UI_612, UI_612, UI_612, \
		UI_612, I_545, UI_612, UI_612, UI_612, UI_612, UI_612, \
		A_501, UI_612, UI_612, UI_612, UI_612, UI_612, UI_612, \
		A_501, UI_612, UI_612, UI_612, UI_612, UI_612, Y_618, \
		UI_612, UI_612, UI_612, UI_612, UI_612, \
		UI_612, UI_612, UI_612, UI_612, UI_612, \
		BY_513 \
	)

	b_cmavo = ( \
		PU_592, UI_612, BAhE_503, BAI_502, ZAhO_621, UI_612, BAI_502, \
		BAI_502, BE_504, FAhA_528, COI_519, BAI_502, BEhO_506, UI_612, \
		BEI_505, PA_672, UNK_M1, UNK_M1, BIhI_507, BIhI_507, UI_612, \
		BO_508, UNK_M1, UNK_M1, UNK_M1, UNK_M1, UNK_M1, BOI_651, \
		BU_511, GOhA_543, GOhA_543, GOhA_543, UNK_M1, FAhA_528, BY_513 \
	)

	c_cmavo = ( \
		PU_592, CAhA_514, UI_612, BAI_502, ZAhO_621, FAhA_528, CAI_515, \
		BAI_502, JOI_548, LAU_559, UNK_M1, PA_672, JOI_548, UNK_M1, \
		CEI_516, PA_672, UNK_M1, BAI_502, PA_672, BAI_502, BAI_502, \
		CO_518, ZAhO_621, GOhA_543, ZAhO_621, COI_519, ZAhO_621, COI_519, \
		CU_520, VUhU_679, CUhE_521, CAI_515, MOI_663, BAI_502, BY_513 \
	)

	d_cmavo = ( \
		KOhA_555, PA_672, KOhA_555, UI_612, DAhO_524, KOhA_555, UI_612, \
		PA_672, KOhA_555, ZAhO_621, KOhA_555, BAI_502, VUhU_679, KOhA_555, \
		KOhA_555, KOhA_555, ZAhO_621, KOhA_555, TAhE_604, BAI_502, KOhA_555, \
		KOhA_555, UI_612, BAI_502, KOhA_555, KOhA_555, DOhU_526, DOI_525, \
		GOhA_543, FAhA_528, PA_672, BAI_502, BAI_502, NU_586, BY_513 \
	)

	f_cmavo = ( \
		FA_527, FAhA_528, BAI_502, VUhU_679, FAhO_529, JOI_548, FA_527, \
		BAI_502, FA_527, VUhU_679, FEhE_530, VUhU_679, COI_519, FEhU_531, \
		PA_672, FA_527, FA_527, BAI_502, COI_519, FIhO_532, PA_672, \
		FA_527, KOhA_555, KOhA_555, KOhA_555, KOhA_555, KOhA_555, FOI_533, \
		FA_527, FUhA_655, FUhE_535, UI_612, FUhO_536, VUhU_679, BY_513 \
	)

	g_cmavo = ( \
		GA_537, BAI_502, BY_513, UI_612, GAhO_656, FAhA_528, PA_672, \
		BAI_502, GA_537, VUhU_679, UI_612, GA_537, BY_513, GEhU_538, \
		VUhU_679, GI_539, GIhA_541, GIhA_541, GIhA_541, GIhA_541, GIhA_541, \
		GA_537, GOhA_543, GOhA_543, GOhA_543, GOhA_543, GOhA_543, GOI_542, \
		GA_537, GUhA_544, GUhA_544, GUhA_544, GUhA_544, GUhA_544, BY_513 \
	)

	j_cmavo = ( \
		JA_546, NA_578, BAI_502, BAI_502, UI_612, UNK_M1, JAI_547, \
		PA_672, JA_546, NAhE_583, COI_519, JA_546, BY_513, UI_612, \
		NU_586, A_501, UI_612, BAI_502, PA_672, BAI_502, BAI_502, \
		JA_546, UI_612, JOI_548, JOhI_657, BY_513, JOI_548, JOI_548, \
		JA_546, UI_612, UNK_M1, COI_519, UI_612, VUhU_679, BY_513 \
	)

	k_cmavo = ( \
		NU_586, BAI_502, CAhA_514, BAI_502, PA_672, UI_612, BAI_502, \
		UI_612, KE_551, KOhA_555, KEhE_550, GAhO_656, COI_519, UI_612, \
		KEI_552, KI_554, UI_612, COI_519, BAI_502, PA_672, BAI_502, \
		KOhA_555, KOhA_555, KOhA_555, KOhA_555, KOhA_555, KOhA_555, \
		BAI_502, KU_556, JOI_548, KUhE_658, UI_612, KUhO_557, \
		BAI_502, BY_513 \
	)

	l_cmavo = ( \
		LA_558, UI_612, LAhE_561, LA_558, ZOI_627, BAI_502, LA_558, \
		LAU_559, LE_562, BAI_502, LE_562, LE_562, UI_612, LEhU_565, \
		LE_562, LI_566, UI_612, BAI_502, NU_586, UI_612, LIhU_567, \
		LE_562, BY_513, LE_562, LE_562, LOhO_568, LOhU_569, LE_562, \
		LU_571, LAhE_561, LAhE_561, LAhE_561, LAhE_561, LUhU_573, BY_513 \
	)

	m_cmavo = ( \
		KOhA_555, KOhA_555, BAI_502, BAI_502, MAhO_662, PA_672, MAI_661, \
		BAI_502, ME_574, BAI_502, BAI_502, PA_672, LI_566, MEhU_575, \
		MOI_663, KOhA_555, KOhA_555, COI_519, BIhI_507, KOhA_555, UI_612, \
		GOhA_543, PA_672, MOhE_664, MOhI_577, MAI_661, ZAhO_621, MOI_663, \
		PA_672, UI_612, NU_586, BAI_502, COI_519, BAI_502, BY_513 \
	)

	n_cmavo = ( \
		NA_578, BY_513, NAhE_583, UI_612, TAhE_604, NAhU_665, NAI_581, \
		CUhE_521, GOI_542, FAhA_528, UNK_M1, FAhA_528, VUhU_679, FAhA_528, \
		GOhA_543, NU_586, FAhA_528, NIhE_666, BAI_502, NIhO_584, PA_672, \
		PA_672, GOhA_543, NAhE_583, NIhO_584, PA_672, GOI_542, NOI_585, \
		NU_586, NUhA_667, COI_519, NUhI_587, CAhA_514, NUhU_588, BY_513 \
	)

	p_cmavo = ( \
		PA_672, BAI_502, UI_612, VUhU_679, FAhA_528, BAI_502, PA_672, \
		UI_612, GOI_542, UI_612, UNK_M1, UI_612, PEhO_673, COI_519, \
		CAI_515, PA_672, VUhU_679, PA_672, VUhU_679, BAI_502, JOI_548, \
		GOI_542, UNK_M1, GOI_542, BAI_502, UNK_M1, GOI_542, NOI_585, \
		PU_592, BAI_502, BAI_502, CAhA_514, ZAhO_621, NU_586, BY_513 \
	)

	r_cmavo = ( \
		KOhA_555, BAI_502, PA_672, BAI_502, RAhO_593, UI_612, BAI_502, \
		PA_672, PA_672, VUhU_679, UI_612, COI_519, FAhA_528, UNK_M1, \
		PA_672, KOhA_555, BAI_502, UI_612, BAI_502, VUhU_679, FAhA_528, \
		PA_672, UI_612, UI_612, UI_612, UI_612, UI_612, ROI_594, \
		KOhA_555, UI_612, CAI_515, TAhE_604, BY_513, FAhA_528, BY_513 \
	)

	s_cmavo = ( \
		SA_595, UI_612, UI_612, VUhU_679, VUhU_679, UI_612, CAI_515, \
		BAI_502, SE_596, UI_612, BY_513, UI_612, UI_612, SEhU_598, \
		SEI_597, SI_601, UI_612, MOI_663, VUhU_679, NU_586, BAI_502, \
		PA_672, PA_672, PA_672, PA_672, PA_672, PA_672, SOI_602, \
		SU_603, UI_612, PA_672, VUhU_679, PA_672, NU_586, BY_513 \
	)

	t_cmavo = ( \
		KOhA_555, COI_519, TAhE_604, BAI_502, UI_612, UI_612, BAI_502, \
		LAU_559, SE_596, VUhU_679, FAhA_528, UNK_M1, PA_672, TEhU_675, \
		TEI_605, KOhA_555, FAhA_528, UI_612, BAI_502, SEI_597, BAI_502, \
		TO_606, BY_513, NAhE_583, TO_606, FAhA_528, UI_612, TOI_607, \
		KOhA_555, LAhE_561, TUhE_610, BAI_502, PA_672, TUhU_611, BY_513 \
	)

	v_cmavo = ( \
		VA_613, VUhU_679, UNK_M1, UI_612, BAI_502, BAI_502, PA_672, \
		VAU_614, SE_596, VEhA_615, VEhA_615, VEhA_615, VEhO_678, VEhA_615, \
		VEI_677, VA_613, VIhA_616, VIhA_616, VIhA_616, COI_519, VIhA_616, \
		PA_672, KOhA_555, KOhA_555, KOhA_555, KOhA_555, KOhA_555, NOI_585, \
		VA_613, FAhA_528, UI_612, LAhE_561, UNK_M1, VUhU_679, BY_513 \
	)

	x_cmavo = ( \
		PA_672, XAI_M2, XAI_M2, XAI_M2, XAI_M2, XAI_M2, XAI_M2, \
		XAI_M2, SE_596, XAI_M2, XAI_M2, XAI_M2, XAI_M2, XAI_M2, \
		XAI_M2, XI_617, XAI_M2, XAI_M2, XAI_M2, XAI_M2, XAI_M2, \
		PA_672, XAI_M2, XAI_M2, XAI_M2, XAI_M2, XAI_M2, XAI_M2, \
		UI_612, XAI_M2, XAI_M2, XAI_M2, XAI_M2, XAI_M2, BY_513 \
	)

	z_cmavo = ( \
		ZI_624, UI_612, BAhE_503, NU_586, ZAhO_621, PA_672, LAU_559, \
		BAI_502, PA_672, ZEhA_622, ZEhA_622, ZEhA_622, FAhA_528, ZEhA_622, \
		ZEI_623, ZI_624, UNK_M1, ZIhE_625, UNK_M1, KOhA_555, UNK_M1, \
		ZO_626, FAhA_528, KOhA_555, FAhA_528, UI_612, ZOhU_628, ZOI_627, \
		ZI_624, FAhA_528, BAI_502, KOhA_555, NU_586, UI_612, BY_513 \
	)

	## This table is an index into the 18 preceding tables.
	##

	cmavo = ( \
		vowel_cmavo, b_cmavo, c_cmavo, \
		d_cmavo, f_cmavo, g_cmavo, \
		j_cmavo,  k_cmavo, \
		l_cmavo, m_cmavo, n_cmavo, \
		p_cmavo, r_cmavo, s_cmavo, \
		t_cmavo, v_cmavo, x_cmavo, \
		z_cmavo \
	)
# end class Constants:

#######################################################################
## Token
#######################################################################

class Token:
	"""
	Class Token is the token struct (defined in token.h).
	ttype is the type field of token struct (defined in token.h)
	(type is a reserved word in Python).
	nextn is the next field of token struct (defined in token.h)
	(next is a reserved word in Python).
	The rest are the same.

	Notes: 
		Function settype(tok, type) defined in token.c is ommited since the setter 
		function for ttype (type) property is performing the exact same fuctionality.

		Function add(parent, child) is implemented as an object (instance) method and not as a 
		class method (static).

		In C code types ptoken and YYSTYPE are defined as pointers to token struct.

	This class also implements all functions (except downcase) for printing a token 
	defined in print.c.
	Function downcase is not implemented since there is an Python intrinsic couterpart.
	"""
	def __init__(self, ttype = -1):
		if not isinstance(ttype, int):
			raise LojbanException(self, "ttype should be an int (is {:s})".format(ttype.__class__.__qualname__))
		# end if not isinstance(ttype, int):
		self._ttype = ttype
		self._text = None
		self._up = None
		self._right = None
		self._downright = None
		self._downleft = None
		self._nextn = None
	# end def __init__(self):

	def __str__(self):
		return self.tostr()
	# end def __str__(self):
	
	def ___repr__(self):
		return self.__str__()
	# end def ___repr__(self):

	def tostr(self, endline = False, singlemode = False, maxline = 75):
		sysstdout = sys.stdout
		buffer = StringIO()
		sys.stdout = buffer
		self.print(self, endline = False, singlemode = False, maxline = 75)
		sys.stdout = sysstdout
		return buffer.getvalue()
	# end def tostr(self, endline = False, singlemode = False, maxline = 75):

	@property
	def ttype(self):
		return self._ttype
	# end def ttype(self):
	
	@ttype.setter
	def ttype(self, v):
		if v and not isinstance(v, int):
			raise LojbanException(self, "ttype should be an int (is {:s})".format(v.__class__.__qualname__))
		# end if v and not isinstance(v, int):
		self._ttype = v
	# end def ttype(self, v):

	@property
	def text(self):
		return self._text
	# end def text(self):
	
	@text.setter
	def text(self, v):
		if v and not isinstance(v, str):
			raise LojbanException(self, "text should be a string (is {:s})".format(v.__class__.__qualname__))
		# end if v and not isinstance(v, str):
		self._text = v
	# end def text(self, v):	

	@property
	def up(self):
		return self._up
	# end def up(self):
	
	@up.setter
	def up(self, v):
		if not v:
			self._up = None
		elif isinstance(v, Token):
			self._up = weakref.ref(v)
		elif (v.__class__.__qualname__ == "ReferenceType" or v.__class__.__qualname__ == "weakref") and isinstance(v(), Token):
			self._up = v
		else:
			raise LojbanException(self, "Argument should be a Token" + \
				" or a weak reference to Token or None"+\
				" (is {:s} {:s})".format(v.__class__.__qualname__, \
					"" if (v.__class__.__qualname__ != "ReferenceType" and v.__class__.__qualname__ != "weakref") else \
					v().__class__.__qualname__))
		# end if 
	# end def up(self, v):

	@property
	def right(self):
		return self._right
	# end def right(self):
	
	@right.setter
	def right(self, v):
		if not v:
			self._right = None
		elif isinstance(v, Token):
			self._right = weakref.ref(v)
		elif (v.__class__.__qualname__ == "ReferenceType" or v.__class__.__qualname__ == "weakref") and isinstance(v(), Token):
			self._right = v
		else:
			raise LojbanException(self, "Argument should be a Token" + \
				" or a weak reference to Token or None"+\
				" (is {:s} {:s})".format(v.__class__.__qualname__, \
					"" if (v.__class__.__qualname__ != "ReferenceType" and v.__class__.__qualname__ != "weakref") else \
					v().__class__.__qualname__))
		# end if 
	# end def right(self, v):

	@property
	def downright(self):
		return self._downright
	# end def downright(self):
	
	@downright.setter
	def downright(self, v):
		if not v:
			self._downright = None
		elif isinstance(v, Token):
			self._downright = weakref.ref(v)
		elif (v.__class__.__qualname__ == "ReferenceType" or v.__class__.__qualname__ == "weakref") and isinstance(v(), Token):
			self._downright = v
		else:
			raise LojbanException(self, "Argument should be a Token" + \
				" or a weak reference to Token or None"+\
				" (is {:s} {:s})".format(v.__class__.__qualname__, \
					"" if (v.__class__.__qualname__ != "ReferenceType" and v.__class__.__qualname__ != "weakref") else \
					v().__class__.__qualname__))
		# end if 
	# end def downright(self, v):

	@property
	def downleft(self):
		return self._downleft
	# end def downleft(self):
	
	@downleft.setter
	def downleft(self, v):
		if not v:
			self._downleft = None
		elif isinstance(v, Token):
			self._downleft = weakref.ref(v)
		elif (v.__class__.__qualname__ == "ReferenceType" or v.__class__.__qualname__ == "weakref") and isinstance(v(), Token):
			self._downleft = v
		else:
			raise LojbanException(self, "Argument should be a Token" + \
				" or a weak reference to Token or None"+\
				" (is {:s} {:s})".format(v.__class__.__qualname__, \
					"" if (v.__class__.__qualname__ != "ReferenceType" and v.__class__.__qualname__ != "weakref") else \
					v().__class__.__qualname__))
		# end if 
	# end def downleft(self, v):

	@property
	def nextn(self):
		return self._nextn
	# end def nextn(self):
	
	@nextn.setter
	def nextn(self, v):
		if not v:
			self._nextn = None
		elif isinstance(v, Token):
			self._nextn = weakref.ref(v)
		elif (v.__class__.__qualname__ == "ReferenceType" or v.__class__.__qualname__ == "weakref") and isinstance(v(), Token):
			self._nextn = v
		else:
			raise LojbanException(self, "Argument should be a Token" + \
				" or a weak reference to Token or None"+\
				" (is {:s} {:s})".format(v.__class__.__qualname__, \
					"" if (v.__class__.__qualname__ != "ReferenceType" and v.__class__.__qualname__ != "weakref") else \
					v().__class__.__qualname__))
		# end if 
	# end def nextn(self, v):

	def add(parent, child):
		"""
		Adds a child node to parent node.
		"""
		if child and ((child.__class__.__qualname__ != "ReferenceType" and child.__class__.__qualname__ != "weakref") or \
			not isinstance(child(), Token)):
			raise LojbanException(LojbanParser(), "Argument should be" + \
				" a weak reference to childen or None"+\
				" (is {:s} {:s})".format(child.__class__.__qualname__, \
					"" if (child.__class__.__qualname__ != "ReferenceType" and child.__class__.__qualname__ != "weakref") else \
					child().__class__.__qualname__))
		# end if 
		if child is None:
			return
		# end if child is None:
		child().up = parent
		if parent.downleft:
			parent.downright().right = child
		else: # if parent.downleft:
			parent.downleft = child
		# end if not parent.downleft is None:
		parent.downright = child
	# end def add(parent, child):

	#
	# methods for printing a Token (from print.c)
	#

	@staticmethod
	def print(tok, endline = True, singlemode = False, maxline = 75): 
		"""
		Prints a tree of tokens.
		print is a intrinsic Python function thus renamed.
		"""
		def _print1(tok):
			"""
			Traverses and prints a tree of tokens.
			"""
			if tok and not isinstance(tok, Token):
				raise LojbanException(Token(), "Argument should be a Token (is {:s}).".format(tok.__class__.__qualname__))
			# end if tok and not isinstance(tok, Token):
			_LDELIM = "({<["
			_RDELIM = ")}>]"

			tail_recursion = True
			while tail_recursion:
				tail_recursion = False
				if tok is None:
					Token.print._column += 4
					if Token.print._column >= Token.print._maxline:
						print()
						Token.print._column = 4
					# end if Token.print._column >= Token.print._maxline:
					print("NULL", end = "")
				elif tok.ttype == 0:
					Token.print._column += 3
					if Token.print._column >= Token.print._maxline:
						print()
						Token.print._column = 3
					# end if Token.print._column >= Token.print._maxline:
					print("EOT", end = "")
				elif tok.text:
					Token.print._column += len(tok.text)
					if Token.print._column >= Token.print._maxline:
						print()
						Token.print._column = len(tok.text)
					# end if Token.print._column >= Token.print._maxline:
					print("{:s}".format(tok.text), end = "") 
				elif not tok.downleft:
					Token.print._column += 2
					if Token.print._column >= Token.print._maxline:
						print()
						Token.print._column = 2
					# end if Token.print._column >= Token.print._maxline:
					print("()", end = "")
				elif (not Token.print._singlemode and not tok.downleft().right):
					tok = tok.downleft()
					tail_recursion = True
				else:
					p = tok.downleft
					while not p is None:
						Token.print._column += 1
						if Token.print._column >= Token.print._maxline:
							print()
							Token.print._column = 1
						# end if Token.print._column >= Token.print._maxline:
						d = " "
						if p() == tok.downleft():
							d = _LDELIM[Token.print._level & 3]
							Token.print._level += 1
						# end if p() == tok.downleft():
						print("{:s}".format(d), end = "")
						_print1(p())
						p = p().right
					# end while not p is None:
					Token.print._column += 1
					if Token.print._column >= Token.print._maxline:
						print()
						Token.print._column = 1
					# end if Token.print._column >= Token.print._maxline:
					Token.print._level -= 1
					print("{:s}".format(_RDELIM[Token.print._level & 3]), end = "")
				# end if 
			# end while tail_recursion:
		# end def print1(tok):

		if tok and not isinstance(tok, Token):
			raise LojbanException(Token(), "Argument should be a Token (is {:s}).".format(tok.__class__.__qualname__))
		# end if tok and not isinstance(tok, Token):

		if not getattr(Token.print, "_level", None):
			Token.print._level = 0
		# end if not getattr(Token.print, "_level", None):
		if not getattr(Token.print, "_column", None):
			Token.print._column = 0
		# end if not getattr(Token.print, "_column", None):
		if not getattr(Token.print, "_singlemode", None):
			Token.print._singlemode = False
		# end if not getattr(Token.print, "_singlemode", None):
		if not getattr(Token.print, "_maxline", None):
			Token.print._maxline = 75
		# end if not getattr(Token.print, "_maxline", None):

		Token.print._singlemode = singlemode
		Token.print._maxline = maxline
		if Token.print._maxline < 1:
			Token.print._maxline = sys.maxsize
		# end if Token.print._maxline < 1:
		Token.print._level = 0
		Token.print._column = 0
		_print1(tok)
		if endline:
			print()
		# end if endline:
	# end def print(self, tok):
		
	@staticmethod
	def rprint(tok, endline = True, singlemode = False, maxline = 75):
		"""
		Reverse prints of a token tree.
		"""
		def _prologize(p):
			"""
			Replaces single quotes and non alphanumeric characters with underscores.
			"""
			if p is None:
				return None
			# end if p is None:
			r = ""
			for c in p:
				if c == "'":
					r += "h"
				elif not c.isalnum():
					r += "_"
				else:
					r += c
				# end if
			# end for c in p:
			return r
		# end def _prologize(p):

		def _rprint1(tok):
			"""
			Traverses in reverse order and prints of a token tree.
			"""
			if tok and not isinstance(tok, Token):
				raise LojbanException(Token(), "Argument should be a Token (is {:s}).".format(tok.__class__.__qualname__))
			# end if tok and not isinstance(tok, Token):

			tail_recursion = True
			while tail_recursion:
				tail_recursion = False
				if tok and tok.ttype != 0:
					rule = Constants.rulename(tok.ttype)
				else:
					rule = None
				# end if
				_prologize(rule)

				if tok is None:
					Token.rprint._column += 4
					if Token.rprint._column >= Token.rprint._maxline:
						print()
						Token.rprint._column = 4
					# end if Token.rprint._column >= Token.rprint._maxline:
					print("NULL", end = "")
				elif tok.ttype == 0:
					Token.rprint._column += 3
					if Token.rprint._column >= Token.rprint._maxline:
						print()
						Token.rprint._column = 3
					# end if Token.rprint._column >= Token.rprint._maxline:
					print("EOT", end = "")
				elif not tok.text is None:
					Token.rprint._column += len(rule) + len(tok.text) + 2
					if Token.rprint._column >= Token.rprint._maxline:
						print()
						Token.rprint._column = len(rule) + len(tok.text) + 2
					# end if Token.rprint._column >= Token.rprint._maxline:
					_prologize(tok.text)
					print("{:s}({:s})".format(rule, tok.text.lower()), end = "")
				elif tok.downleft is None:
					Token.rprint._column += len(rule) + 2
					if Token.rprint._column >= Token.rprint._maxline:
						print()
						Token.rprint._column = len(rule) + 2
					# end if Token.rprint._column >= Token.rprint._maxline:
					print("{:s}()".format(rule), end = "")
				elif not Token.rprint._singlemode and tok.downleft().right is None:
					tok = tok.downleft()
					tail_recursion = True
				else:
					Token.rprint._column += len(rule)
					if Token.rprint._column >= Token.rprint._maxline:
						print()
						Token.rprint._column = len(rule)
					# end if Token.rprint._column >= Token.rprint._maxline:
					print("{:s}".format(rule), end = "")
					p = tok.downleft
					while not p is None:
						Token.rprint._column += 1
						if Token.rprint._column >= Token.rprint._maxline:
							print()
							Token.rprint._column = 1
						# end if Token.rprint._column >= Token.rprint._maxline:
						print("{:s}".format('(' if p == tok.downleft else ','), end = "")
						_rprint1(p())
						p = p().right
					# end while not p is None:
					Token.rprint._column += 1
					if Token.rprint._column >= Token.rprint._maxline:
						print()
						Token.rprint._column = 1
					# end if Token.rprint._column >= Token.rprint._maxline:
					print(")", end = "")
				# end if
			# end while tail_recursion:
		# end def _rprint1(self, tok):

		if tok and not isinstance(tok, Token):
			raise LojbanException(Token(), "Argument should be a Token (is {:s}).".format(tok.__class__.__qualname__))
		# end if tok and not isinstance(tok, Token):

		if not getattr(Token.rprint, "_column", None):
			Token.rprint._column = 0
		# end if not getattr(Token.rprint, "_column", None):
		if not getattr(Token.rprint, "_singlemode", None):
			Token.rprint._singlemode = False
		# end if not getattr(Token.rprint, "_singlemode", None):
		if not getattr(Token.rprint, "_maxline", None):
			Token.rprint._maxline = 75
		# end if not getattr(Token.rprint, "_maxline", None):
		Token.rprint._singlemode = singlemode
		Token.rprint._maxline = maxline

		Token.rprint._column = 0
		_rprint1(tok)
		if endline:
			print(".")
		else: # if endline:
			print(".", end = "")
		# end if endline:
	# end def rprint(self, tok):

	@staticmethod
	def tprint(tok):
		"""
		Prints a tree of tokens
		"""
		def _tree1(tok):
			"""
			Recursively prints a tree of tokens.
			"""
			if not isinstance(tok, Token):
				raise LojbanException(Token(), "Argument should be a Token (is {:s}).".format(tok.__class__.__qualname__))
			# end if isinstance(tok, Token):
			child = tok.downleft
			while not child is None:
				_tree1(child())
				child = child().right
			# end while not child is None:
			name = Constants.rulename(tok.ttype) if not tok.ttype is None else None
			atype = tok.ttype
			# # Note: the following code is enclosed in a if 0 directive thus not executed
			# # Not executed code start
			# # if 0
			# if not tok.downleft is None and tok.downleft.right is None:
			#	tok.ttype = tok.downleft.ttype
			#	return
			# # end if not tok.downleft is None and tok.downleft.right is None:
			# # endif
			# # Not executed code end
			Token.tprint._magic += 1
			tok.ttype = Token.tprint._magic
			print("{:s}\t{:s}".format(str(tok.ttype), str(name)), end = "")
			if tok.text:
				print("\t{:s}".format(tok.text), end = "")
			else:
				child = tok.downleft
				while not child is None:
					print("\t{:s}".format(str(child().ttype)), end = "")
					child = child().right
				# end while not child is None:
			# end if
			print()
		# end def _tree1(self, tok):

		if tok is None:
			print("NULL")
			return
		# end if tok is None:
		if not isinstance(tok, Token):
			raise LojbanException(Token(), "Argument should be a Token (is {:s}).".format(tok.__class__.__qualname__))
		# end if isinstance(tok, Token):
		if not getattr(Token.tprint, "_magic", None):
			Token.tprint._magic = 0
		# end if not getattr(Token._print1, "_level", None):
		Token.tprint._magic = 0
		_tree1(tok)
	# end def tprint(self, tok):
# end class Token:

#######################################################################
## LojbanParser
#######################################################################

class LojbanParser:
	"""
	This class implements all the logic of the parser.
	"""
	def __init__(self, parameters = Parameters()):
		self._parameters = parameters
		self.reset()
	# end def __init__(self, ...):

	def __str__(self):
		return "LojbanParser with " + self._parameters
	# end def __str__(self):

	def __repr__(self):
		return self.__str__()
	# end def __repr__(self):

	@property
	def rulemode(self):
		return self._parameters.rulemode
	# end def rulemode(self):

	@property
	def stringspace(self):
		return self._stringspace
	# end def stringspace(self):

	@property
	def tokspace(self):
		return self._tokspace
	# end def tokspace(self):
	
	@property
	def treemode(self):
		return self._parameters.treemode
	# end def treemode(self):

	_VERSION = "233"

	@staticmethod
	def _mkcmavo():
		"""
		Utility method for showing cmavo.
		It is not called during parsing, it is called only from main,
		on user request.
		"""
		cc = (".", "b", "c", "d", "f", "g", "j", "k", "l", "m", "n", \
					"p", "r", "s", "t", "v", "x", "z")

		vc = ( \
			"a", "a'a", "a'e", "a'i", "a'o", "a'u", "ai", "au", "e", "e'a", \
			"e'e", "e'i", "e'o", "e'u", "ei", "i", "i'a", "i'e", "i'i", "i'o", \
			"i'u", "o", "o'a", "o'e", "o'i", "o'o", "o'u", "oi", "u", "u'a", \
			"u'e", "u'i", "u'o", "u'u", "y", "ia", "ie", "ii", "io", "iu", \
			"ua", "ue", "ui", "uo", "uu", "y'y" \
		)

		idx = 0
		for i in range(len(cc)):
			jmax = 35 if i != 0 else len(vc)
			for j in range(jmax):
				t = Constants.cmavo[i][j]
				if t >= 0:
					rule = Constants.rulename(t)
					try:
						apos = rule.index("'")
						rule = rule[:apos] + 'h' + rule[apos+1:]
					except Exception as e:
						pass
					# end try except Exception as e:
					idx += 1
					print("{:0>3d}:({:0>2d}-{:0>2d}): {:1s}{:<8} {:<8}".format(idx, i, j, cc[i], vc[j], rule))
				# end if t >= 0:
			# end for j in range(jmax):
		# end for i in range(len(cc)):
	# end def _mkcmavo():
	
	def _absorb(self):
		"""
		This method does indicator processing.  It invokes lerfu() and does
		1-token lookahead to watch for following indicators.  If found, they
		are absorbed into the previous token.  Indicators belong to selmao
		UI, CAI, Y, DAhO, FUhE, or FUhO.  UI and CAI can also have a
		following NAI, which is checked for and absorbed as well.
		"""
		if not getattr(LojbanParser._absorb, "_cache", None):
			LojbanParser._absorb._cache = None
		# end if not getattr(LojbanParser._absorb, "_cache", None):

		tok = LojbanParser._absorb._cache if LojbanParser._absorb._cache else self._lerfu()

		if tok().ttype == 0:
			return tok
		# end if tok().ttype == 0:
		result = None
		LojbanParser._absorb._cache = self._lerfu()
		while Constants.isindicator(LojbanParser._absorb._cache):
			if LojbanParser._absorb._cache().ttype == Constants.NAI_581:
				if result is None:
					break
				# end if result:
				lasttype = result().downright().ttype
				if lasttype != Constants.UI_612 and lasttype != Constants.CAI_515:
					break
				# end if lasttype != Constants.UI_612 and lasttype != Constants.CAI_515:
			# end if LojbanParser._absorb._cache().ttype == Constants.NAI_581:
			if result is None:
				result = self._newtoken()
				result().ttype = tok().ttype
				result().add(tok)
			# end if result is None:
			result().add(LojbanParser._absorb._cache)
			LojbanParser._absorb._cache = self._lerfu()
		# end while Constants.isindicator(LojbanParser._absorb._cache):
		if result:
			return result
		# end if result:
		return tok
	# end def _absorb(self):

	def _BIhI_root_932(self):
		ttype = 932
		tok = self._BIhI_root_932_2()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._BIhI_root_932_1()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._BIhI_root_932_4()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._BIhI_root_932_3()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _BIhI_root_932(self):

	def _BIhI_root_932_1(self):
		result = self._newtoken()
		tok = self._isnext(Constants.BIhI_507, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _BIhI_root_932_1(self):

	def _BIhI_root_932_2(self):
		result = self._newtoken()
		tok = self._isnext(Constants.BIhI_507, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.NAI_581, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _BIhI_root_932_2(self):

	def _BIhI_root_932_3(self):
		result = self._newtoken()
		tok = self._isnext(Constants.SE_596, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.BIhI_507, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _BIhI_root_932_3(self):

	def _BIhI_root_932_4(self):
		result = self._newtoken()
		tok = self._isnext(Constants.SE_596, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.BIhI_507, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.NAI_581, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _BIhI_root_932_4(self):

	def _cmenecheck(self, p, bad):
		"""
		Reports invalidity of cmene.
		"""
		badlen = len(bad);
		plen = len(p);

		ipos = 0;
		while (ipos < plen):
			ifpos = LojbanParser._strchr(p[ipos:], bad[0]);
			if ifpos is None:
				return;
			# end if ifpos is None:
			if p[(ipos + ifpos + 1) : (ipos + ifpos + badlen)] == bad[1:]:
				break;
			# end if p[(ipos + ifpos + 1) : (ipos + ifpos + badlen)] == bad[1:]:
			ipos += 1
		# end while (ipos < plen):
		if ifpos is None or ipos == plen:
			return;
		# end if ifpos is None or ipos == plen:
		if ifpos == 0 or Constants.isV(p[ipos + ifpos - 1]):
			print("Illegal cmene {:s} at line {:d}, column {:d}: contains {:s}".format(p, self._line, self._column, bad))
		# end if ifpos == 0 or isV(p[ipos + ifpos - 1]):
	# end def _cmenecheck(p, bad):

	def _compound(self):
		"""
		Invokes the lexer rule drivers to try to make compounds.
		If all of them fail, it calls gettoken() and returns it.
		The ordering constraints needed for
		recursive-descent compounding is the longest first.
		Note: Definition of TEST replaced with resulting code.
		"""
		tok = self._gettoken()
		toktype = tok().ttype
		self._fail(tok)
		if toktype == Constants.A_501:
			tok = self._lexer_C_915_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_D_916_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_B_910_driver()
			if tok:
				return tok
			# end if tok:
		elif toktype == Constants.BAI_502:
			tok = self._lexer_G_935_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_O_970_driver()
			if tok:
				return tok
			# end if tok:
		elif toktype == Constants.BIhI_507:
			tok = self._lexer_G_935_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_V_1010_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_W_1015_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_F_930_driver()
			if tok:
				return tok
			# end if tok:
		elif toktype == Constants.BY_513:
			tok = self._lexer_A_905_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_Y_1025_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_Q_985_driver()
			if tok:
				return tok
			# end if tok:
		elif toktype == Constants.CAhA_514:
			tok = self._lexer_G_935_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_O_970_driver()
			if tok:
				return tok
			# end if tok:
		elif toktype == Constants.CUhE_521:
			tok = self._lexer_G_935_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_O_970_driver()
			if tok:
				return tok
			# end if tok:
		elif toktype == Constants.FAhA_528:
			tok = self._lexer_G_935_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_O_970_driver()
			if tok:
				return tok
			# end if tok:
		elif toktype == Constants.FEhE_530:
			tok = self._lexer_G_935_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_O_970_driver()
			if tok:
				return tok
			# end if tok:
		elif toktype == Constants.GA_537:
			tok = self._lexer_G_935_driver()
			if tok:
				return tok
			# end if tok:
		elif toktype == Constants.GI_539:
			tok = self._lexer_P_980_driver()
			if tok:
				return tok
			# end if tok:
		elif toktype == Constants.GIhA_541:
			tok = self._lexer_M_965_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_N_966_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_R_990_driver()
			if tok:
				return tok
			# end if tok:
		elif toktype == Constants.GUhA_544:
			tok = self._lexer_H_940_driver()
			if tok:
				return tok
			# end if tok:
		elif toktype == Constants.I_545:
			tok = self._lexer_K_955_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_S_995_driver()
			if tok:
				return tok
			# end if tok:
		elif toktype == Constants.JA_546:
			tok = self._lexer_U_1005_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_E_925_driver()
			if tok:
				return tok
			# end if tok:
		elif toktype == Constants.JOI_548:
			tok = self._lexer_G_935_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_V_1010_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_W_1015_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_F_930_driver()
			if tok:
				return tok
			# end if tok:
		elif toktype == Constants.KI_554:
			tok = self._lexer_G_935_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_O_970_driver()
			if tok:
				return tok
			# end if tok:
		elif toktype == Constants.LAU_559:
			tok = self._lexer_A_905_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_Y_1025_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_Q_985_driver()
			if tok:
				return tok
			# end if tok:
		elif toktype == Constants.MOhI_577:
			tok = self._lexer_G_935_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_O_970_driver()
			if tok:
				return tok
			# end if tok:
		elif toktype == Constants.NA_578:
			tok = self._lexer_C_915_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_D_916_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_B_910_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_U_1005_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_E_925_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_J_950_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_M_965_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_N_966_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_R_990_driver()
			if tok:
				return tok
			# end if tok:
		elif toktype == Constants.NAhE_583:
			tok = self._lexer_I_945_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_G_935_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_O_970_driver()
			if tok:
				return tok
			# end if tok:
		elif toktype == Constants.PU_592:
			tok = self._lexer_G_935_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_O_970_driver()
			if tok:
				return tok
			# end if tok:
		elif toktype == Constants.SE_596:
			tok = self._lexer_C_915_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_D_916_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_B_910_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_U_1005_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_E_925_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_H_940_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_M_965_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_N_966_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_G_935_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_O_970_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_V_1010_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_W_1015_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_F_930_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_R_990_driver()
			if tok:
				return tok
			# end if tok:
		elif toktype == Constants.TAhE_604:
			tok = self._lexer_G_935_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_O_970_driver()
			if tok:
				return tok
			# end if tok:
		elif toktype == Constants.TEI_605:
			tok = self._lexer_A_905_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_Y_1025_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_Q_985_driver()
			if tok:
				return tok
			# end if tok:
		elif toktype == Constants.VA_613:
			tok = self._lexer_G_935_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_O_970_driver()
			if tok:
				return tok
			# end if tok:
		elif toktype == Constants.VEhA_615:
			tok = self._lexer_G_935_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_O_970_driver()
			if tok:
				return tok
			# end if tok:
		elif toktype == Constants.VIhA_616:
			tok = self._lexer_G_935_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_O_970_driver()
			if tok:
				return tok
			# end if tok:
		elif toktype == Constants.ZAhO_621:
			tok = self._lexer_G_935_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_O_970_driver()
			if tok:
				return tok
			# end if tok:
		elif toktype == Constants.ZEhA_622:
			tok = self._lexer_G_935_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_O_970_driver()
			if tok:
				return tok
			# end if tok:
		elif toktype == Constants.ZI_624:
			tok = self._lexer_G_935_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_O_970_driver()
			if tok:
				return tok
			# end if tok:
		elif toktype == Constants.GAhO_656:
			tok = self._lexer_G_935_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_V_1010_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_W_1015_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_F_930_driver()
			if tok:
				return tok
			# end if tok:
		elif toktype == Constants.PA_672:
			tok = self._lexer_A_905_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_Y_1025_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_O_970_driver()
			if tok:
				return tok
			# end if tok:
			tok = self._lexer_L_960_driver()
			if tok:
				return tok
			# end if tok:
		# end if

		rettok = self._gettoken()
		return rettok
	# end def _compound(self):

	def _copyright(self):
		print("Transcripted in Python: Based on " + \
			 "25{:s} moi ke lojbo genturfa'i".format(LojbanParser._VERSION[1:]))
		print("Copyright 1991,1992,1993 The Logical Languages Group, Inc." + \
			"  All Rights Reserved")
	# end def _copyright(self):

	def _cpd_reduce(self, tok, ttype):
		"""
		cpd_reduce(result, type) does a settype() and outputs debugging info.
		"""
		if tok:
			tok().ttype = ttype
			if self._parameters.D_cpd_reduce:
				print("compounder reduced {:s}".format(Constants.rulename(ttype)))
			# end if self._parameters.D_cpd_reduce:
		# end if tok:
		return tok
	# end def _cpd_reduce(self, tok, type):

	def _destroy(self, tok):
		"""
		Destroys (removes) a token from the list.
		Releases a token to the freelist.
		"""
		tok().nextn = self._freelist
		self._freelist = tok
	# end _def destroy(self, tok):

	def _EK_root_911(self):
		ttype = 911
		tok = self._EK_root_911_4()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._EK_root_911_5()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._EK_root_911_6()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._EK_root_911_8()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._EK_root_911_1()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._EK_root_911_2()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._EK_root_911_3()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._EK_root_911_7()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _EK_root_911(self):

	def _EK_root_911_1(self):
		result = self._newtoken()
		tok = self._isnext(Constants.A_501, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _EK_root_911_1(self):

	def _EK_root_911_2(self):
		result = self._newtoken()
		tok = self._isnext(Constants.SE_596, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.A_501, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _EK_root_911_2(self):

	def _EK_root_911_3(self):
		result = self._newtoken()
		tok = self._isnext(Constants.NA_578, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.A_501, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _EK_root_911_3(self):

	def _EK_root_911_4(self):
		result = self._newtoken()
		tok = self._isnext(Constants.A_501, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.NAI_581, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _EK_root_911_4(self):

	def _EK_root_911_5(self):
		result = self._newtoken()
		tok = self._isnext(Constants.SE_596, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.A_501, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.NAI_581, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _EK_root_911_5(self):

	def _EK_root_911_6(self):
		result = self._newtoken()
		tok = self._isnext(Constants.NA_578, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.A_501, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.NAI_581, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _EK_root_911_6(self):

	def _EK_root_911_7(self):
		result = self._newtoken()
		tok = self._isnext(Constants.NA_578, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.SE_596, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.A_501, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _EK_root_911_7(self):

	def _EK_root_911_8(self):
		result = self._newtoken()
		tok = self._isnext(Constants.NA_578, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.SE_596, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.A_501, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.NAI_581, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _EK_root_911_8(self):

	def _elidable(self, t):
		"""
		elidable(t) returns an elidable terminator of the specified type t.
		Note: we hack the parser skeleton to YYABORT on real errors (which are known
		because the parser state stack self._needs popping) before getting here.
		"""
		if self._parameters.elidemode:
			return None
		# end if self._parameters.elidemode:
		result = self._newtoken()
		result().ttype = t
		result().text = Constants.rulename(t)
		if self._parameters.D_elidable:
			print("inserting elided {:s} ({:d})".format(result().text, result().ttype))
		# end if self._parameters.D_elidable:
		return result
	# end def _elidable(self, t):

	def _event_mod_1052(self):
		ttype = 1052
		tok = self._event_mod_1052_2()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._event_mod_1052_1()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _event_mod_1052(self):

	def _event_mod_1052_1(self):
		result = self._newtoken()
		tok = self._event_mod_A_1053()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _event_mod_1052_1(self):

	def _event_mod_1052_2(self):
		result = self._newtoken()
		tok = self._event_mod_A_1053()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._event_mod_1052()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _event_mod_1052_2(self):

	def _event_mod_A_1053(self):
		ttype = 1053
		tok = self._event_mod_A_1053_4()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._event_mod_A_1053_3()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._event_mod_A_1053_2()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._event_mod_A_1053_1()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _event_mod_A_1053(self):

	def _event_mod_A_1053_1(self):
		result = self._newtoken()
		tok = self._isnext(Constants.ZAhO_621, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _event_mod_A_1053_1(self):

	def _event_mod_A_1053_2(self):
		result = self._newtoken()
		tok = self._isnext(Constants.ZAhO_621, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.NAI_581, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _event_mod_A_1053_2(self):

	def _event_mod_A_1053_3(self):
		result = self._newtoken()
		tok = self._isnext(Constants.ZAhO_621, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._interval_property_1051()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _event_mod_A_1053_3(self):

	def _event_mod_A_1053_4(self):
		result = self._newtoken()
		tok = self._isnext(Constants.ZAhO_621, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.NAI_581, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._interval_property_1051()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _event_mod_A_1053_4(self):

	def _fabsorb(self):
		"""
		This method does absorption of forethought indicators.
		It invokes glue() and watches for BAhE tokens.
		If found, the next token is read and the BAhE is absorbed
		into it, passing up the type of the following token as the 
		type of the compound.
		"""
		tok = self._glue()
		if tok().ttype == Constants.BAhE_503:
			absorber = self._fabsorb()
			if absorber().ttype == 0:
				return tok
			# end if absorber.ttype == 0:
			result = self._newtoken()
			result().add(tok)
			result().add(absorber)
			result().ttype = absorber().ttype
			return result
		# end if tok().ttype == Constants.BAhE_503:
		return tok
	# end def _fabsorb(self):

	def _fail(self, tok):
		"""
		fail(tok) is used to cause backtracking failure.  
		The argument, tok, is scanned recursively, and all selmao-level tokens are 
		pushed onto the front of the self._pushback queue (preserving their order).  
		Fail() returns None.
		"""
		self._head = self._tail = None
		self._release(tok)
		if self._head:
			self._tail().nextn = self._pushback
			self._pushback = self._head
		# end if not self._head is None:
		return None
	# end def _fail(self, tok):

	def _filter(self):
		"""
		This method does filtering, removing non-parsable quoted material.
		It invokes lex() and passes everything through unchanged unless it involves
		"zo", "zoi", "la'o", "lo'u", or "le'u".
		"""
		_NORMAL_MODE = 0
		_ZO_MODE = 1
		_ZOI_START_MODE = 2
		_ZOI_STRING_MODE = 3
		_ZOI_END_MODE = 4
		_LOhU_MODE = 5
		_LEhU_MODE = 6
		if not getattr(LojbanParser._filter, "_tok", None):
			LojbanParser._filter._tok = None
		# end if not getattr(LojbanParser._filter, "_tok", None):
		if not getattr(LojbanParser._filter, "_delim", None):
			LojbanParser._filter._delim = None
		# end if not getattr(LojbanParser._filter, "_delim", None):
		if not getattr(LojbanParser._filter, "_mode", None):
			LojbanParser._filter._mode = _NORMAL_MODE
		# end if not getattr(LojbanParser._filter, "_mode", None):

		if LojbanParser._filter._mode == _NORMAL_MODE:
			LojbanParser._filter._tok = self._lex()
			if LojbanParser._filter._tok().ttype == 0:
				return LojbanParser._filter._tok
			if (LojbanParser._filter._tok().text == "zo"):
				LojbanParser._filter._mode = _ZO_MODE
			elif (LojbanParser._filter._tok().text == "zoi"):
				LojbanParser._filter._mode = _ZOI_START_MODE
			elif (LojbanParser._filter._tok().text == "la'o"):
				LojbanParser._filter._mode = _ZOI_START_MODE
			elif (LojbanParser._filter._tok().text == "lo'u"):
				LojbanParser._filter._mode = _LOhU_MODE
			return LojbanParser._filter._tok
		elif LojbanParser._filter._mode == _ZO_MODE:
			LojbanParser._filter._tok = self._lex()
			if LojbanParser._filter._tok().ttype == 0:
				return LojbanParser._filter._tok
			LojbanParser._filter._tok().ttype = Constants.any_word_698
			LojbanParser._filter._mode = _NORMAL_MODE
			return LojbanParser._filter._tok
		elif LojbanParser._filter._mode == _ZOI_START_MODE:
			LojbanParser._filter._tok = self._lex()
			if LojbanParser._filter._tok().ttype == 0:
				return LojbanParser._filter._tok
			LojbanParser._filter._tok().ttype = Constants.any_word_698
			LojbanParser._filter._mode = _ZOI_STRING_MODE
			LojbanParser._filter._delim = LojbanParser._filter._tok
			return LojbanParser._filter._tok
		elif LojbanParser._filter._mode == _ZOI_STRING_MODE:
			result = self._newtoken()
			result().ttype = Constants.anything_699
			while True:
				LojbanParser._filter._tok = self._lex()
				if LojbanParser._filter._tok().ttype == 0:
					return LojbanParser._filter._tok
				if LojbanParser._filter._tok().text == LojbanParser._filter._delim().text:
					break
				LojbanParser._filter._tok().ttype = -1
				result().add(LojbanParser._filter._tok)
			# end while True:
			LojbanParser._filter._mode = _ZOI_END_MODE
			return result
		elif LojbanParser._filter._mode == _ZOI_END_MODE:
			# note: LojbanParser._filter._token has already been read 
			LojbanParser._filter._tok().ttype = Constants.any_word_698
			LojbanParser._filter._mode = _NORMAL_MODE
			return LojbanParser._filter._tok
		elif LojbanParser._filter._mode == _LOhU_MODE:
			result = self._newtoken()
			result().ttype = Constants.any_words_697
			zo = False
			while True:
				LojbanParser._filter._tok = self._lex()
				if LojbanParser._filter._tok().ttype == 0:
					return LojbanParser._filter._tok
				if (not zo and LojbanParser._filter._tok().text == "le'u"):
					break
				zo = (LojbanParser._filter._tok().text == "zo")
				LojbanParser._filter._tok().ttype = -1
				result().add(LojbanParser._filter._tok)
			# end while True:
			LojbanParser._filter._mode = _LEhU_MODE
			return result
		elif LojbanParser._filter._mode == _LEhU_MODE:
			# note: LojbanParser._filter._token has already been read 
			LojbanParser._filter._mode = _NORMAL_MODE
			return LojbanParser._filter._tok
		# NOTREACHED
		raise LojbanException(self,\
			"FATAL ERROR: Reached invalid code")
	# end def _filter(self):

	def _getword(self):
		"""
		This method picks words out of the standard input stream.  It treats
		whitespace and "." as word separators, mashes upper case to lower case,
		converts digits to appropriate cmavo, and blows away all else.   Text between
		slashes is treated as comments (possibly English translations) and discarded.

		Getword returns a pointer to a static buffer which will be overwritten by
		successive calls, or else NULL (which means end of file).
		Line and column numbers are tracked for error recovery.
		Getword remembers EOF on input and does not re-examine the input stream.
		"""
		_digits = ("no", "pa", "re", "ci", "vo", "mu", "xa", "ze", "bi", "so")
		if not getattr(LojbanParser._getword, "_eof", None):
			LojbanParser._getword._eof = False
		# end if not getattr(LojbanParser._getword, "_eof", None):
		if LojbanParser._getword._eof:
			return None
		# end if LojbanParser._getword._eof
		oldch = None
		buffer = []
		while True:
			try:
				if oldch is None:
					ch = sys.stdin.read(1)
				else: # if oldch is None:
					ch = oldch
					oldch = None
				# end if oldch is None:
				self._column += 1
				if (ch == '\n'):
					self._column = 0
					self._line += 1
					if self._interactive:
						LojbanParser._getword._eof = True
						return " ".join((''.join(buffer)).strip().split()) if buffer else None
						# return ''.join(buffer) if buffer else None  # TODO
					# end if self._interactive:
				# end if (ch == '\n'):
				if ch == '': # EOF
					if self._interactive:
						raise LojbanException(self)
					# end if self._interactive:
					LojbanParser._getword._eof = True
					return " ".join((''.join(buffer)).strip().split()) if buffer else None
					# return ''.join(buffer) if buffer else None  # TODO
				elif ch.isspace() or ch == '.':
					if buffer: 
						return " ".join((''.join(buffer)).strip().split())
						# return ''.join(buffer) # TDOD
					# end if buffer: 
				elif ch.isupper():
					buffer.append(ch.lower())
				elif ch.islower() or ch == '\'':
					buffer.append(ch)
				elif ch == '/':
					ch = sys.stdin.read(1)
					while ch != '/' and ch != '':
						ch = sys.stdin.read(1)
					# end while ch != '/' and ch != ''
				elif ch == '\\':
					ch = sys.stdin.read(1)
					if ch != '\n':
						oldch = ch
					else: # if ch != '\n'
						self._column = 0
						self._line += 1
					# end if ch != '\n'
				elif ch.isdigit():
					buffer.append(Getword._digits[ord(ch) - ord('0')])
				# end if ch
			except EOFError as e:
				if self._interactive:
					raise LojbanException(self)
				# end if self._interactive:
				LojbanParser._getword._eof = True
				return " ".join((''.join(buffer)).strip().split()) if buffer else None
				# return ''.join(buffer) if buffer else None  # TODO
			# end try except EOFError as e:
		# end while True:
	# end def _getword(self):

	def _gettoken(self):
		"""
		gettoken() invokes absorb() and returns 
		tokens without modification.
		However, if there are any tokens on the self._pushback list, 
		they will be used first.
		"""
		if self._pushback:
			result = self._pushback
			self._pushback = self._pushback().nextn
			result().nextn = None
		else: # if self._pushback:
			result = self._absorb()
			if self._parameters.D_cpd_lex:
				print("compounder lexing: ", end = "")
				self.print(result())
			# end if self._parameters.D_cpd_lex:
		# end if not self._pushback is None:
		return result
	# end def _gettoken(self):

	def _GIK_root_981(self):
		ttype = 981
		tok = self._GIK_root_981_2()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._GIK_root_981_1()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _GIK_root_981(self):

	def _GIK_root_981_1(self):
		result = self._newtoken()
		tok = self._isnext(Constants.GI_539, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _GIK_root_981_1(self):

	def _GIK_root_981_2(self):
		result = self._newtoken()
		tok = self._isnext(Constants.GI_539, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.NAI_581, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _GIK_root_981_2(self):

	def _GIhEK_root_991(self):
		ttype = 991
		tok = self._GIhEK_root_991_4()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._GIhEK_root_991_5()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._GIhEK_root_991_6()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._GIhEK_root_991_8()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._GIhEK_root_991_1()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._GIhEK_root_991_2()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._GIhEK_root_991_3()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._GIhEK_root_991_7()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _GIhEK_root_991(self):

	def _GIhEK_root_991_1(self):
		result = self._newtoken()
		tok = self._isnext(Constants.GIhA_541, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _GIhEK_root_991_1(self):

	def _GIhEK_root_991_2(self):
		result = self._newtoken()
		tok = self._isnext(Constants.SE_596, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.GIhA_541, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _GIhEK_root_991_2(self):

	def _GIhEK_root_991_3(self):
		result = self._newtoken()
		tok = self._isnext(Constants.NA_578, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.GIhA_541, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _GIhEK_root_991_3(self):

	def _GIhEK_root_991_4(self):
		result = self._newtoken()
		tok = self._isnext(Constants.GIhA_541, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.NAI_581, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _GIhEK_root_991_4(self):

	def _GIhEK_root_991_5(self):
		result = self._newtoken()
		tok = self._isnext(Constants.SE_596, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.GIhA_541, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.NAI_581, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _GIhEK_root_991_5(self):

	def _GIhEK_root_991_6(self):
		result = self._newtoken()
		tok = self._isnext(Constants.NA_578, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.GIhA_541, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.NAI_581, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _GIhEK_root_991_6(self):

	def _GIhEK_root_991_7(self):
		result = self._newtoken()
		tok = self._isnext(Constants.NA_578, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.SE_596, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.GIhA_541, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _GIhEK_root_991_7(self):

	def _GIhEK_root_991_8(self):
		result = self._newtoken()
		tok = self._isnext(Constants.NA_578, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.SE_596, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.GIhA_541, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.NAI_581, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _GIhEK_root_991_8(self):

	def _I_root_956(self):
		ttype = 956
		tok = self._I_root_956_2()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._I_root_956_1()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _I_root_956(self):

	def _I_root_956_1(self):
		result = self._newtoken()
		tok = self._isnext(Constants.I_545, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _I_root_956_1(self):

	def _I_root_956_2(self):
		result = self._newtoken()
		tok = self._isnext(Constants.I_545, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._simple_JOIK_JEK_957()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _I_root_956_2(self):

	def _interval_modifier_1050(self):
		ttype = 1050
		tok = self._interval_modifier_1050_2()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._interval_modifier_1050_1()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._interval_modifier_1050_3()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _interval_modifier_1050(self):

	def _interval_modifier_1050_1(self):
		result = self._newtoken()
		tok = self._interval_property_1051()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _interval_modifier_1050_1(self):

	def _interval_modifier_1050_2(self):
		result = self._newtoken()
		tok = self._interval_property_1051()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._event_mod_1052()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _interval_modifier_1050_2(self):

	def _interval_modifier_1050_3(self):
		result = self._newtoken()
		tok = self._event_mod_1052()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _interval_modifier_1050_3(self):

	def _interval_property_1051(self):
		ttype = 1051
		tok = self._interval_property_1051_2()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._interval_property_1051_1()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._interval_property_1051_4()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._interval_property_1051_3()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _interval_property_1051(self):

	def _interval_property_1051_1(self):
		result = self._newtoken()
		tok = self._number_root_961()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._isnext(Constants.ROI_594, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _interval_property_1051_1(self):

	def _interval_property_1051_2(self):
		result = self._newtoken()
		tok = self._number_root_961()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._isnext(Constants.ROI_594, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.NAI_581, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _interval_property_1051_2(self):

	def _interval_property_1051_3(self):
		result = self._newtoken()
		tok = self._isnext(Constants.TAhE_604, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _interval_property_1051_3(self):

	def _interval_property_1051_4(self):
		result = self._newtoken()
		tok = self._isnext(Constants.TAhE_604, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.NAI_581, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _interval_property_1051_4(self):

	def _isbrivla(self, s):
		"""
		Check if a word if a brivla
		"""
		lastC = False
		for c in s:
			if c == "y" or c == "\'":
				continue
			elif Constants.isC(c) and lastC:
				return True
			elif Constants.isC(c):
				lastC = True
			else:
				lastC = False
			# end if c
		# end for c in s:
		return False
	# end def _isbrivla(s):

	def _iscmene(self, p):
		"""
		Checks if a word is a cmene
		"""
		if not Constants.isC(p[-1]):
			return False
		# end if not isC(s[-1]):
		self._cmenecheck(p, "la")
		self._cmenecheck(p, "doi")
		self._cmenecheck(p, "h")
		self._cmenecheck(p, "w")
		self._cmenecheck(p, "q")
		return True
	# end def _iscmene(p):

	def _isnext(self, t, result):
		"""
		Gets the next token and adds it to result.  If it has the
		specified t, return it otherwise, return None to provoke backtracking.
		Note: "is" is a reserved word in Python thus renamed to isnext.
		"""
		tok = self._gettoken()
		result().add(tok)
		return (tok if (tok().ttype == t) else None)
	# end def _isnext(self, t, result):

	def _JEK_root_926(self):
		ttype = 926
		tok = self._JEK_root_926_4()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._JEK_root_926_5()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._JEK_root_926_6()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._JEK_root_926_8()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._JEK_root_926_1()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._JEK_root_926_2()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._JEK_root_926_3()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._JEK_root_926_7()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _JEK_root_926(self):

	def _JEK_root_926_1(self):
		result = self._newtoken()
		tok = self._isnext(Constants.JA_546, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _JEK_root_926_1(self):

	def _JEK_root_926_2(self):
		result = self._newtoken()
		tok = self._isnext(Constants.SE_596, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.JA_546, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _JEK_root_926_2(self):

	def _JEK_root_926_3(self):
		result = self._newtoken()
		tok = self._isnext(Constants.NA_578, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.JA_546, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _JEK_root_926_3(self):

	def _JEK_root_926_4(self):
		result = self._newtoken()
		tok = self._isnext(Constants.JA_546, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.NAI_581, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _JEK_root_926_4(self):

	def _JEK_root_926_5(self):
		result = self._newtoken()
		tok = self._isnext(Constants.SE_596, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.JA_546, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.NAI_581, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _JEK_root_926_5(self):

	def _JEK_root_926_6(self):
		result = self._newtoken()
		tok = self._isnext(Constants.NA_578, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.JA_546, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.NAI_581, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _JEK_root_926_6(self):

	def _JEK_root_926_7(self):
		result = self._newtoken()
		tok = self._isnext(Constants.NA_578, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.SE_596, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.JA_546, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _JEK_root_926_7(self):

	def _JEK_root_926_8(self):
		result = self._newtoken()
		tok = self._isnext(Constants.NA_578, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.SE_596, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.JA_546, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.NAI_581, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _JEK_root_926_8(self):

	def _JOIK_root_931(self):
		ttype = 931
		tok = self._JOIK_root_931_2()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._JOIK_root_931_1()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._JOIK_root_931_4()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._JOIK_root_931_3()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._JOIK_root_931_5()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._JOIK_root_931_6()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _JOIK_root_931(self):

	def _JOIK_root_931_1(self):
		result = self._newtoken()
		tok = self._isnext(Constants.JOI_548, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _JOIK_root_931_1(self):

	def _JOIK_root_931_2(self):
		result = self._newtoken()
		tok = self._isnext(Constants.JOI_548, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.NAI_581, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _JOIK_root_931_2(self):

	def _JOIK_root_931_3(self):
		result = self._newtoken()
		tok = self._isnext(Constants.SE_596, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.JOI_548, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _JOIK_root_931_3(self):

	def _JOIK_root_931_4(self):
		result = self._newtoken()
		tok = self._isnext(Constants.SE_596, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.JOI_548, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.NAI_581, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _JOIK_root_931_4(self):

	def _JOIK_root_931_5(self):
		result = self._newtoken()
		tok = self._BIhI_root_932()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _JOIK_root_931_5(self):

	def _JOIK_root_931_6(self):
		result = self._newtoken()
		tok = self._isnext(Constants.GAhO_656, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._BIhI_root_932()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._isnext(Constants.GAhO_656, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _JOIK_root_931_6(self):

	def _glue(self):
		"""
		This method handles lujvo glue.  It invokes termin() and does
		1-token lookahead to watch for ZEI.  If found, the ZEI and the following
		token are absorbed into the previous token.  The result is given type BRIVLA.
		"""
		if not getattr(LojbanParser._glue, "_cache", None):
			LojbanParser._glue._cache = None
		# end if not getattr(LojbanParser._glue, "_cache", None):
		tok = LojbanParser._glue._cache if LojbanParser._glue._cache else self._termin()
		if (tok().ttype == 0): 
			return tok
		result = None
		while True:
			LojbanParser._glue._cache = self._termin()
			if LojbanParser._glue._cache().ttype != Constants.ZEI_623:
				break
			elif result is None:
				result = self._newtoken()
				result().ttype = Constants.BRIVLA_509
				result().add(tok)
			result().add(LojbanParser._glue._cache)
			result().add(self._termin())
		# end while True:
		return result if result else tok
	# end def _glue(self):

	def _lerfu(self):
		"""
		This method does BU processing.  It invokes fabsorb() and does
		1-token lookahead to detect a following BU.  The BU is absorbed into
		the previous token, changing its selmao to BY.
		"""
		if not getattr(LojbanParser._lerfu, "_cache", None):
			LojbanParser._lerfu._cache = None
		# end if not getattr(LojbanParser._lerfu, "_cache", None):
		tok = LojbanParser._lerfu._cache if LojbanParser._lerfu._cache else self._fabsorb()
		LojbanParser._lerfu._cache = self._fabsorb()

		if (LojbanParser._lerfu._cache().ttype == Constants.BU_511):
			result = self._newtoken()
			result().ttype = Constants.BY_513
			result().add(tok)
			result().add(LojbanParser._lerfu._cache)
			LojbanParser._lerfu._cache = None
			return result
		# end if (LojbanParser._lerfu._cache().ttype == Constants.BU_511):
		return tok
	# end def _lerfu(self):

	def _lerfu_string_root_986(self):
		result = self._newtoken()
		tok = self._lerfu_word_987()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		while True:
			tok = self._gettoken()
			if tok().ttype == Constants.PA_672:
				result().add(tok)
			elif tok().ttype in [Constants.BY_513, Constants.LAU_559, Constants.TEI_605]:
				self._fail(tok)
				tok = self._lerfu_word_987()
				result().add(tok)
			else:
				self._fail(tok)
				return self._cpd_reduce(result, 986)
			# end if tok().ttype
		# end while True:
	#end def _lerfu_string_root_986(self):

	def _lerfu_word_987(self):
		ttype = 987
		tok = self._lerfu_word_987_1()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._lerfu_word_987_2()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._lerfu_word_987_3()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _lerfu_word_987(self):

	def _lerfu_word_987_1(self):
		result = self._newtoken()
		tok = self._isnext(Constants.BY_513, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _lerfu_word_987_1(self):

	def _lerfu_word_987_2(self):
		result = self._newtoken()
		tok = self._isnext(Constants.LAU_559, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._lerfu_word_987()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _lerfu_word_987_2(self):

	def _lerfu_word_987_3(self):
		result = self._newtoken()
		tok = self._isnext(Constants.TEI_605, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._lerfu_string_root_986()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._isnext(Constants.FOI_533, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _lerfu_word_987_3(self):

	def _lex(self):
		"""
		This method calls getword and lexes the result.  Its morphological
		resolution is rather feeble: it can break up words consisting of compound
		cmavo, but it assumes that brivla and cmene stand alone, without cmavo
		clinging to the front of them.  This assumption holds for consciously
		written Lojban text, although not for the results of a naive transcription
		of Lojban speech.  It returns a pointer to a token object, which is
		created from the free store.  See lojban.h for an explanation of this
		object.
		"""
		if not getattr(LojbanParser._lex, "_word", None):
			LojbanParser._lex._word = None
		# end if not getattr(LojbanParser._lex, "_word", None):
		result = self._newtoken()
		if not LojbanParser._lex._word:
			LojbanParser._lex._word = self._getword()
			if not LojbanParser._lex._word:
				result().ttype = 0
				if self._parameters.D_valsi:
					print("valsi: end of text")
				# end if self._parameters.D_valsi:
				return result
			# end if not LojbanParser._lex._word:
		# end if not LojbanParser._lex._word:
		if self._iscmene(LojbanParser._lex._word):
			result().ttype = Constants.CMENE_517
			result().text = self._newstring(LojbanParser._lex._word)
			LojbanParser._lex._word = None
		elif self._isbrivla(LojbanParser._lex._word):
			result().ttype = Constants.BRIVLA_509
			result().text = self._newstring(LojbanParser._lex._word)
			LojbanParser._lex._word = None
		else:
			tmpword = [c for c in LojbanParser._lex._word]
			tmpword.append('')
			idx = 1
			for idx in range(1, len(tmpword)):
				if Constants.isC(tmpword[idx]):
					break
				# end if Constants.isC(LojbanParser._lex._word[idx]):
			# end for idx in range(1, len(LojbanParser._lex._word)):
			result().text = self._newstring(LojbanParser._lex._word[:idx])
			# LojbanParser._lex._word = p
			LojbanParser._lex._word = LojbanParser._lex._word[len(result().text):]
		# end if
		if self._parameters.D_valsi:
			print("valsi: ", end = "")
			self.print(result())
		# end if self._parameters.D_valsi:
		return result
	# end def _lex():

	def _lexer_A_905_driver(self):
		return self._cpd_reduce(self._utt_ordinal_root_906(), 905)
	#end def _lexer_A_905_driver(self):

	def _lexer_B_910_driver(self):
		return self._cpd_reduce(self._EK_root_911(), 910)
	#end def _lexer_B_910_driver(self):

	def _lexer_C_915_driver(self):
		ttype = 915
		tok = self._lexer_C_915_1()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._lexer_C_915_2()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _lexer_C_915_driver(self):

	def _lexer_C_915_1(self):
		result = self._newtoken()
		tok = self._EK_root_911()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._isnext(Constants.BO_508, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _lexer_C_915_1(self):

	def _lexer_C_915_2(self):
		result = self._newtoken()
		tok = self._EK_root_911()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._simple_tag_971()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._isnext(Constants.BO_508, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _lexer_C_915_2(self):

	def _lexer_D_916_driver(self):
		ttype = 916
		tok = self._lexer_D_916_1()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._lexer_D_916_2()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _lexer_D_916_driver(self):

	def _lexer_D_916_1(self):
		result = self._newtoken()
		tok = self._EK_root_911()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._isnext(Constants.KE_551, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _lexer_D_916_1(self):

	def _lexer_D_916_2(self):
		result = self._newtoken()
		tok = self._EK_root_911()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._simple_tag_971()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._isnext(Constants.KE_551, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _lexer_D_916_2(self):

	def _lexer_E_925_driver(self):
		return self._cpd_reduce(self._JEK_root_926(), 925)
	#end def _lexer_E_925_driver(self):

	def _lexer_F_930_driver(self):
		return self._cpd_reduce(self._JOIK_root_931(), 930)
	#end def _lexer_F_930_driver(self):

	def _lexer_G_935_driver(self):
		ttype = 935
		tok = self._lexer_G_935_3()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._lexer_G_935_1()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._lexer_G_935_4()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._lexer_G_935_2()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._lexer_G_935_5()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._lexer_G_935_6()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _lexer_G_935_driver(self):

	def _lexer_G_935_1(self):
		result = self._newtoken()
		tok = self._isnext(Constants.GA_537, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _lexer_G_935_1(self):

	def _lexer_G_935_2(self):
		result = self._newtoken()
		tok = self._isnext(Constants.SE_596, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.GA_537, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _lexer_G_935_2(self):

	def _lexer_G_935_3(self):
		result = self._newtoken()
		tok = self._isnext(Constants.GA_537, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.NAI_581, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _lexer_G_935_3(self):

	def _lexer_G_935_4(self):
		result = self._newtoken()
		tok = self._isnext(Constants.SE_596, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.GA_537, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.NAI_581, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _lexer_G_935_4(self):

	def _lexer_G_935_5(self):
		result = self._newtoken()
		tok = self._simple_tag_971()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._GIK_root_981()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _lexer_G_935_5(self):

	def _lexer_G_935_6(self):
		result = self._newtoken()
		tok = self._JOIK_root_931()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._isnext(Constants.GI_539, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _lexer_G_935_6(self):

	def _lexer_H_940_driver(self):
		ttype = 940
		tok = self._lexer_H_940_3()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._lexer_H_940_1()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._lexer_H_940_4()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._lexer_H_940_2()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _lexer_H_940_driver(self):

	def _lexer_H_940_1(self):
		result = self._newtoken()
		tok = self._isnext(Constants.GUhA_544, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _lexer_H_940_1(self):

	def _lexer_H_940_2(self):
		result = self._newtoken()
		tok = self._isnext(Constants.SE_596, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.GUhA_544, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _lexer_H_940_2(self):

	def _lexer_H_940_3(self):
		result = self._newtoken()
		tok = self._isnext(Constants.GUhA_544, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.NAI_581, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _lexer_H_940_3(self):

	def _lexer_H_940_4(self):
		result = self._newtoken()
		tok = self._isnext(Constants.SE_596, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.GUhA_544, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.NAI_581, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _lexer_H_940_4(self):

	def _lexer_I_945_driver(self):
		ttype = 945
		tok = self._lexer_I_945_1()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _lexer_I_945_driver(self):

	def _lexer_I_945_1(self):
		result = self._newtoken()
		tok = self._isnext(Constants.NAhE_583, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.BO_508, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _lexer_I_945_1(self):

	def _lexer_J_950_driver(self):
		ttype = 950
		tok = self._lexer_J_950_1()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _lexer_J_950_driver(self):

	def _lexer_J_950_1(self):
		result = self._newtoken()
		tok = self._isnext(Constants.NA_578, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.KU_556, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _lexer_J_950_1(self):

	def _lexer_K_955_driver(self):
		ttype = 955
		tok = self._lexer_K_955_1()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._lexer_K_955_2()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _lexer_K_955_driver(self):

	def _lexer_K_955_1(self):
		result = self._newtoken()
		tok = self._I_root_956()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._isnext(Constants.BO_508, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _lexer_K_955_1(self):

	def _lexer_K_955_2(self):
		result = self._newtoken()
		tok = self._I_root_956()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._simple_tag_971()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._isnext(Constants.BO_508, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _lexer_K_955_2(self):

	def _lexer_L_960_driver(self):
		return self._cpd_reduce(self._number_root_961(), 960)
	#end def _lexer_L_960_driver(self):

	def _lexer_M_965_driver(self):
		ttype = 965
		tok = self._lexer_M_965_1()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._lexer_M_965_2()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _lexer_M_965_driver(self):

	def _lexer_M_965_1(self):
		result = self._newtoken()
		tok = self._GIhEK_root_991()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._isnext(Constants.BO_508, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _lexer_M_965_1(self):

	def _lexer_M_965_2(self):
		result = self._newtoken()
		tok = self._GIhEK_root_991()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._simple_tag_971()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._isnext(Constants.BO_508, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _lexer_M_965_2(self):

	def _lexer_N_966_driver(self):
		ttype = 966
		tok = self._lexer_N_966_1()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._lexer_N_966_2()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _lexer_N_966_driver(self):

	def _lexer_N_966_1(self):
		result = self._newtoken()
		tok = self._GIhEK_root_991()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._isnext(Constants.KE_551, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _lexer_N_966_1(self):

	def _lexer_N_966_2(self):
		result = self._newtoken()
		tok = self._GIhEK_root_991()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._simple_tag_971()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._isnext(Constants.KE_551, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _lexer_N_966_2(self):

	def _lexer_O_970_driver(self):
		return self._cpd_reduce(self._simple_tense_modal_972(), 970)
	#end def _lexer_O_970_driver(self):

	def _lexer_P_980_driver(self):
		return self._cpd_reduce(self._GIK_root_981(), 980)
	#end def _lexer_P_980_driver(self):

	def _lexer_Q_985_driver(self):
		return self._cpd_reduce(self._lerfu_string_root_986(), 985)
	#end def _lexer_Q_985_driver(self):

	def _lexer_R_990_driver(self):
		return self._cpd_reduce(self._GIhEK_root_991(), 990)
	#end def _lexer_R_990_driver(self):

	def _lexer_S_995_driver(self):
		return self._cpd_reduce(self._I_root_956(), 995)
	#end def _lexer_S_995_driver(self):

	def _lexer_U_1005_driver(self):
		ttype = 1005
		tok = self._lexer_U_1005_2()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._lexer_U_1005_1()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _lexer_U_1005_driver(self):

	def _lexer_U_1005_1(self):
		result = self._newtoken()
		tok = self._JEK_root_926()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._isnext(Constants.BO_508, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _lexer_U_1005_1(self):

	def _lexer_U_1005_2(self):
		result = self._newtoken()
		tok = self._JEK_root_926()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._simple_tag_971()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._isnext(Constants.BO_508, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _lexer_U_1005_2(self):

	def _lexer_V_1010_driver(self):
		ttype = 1010
		tok = self._lexer_V_1010_2()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._lexer_V_1010_1()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _lexer_V_1010_driver(self):

	def _lexer_V_1010_1(self):
		result = self._newtoken()
		tok = self._JOIK_root_931()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._isnext(Constants.BO_508, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _lexer_V_1010_1(self):

	def _lexer_V_1010_2(self):
		result = self._newtoken()
		tok = self._JOIK_root_931()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._simple_tag_971()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._isnext(Constants.BO_508, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _lexer_V_1010_2(self):

	def _lexer_W_1015_driver(self):
		ttype = 1015
		tok = self._lexer_W_1015_2()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._lexer_W_1015_1()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _lexer_W_1015_driver(self):

	def _lexer_W_1015_1(self):
		result = self._newtoken()
		tok = self._JOIK_root_931()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._isnext(Constants.KE_551, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _lexer_W_1015_1(self):

	def _lexer_W_1015_2(self):
		result = self._newtoken()
		tok = self._JOIK_root_931()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._simple_tag_971()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._isnext(Constants.KE_551, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _lexer_W_1015_2(self):

	def _lexer_Y_1025_driver(self):
		ttype = 1025
		tok = self._lexer_Y_1025_1()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._lexer_Y_1025_2()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _lexer_Y_1025_driver(self):

	def _lexer_Y_1025_1(self):
		result = self._newtoken()
		tok = self._number_root_961()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._isnext(Constants.MOI_663, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _lexer_Y_1025_1(self):

	def _lexer_Y_1025_2(self):
		result = self._newtoken()
		tok = self._lerfu_string_root_986()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._isnext(Constants.MOI_663, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _lexer_Y_1025_2(self):

	def _makefree(self):
		"""
		manufactures new tokens for the freelist.
		"""
		self._tokenslist.append(Token())
		self._tokspace += sys.getsizeof(Token())
		self._tokenslist[-1].nextn = None
		self._freelist = weakref.ref(self._tokenslist[-1])
	# end def _makefree(self):

	def _modal_974(self):
		ttype = 974
		tok = self._modal_974_2()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._modal_974_1()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _modal_974(self):

	def _modal_974_1(self):
		result = self._newtoken()
		tok = self._modal_A_975()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _modal_974_1(self):

	def _modal_974_2(self):
		result = self._newtoken()
		tok = self._modal_A_975()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._isnext(Constants.NAI_581, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _modal_974_2(self):

	def _modal_A_975(self):
		ttype = 973
		tok = self._modal_A_975_1()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._modal_A_975_2()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _modal_A_975(self):

	def _modal_A_975_1(self):
		result = self._newtoken()
		tok = self._isnext(Constants.BAI_502, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _modal_A_975_1(self):

	def _modal_A_975_2(self):
		result = self._newtoken()
		tok = self._isnext(Constants.SE_596, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.BAI_502, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _modal_A_975_2(self):

	def _newnode(self, t, n1):
		"""
		Creates a new node.
		Note: Some code was never executed and thus removed.
		"""
		# Removed the following code
		# since simplemode is 0 in node.c and cannot change (unless
		# the code is modified).
		# Removed code start:
		#	if (0 && simplemode)	/* not yet implemented */
		#		result = n1
		# Removed code end.
		# Note that the else clause is the only part executed
		result = self._newtoken()
		result().add(n1)
		result().ttype = self._lastreduce = t
		if self._parameters.D_reduce:
			print("reducing to {:s}".format(Constants.rulename(t)))
		# end if self._parameters.D_reduce:
		return result
	# end def _newnode(self, t, n1):

	def _newstring(self, word):
		"""
		Counts memory used for the words.
		"""
		self._stringspace += len(word)
		result = word
		return result
	# end def _newstring(self, n):

	def _newtoken(self):
		"""
		Creates a new token and assigns (global) variables 
		freelist and newtoken_result.
		Returns a newly allocated and initialized token.
		"""
		if self._freelist is None:
			self._makefree()
		# end if self._freelist is None:
		self._newtoken_result = self._freelist
		self._freelist = self._freelist().nextn
		self._newtoken_result().ttype = -1
		self._newtoken_result().text = None
		self._newtoken_result().up = self._newtoken_result().right = \
			self._newtoken_result().nextn = self._newtoken_result().downleft = \
			self._newtoken_result().downright = None
		return self._newtoken_result
	# end def _newtoken(self):

	def _node(self, t, n1, *n):
		"""
		node1: It doesn't construct a new node but simply patches up the old one.
		node2..8: They construct new nodes in the parse tree and return them.  
			The first argument is the type of the new node, 
			the remaining arguments are subnodes to add to the new node.
		"""
		if len(n) == 0:
			if self._parameters.singlemode:
				result = self._newnode(t, n1)
				return result
			else: # if self._parameters.singlemode:
				if n1:
					n1().ttype = t
				return n1
			# end if self._parameters.singlemode:
			return None
		elif len(n) > 7:
			LojbanException(self, "FATAL ERROR: node called with" + \
				" {:d}".format(len(n)+2) + " args (accepts max 9).")
		# end if len(n) 

		result = self._newnode(t, n1)
		for ni in n:
			result().add(ni)
		# end for ni in n:
		return result
	# end def _node(self, t, n1, *n):

	def _number_root_961(self):
		result = self._newtoken()
		tok = self._isnext(Constants.PA_672, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		while True:
			tok = self._gettoken()
			if tok().ttype == Constants.PA_672:
				result().add(tok)
			elif tok().ttype in [Constants.BY_513, Constants.LAU_559, Constants.TEI_605]:
				self._fail(tok)
				tok = self._lerfu_word_987()
				result().add(tok)
			else:
				self._fail(tok)
				return result
			# end if tok().ttype ?
		# end while True:
	#end def _number_root_961(self):

	def _release(self, tok):
		"""
		Release a token from the queue
		"""
		t = tok().ttype
		if (t == 0 or (t >= 500 and t <= 699)):
			if self._tail:
				self._tail().nextn = tok
			else: # if self._tail:
				self._head = tok
			# end if not self._tail is None:
			self._tail = tok
			tok().right = tok().up = tok().nextn = None
		else: # if (type == 0 or (t >= 500 and t <= 699)):
			p = tok().downleft
			while p:
				nextp = p().right
				self._release(p)
				p = nextp
			# end while not p is None:
			self._destroy(tok)
		# end if (type == 0 or (t >= 500 and t <= 699)):
	# end def _release(self, tok):

	def _selmao(self):
		"""
		This method assigns cmavo to their selmao using the table in selmao.i.
		Tokens are collected from filter().  Any with types already assigned 
		are not looked up.
		"""
		cons = (0, 1, 2, 3, 0, 4, 5, 0, 0, 6, 7, 8, 9, \
			10, 0, 11, 0, 12, 13, 14, 0, 15, 0, 16, 0, 17 )

		result = self._filter()
		if (result().ttype != Constants.UNK_M1):
			return result

		i = result().text[0]
		i = cons[ord(i) - ord('a')] if i.islower() else 0
		# bumps pointer by 1 if i is nonzero (consonant)
		j = Constants.get_vowels(result().text[(1 if (i != 0) else 0):])
		if i != 0 and j > 34:
			j = Constants.UNK_M1
		if j != Constants.UNK_M1: 
			result().ttype = Constants.cmavo[i][j]
		if result().ttype == Constants.UNK_M1:
			print("Unknown cmavo {:s}".format(result().text) + \
				" at line {:d}, column {:d};".format(self._line, self._column) + \
				" selma'o UI assumed", file = sys.stderr)
			result().ttype = Constants.UI_612
		elif (result().ttype == Constants.XAI_M2):
			print("Experimental cmavo {:s}".format(result().text) + \
				" at line {:d}, column {:d};".format(self._line, self._column) + \
				" selma'o UI assumed\n", file = sys.stderr)
			result().ttype = Constants.UI_612
		# end if
		return result
	# end def _selmao(self):

	def _simple_JOIK_JEK_957(self):
		ttype = 957
		tok = self._JOIK_root_931()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._JEK_root_926()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _simple_JOIK_JEK_957(self):

	def _simple_tag_971(self):
		ttype = 971
		tok = self._gettoken()
		nexttype = tok().ttype
		self._fail(tok)
		if nexttype in [Constants.BAI_502, Constants.CAhA_514, Constants.CUhE_521, Constants.FAhA_528, Constants.FEhE_530, Constants.KI_554, Constants.MOhI_577, Constants.NAhE_583, Constants.PU_592, Constants.SE_596, Constants.TAhE_604, Constants.VA_613, Constants.VEhA_615, Constants.VIhA_616, Constants.ZAhO_621, Constants.ZEhA_622, Constants.ZI_624]:
			tok = self._simple_tag_971_12()
			if tok:
				return self._cpd_reduce(tok, ttype)
			# end if tok:
		# end if nexttype in ?
		return None
	#end def _simple_tag_971(self):

	def _simple_tag_971_12(self):
		result = self._newtoken()
		tok = self._simple_tense_modal_972()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		while True:
			joikjek = self._simple_JOIK_JEK_957()
			if not joikjek:
				return result
			# end if not joikjek:
			tok = self._simple_tense_modal_972()
			if not tok:
				self._fail(joikjek)
				return result
			#end if (!tok) :
			result().add(joikjek)
			result().add(tok)
			result().ttype = 971
			tok = self._newtoken()
			tok().add(result)
			result = tok
		# end while True:
	#end def _simple_tag_971_12(self):

	def _simple_tense_modal_972(self):
		ttype = 972
		tok = self._simple_tense_modal_972_1()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._simple_tense_modal_972_2()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._simple_tense_modal_972_3()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._simple_tense_modal_972_4()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _simple_tense_modal_972(self):

	def _simple_tense_modal_972_1(self):
		result = self._newtoken()
		tok = self._simple_tense_modal_A_973()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _simple_tense_modal_972_1(self):

	def _simple_tense_modal_972_2(self):
		result = self._newtoken()
		tok = self._isnext(Constants.NAhE_583, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._simple_tense_modal_A_973()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _simple_tense_modal_972_2(self):

	def _simple_tense_modal_972_3(self):
		result = self._newtoken()
		tok = self._isnext(Constants.CUhE_521, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _simple_tense_modal_972_3(self):

	def _simple_tense_modal_972_4(self):
		result = self._newtoken()
		tok = self._isnext(Constants.KI_554, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _simple_tense_modal_972_4(self):

	def _simple_tense_modal_A_973(self):
		ttype = 973
		tok = self._simple_tense_modal_A_973_2()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._simple_tense_modal_A_973_1()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._simple_tense_modal_A_973_3()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _simple_tense_modal_A_973(self):

	def _simple_tense_modal_A_973_1(self):
		result = self._newtoken()
		tok = self._modal_974()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _simple_tense_modal_A_973_1(self):

	def _simple_tense_modal_A_973_2(self):
		result = self._newtoken()
		tok = self._modal_974()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._isnext(Constants.KI_554, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _simple_tense_modal_A_973_2(self):

	def _simple_tense_modal_A_973_3(self):
		result = self._newtoken()
		tok = self._tense_A_977()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _simple_tense_modal_A_973_3(self):

	def _space_1040(self):
		ttype = 1040
		tok = self._space_1040_3()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._space_1040_1()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._space_1040_2()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _space_1040(self):

	def _space_1040_1(self):
		result = self._newtoken()
		tok = self._space_A_1042()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _space_1040_1(self):

	def _space_1040_2(self):
		result = self._newtoken()
		tok = self._space_motion_1041()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _space_1040_2(self):

	def _space_1040_3(self):
		result = self._newtoken()
		tok = self._space_A_1042()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._space_motion_1041()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _space_1040_3(self):

	def _space_motion_1041(self):
		result = self._newtoken()
		tok = self._isnext(Constants.MOhI_577, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._space_offset_1045()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _space_motion_1041(self):

	def _space_A_1042(self):
		ttype = 1042
		tok = self._space_A_1042_2()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._space_A_1042_1()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._space_A_1042_3()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _space_A_1042(self):

	def _space_A_1042_1(self):
		result = self._newtoken()
		tok = self._isnext(Constants.VA_613, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _space_A_1042_1(self):

	def _space_A_1042_2(self):
		result = self._newtoken()
		tok = self._isnext(Constants.VA_613, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._space_B_1043()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _space_A_1042_2(self):

	def _space_A_1042_3(self):
		result = self._newtoken()
		tok = self._space_B_1043()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _space_A_1042_3(self):

	def _space_B_1043(self):
		ttype = 1043
		tok = self._space_B_1043_3()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._space_B_1043_1()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._space_B_1043_2()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _space_B_1043(self):

	def _space_B_1043_1(self):
		result = self._newtoken()
		tok = self._space_C_1044()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _space_B_1043_1(self):

	def _space_B_1043_2(self):
		result = self._newtoken()
		tok = self._space_intval_1046()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _space_B_1043_2(self):

	def _space_B_1043_3(self):
		result = self._newtoken()
		tok = self._space_C_1044()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._space_intval_1046()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _space_B_1043_3(self):

	def _space_C_1044(self):
		result = self._newtoken()
		tok = self._space_offset_1045()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		while True:
			tok = self._space_offset_1045()
			if not tok:
				return result
			# end if not tok:
			result().add(tok)
		# end while True:
	#end def _space_C_1044(self):

	def _space_offset_1045(self):
		ttype = 1045
		tok = self._space_offset_1045_2()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._space_offset_1045_1()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _space_offset_1045(self):

	def _space_offset_1045_1(self):
		result = self._newtoken()
		tok = self._space_direction_1048()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _space_offset_1045_1(self):

	def _space_offset_1045_2(self):
		result = self._newtoken()
		tok = self._space_direction_1048()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._isnext(Constants.VA_613, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _space_offset_1045_2(self):

	def _space_intval_1046(self):
		ttype = 1046
		tok = self._space_intval_1046_5()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._space_intval_1046_4()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._space_intval_1046_3()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._space_intval_1046_2()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._space_intval_1046_1()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _space_intval_1046(self):

	def _space_intval_1046_1(self):
		result = self._newtoken()
		tok = self._space_intval_A_1047()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _space_intval_1046_1(self):

	def _space_intval_1046_2(self):
		result = self._newtoken()
		tok = self._space_intval_A_1047()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._space_direction_1048()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _space_intval_1046_2(self):

	def _space_intval_1046_3(self):
		result = self._newtoken()
		tok = self._isnext(Constants.FEhE_530, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._interval_modifier_1050()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _space_intval_1046_3(self):

	def _space_intval_1046_4(self):
		result = self._newtoken()
		tok = self._space_intval_A_1047()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._isnext(Constants.FEhE_530, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._interval_modifier_1050()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _space_intval_1046_4(self):

	def _space_intval_1046_5(self):
		result = self._newtoken()
		tok = self._space_intval_A_1047()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._space_direction_1048()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._isnext(Constants.FEhE_530, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._interval_modifier_1050()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _space_intval_1046_5(self):

	def _space_intval_A_1047(self):
		ttype = 1047
		tok = self._space_intval_A_1047_3()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._space_intval_A_1047_1()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._space_intval_A_1047_2()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _space_intval_A_1047(self):

	def _space_intval_A_1047_1(self):
		result = self._newtoken()
		tok = self._isnext(Constants.VEhA_615, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _space_intval_A_1047_1(self):

	def _space_intval_A_1047_2(self):
		result = self._newtoken()
		tok = self._isnext(Constants.VIhA_616, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _space_intval_A_1047_2(self):

	def _space_intval_A_1047_3(self):
		result = self._newtoken()
		tok = self._isnext(Constants.VEhA_615, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.VIhA_616, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _space_intval_A_1047_3(self):

	def _space_direction_1048(self):
		ttype = 1048
		tok = self._space_direction_1048_2()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._space_direction_1048_1()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _space_direction_1048(self):

	def _space_direction_1048_1(self):
		result = self._newtoken()
		tok = self._isnext(Constants.FAhA_528, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _space_direction_1048_1(self):

	def _space_direction_1048_2(self):
		result = self._newtoken()
		tok = self._isnext(Constants.FAhA_528, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.NAI_581, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _space_direction_1048_2(self):

	@staticmethod
	def _strchr(s, ch):
		"""
		Check is character ch exists in string s.
		Returns the index of ch if it exists or None.
		"""
		try:
			return s.index(ch)
		except ValueError:
			return None
		# end try except ValueError:
	# end def _strchr(s, ch):

	def _tense_A_977(self):
		ttype = 977
		tok = self._tense_A_977_2()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._tense_A_977_1()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _tense_A_977(self):

	def _tense_A_977_1(self):
		result = self._newtoken()
		tok = self._tense_B_978()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _tense_A_977_1(self):

	def _tense_A_977_2(self):
		result = self._newtoken()
		tok = self._tense_B_978()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._isnext(Constants.KI_554, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _tense_A_977_2(self):

	def _tense_B_978(self):
		ttype = 978
		tok = self._tense_B_978_3()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._tense_B_978_1()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._tense_B_978_2()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _tense_B_978(self):

	def _tense_B_978_1(self):
		result = self._newtoken()
		tok = self._tense_C_979()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _tense_B_978_1(self):

	def _tense_B_978_2(self):
		result = self._newtoken()
		tok = self._isnext(Constants.CAhA_514, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _tense_B_978_2(self):

	def _tense_B_978_3(self):
		result = self._newtoken()
		tok = self._tense_C_979()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._isnext(Constants.CAhA_514, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _tense_B_978_3(self):

	def _tense_C_979(self):
		ttype = 979
		tok = self._tense_C_979_3()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._tense_C_979_1()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._tense_C_979_2()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _tense_C_979(self):

	def _tense_C_979_1(self):
		result = self._newtoken()
		tok = self._time_1030()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _tense_C_979_1(self):

	def _tense_C_979_2(self):
		result = self._newtoken()
		tok = self._space_1040()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _tense_C_979_2(self):

	def _tense_C_979_3(self):
		result = self._newtoken()
		tok = self._time_1030()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._space_1040()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _tense_C_979_3(self):

	def _termin(self):
		"""
		This method guarantees proper termination.  It calls selmao() and passes
		through the tokens unchanged, except that if the current token is EOT and
		the last token was not FAhO, a FAhO is generated.  After any FAhO, whether
		real or generated, only EOT tokens will be returned.
		"""
		if not getattr(LojbanParser._termin, "_lasttype", None):
			LojbanParser._termin._lasttype = -1
		# end if not getattr(LojbanParser._termin, "_lasttype", None):
		if LojbanParser._termin._lasttype == Constants.FAhO_529:
			tok = self._newtoken()
			tok().ttype = 0
			return tok
		# end if LojbanParser._termin._lasttype == Constants.FAhO_529:
		tok = self._selmao()
		if tok().ttype == 0:
			tok = self._newtoken()
			tok().ttype = Constants.FAhO_529
			tok().text = self._newstring("(fa'o)")
		# end if tok().ttype == 0:
		LojbanParser._termin._lasttype = tok().ttype
		return tok
	# end def _termin(self):

	def _time_1030(self):
		ttype = 1030
		tok = self._time_1030_2()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._time_1030_1()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._time_1030_3()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _time_1030(self):

	def _time_1030_1(self):
		result = self._newtoken()
		tok = self._isnext(Constants.ZI_624, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _time_1030_1(self):

	def _time_1030_2(self):
		result = self._newtoken()
		tok = self._isnext(Constants.ZI_624, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._time_A_1031()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _time_1030_2(self):

	def _time_1030_3(self):
		result = self._newtoken()
		tok = self._time_A_1031()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _time_1030_3(self):

	def _time_A_1031(self):
		ttype = 1031
		tok = self._time_A_1031_3()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._time_A_1031_1()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._time_A_1031_2()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _time_A_1031(self):

	def _time_A_1031_1(self):
		result = self._newtoken()
		tok = self._time_B_1032()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _time_A_1031_1(self):

	def _time_A_1031_2(self):
		result = self._newtoken()
		tok = self._time_interval_1034()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _time_A_1031_2(self):

	def _time_A_1031_3(self):
		result = self._newtoken()
		tok = self._time_B_1032()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._time_interval_1034()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _time_A_1031_3(self):

	def _time_B_1032(self):
		result = self._newtoken()
		tok = self._time_offset_1033()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		while True:
			tok = self._time_offset_1033()
			if not tok:
				return result
			# end if not tok:
			result().add(tok)
		# end while True:
	#end def _time_B_1032(self):

	def _time_offset_1033(self):
		ttype = 1033
		tok = self._time_offset_1033_2()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._time_offset_1033_1()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _time_offset_1033(self):

	def _time_offset_1033_1(self):
		result = self._newtoken()
		tok = self._time_direction_1035()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _time_offset_1033_1(self):

	def _time_offset_1033_2(self):
		result = self._newtoken()
		tok = self._time_direction_1035()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._isnext(Constants.ZI_624, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _time_offset_1033_2(self):

	def _time_interval_1034(self):
		ttype = 1034
		tok = self._time_interval_1034_5()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._time_interval_1034_4()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._time_interval_1034_3()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._time_interval_1034_2()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._time_interval_1034_1()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _time_interval_1034(self):

	def _time_interval_1034_1(self):
		result = self._newtoken()
		tok = self._isnext(Constants.ZEhA_622, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _time_interval_1034_1(self):

	def _time_interval_1034_2(self):
		result = self._newtoken()
		tok = self._isnext(Constants.ZEhA_622, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._time_direction_1035()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _time_interval_1034_2(self):

	def _time_interval_1034_3(self):
		result = self._newtoken()
		tok = self._interval_modifier_1050()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _time_interval_1034_3(self):

	def _time_interval_1034_4(self):
		result = self._newtoken()
		tok = self._isnext(Constants.ZEhA_622, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._interval_modifier_1050()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _time_interval_1034_4(self):

	def _time_interval_1034_5(self):
		result = self._newtoken()
		tok = self._isnext(Constants.ZEhA_622, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._time_direction_1035()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._interval_modifier_1050()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		return result
	#end def _time_interval_1034_5(self):

	def _time_direction_1035(self):
		ttype = 1035
		tok = self._time_direction_1035_2()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._time_direction_1035_1()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _time_direction_1035(self):

	def _time_direction_1035_1(self):
		result = self._newtoken()
		tok = self._isnext(Constants.PU_592, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _time_direction_1035_1(self):

	def _time_direction_1035_2(self):
		result = self._newtoken()
		tok = self._isnext(Constants.PU_592, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		tok = self._isnext(Constants.NAI_581, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _time_direction_1035_2(self):

	def _toplevel(self, n1):
		"""
		toplevel(n1) is invoked at the top level of the parse to stash the topmost
		node someplace useful.
		"""
		self._results = n1
		return n1
	# end def _toplevel(self, n1):

	def _utt_ordinal_root_906(self):
		ttype = 906
		tok = self._utt_ordinal_root_906_1()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		tok = self._utt_ordinal_root_906_2()
		if tok:
			return self._cpd_reduce(tok, ttype)
		# end if tok:
		return None
	#end def _utt_ordinal_root_906(self):

	def _utt_ordinal_root_906_1(self):
		result = self._newtoken()
		tok = self._lerfu_string_root_986()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._isnext(Constants.MAI_661, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _utt_ordinal_root_906_1(self):

	def _utt_ordinal_root_906_2(self):
		result = self._newtoken()
		tok = self._number_root_961()
		if not tok:
			return self._fail(result)
		# end if not tok:
		result().add(tok)
		tok = self._isnext(Constants.MAI_661, result)
		if not tok:
			return self._fail(result)
		# end if not tok:
		return result
	#end def _utt_ordinal_root_906_2(self):

	def _yyerror(self, msg):
		"""
		Is invoked by the parser when an error (either a real error,
		or else an elided terminator) is detected.  
		It stashes away the next token, the current line, and the current column.
		"""
		self._errline = self._line
		self._errcol = self._column
		self._errtype = self._pcyytoken
		self._errlastreduce = self._lastreduce
	# end def _yyerror(self, msg):

	def _yylex(self):
		"""
		This is the parser's lexical analyzer.  It invokes compound() and
		places the result in yylval.  Returns the node type.
		"""
		self._yylval = self._compound()
		if self._parameters.D_lex:
			print("lexing (selma'o {:s}): ".format(Constants.rulename(self._yylval().ttype)), end = "")
			self.print(self._yylval())
			# print() # TODO added for DEBUG
		# end if self._parameters.D_lex:
		return self._yylval().ttype
	# end def _yylex():

	def _yyparse(self, yymaxdepth = 200, yyredmax = 1000, \
		yydebug = False, yytflag = False, yytfilen = "grammar.tmp"):
		"""
		Parses the document.
		Returns true on success and false on error.
		"""
		_YYMAXDEPTH = yymaxdepth
		_YYREDMAX = yyredmax
		_YYDEBUG = yydebug
		_YYTFLAG = yytflag
		_YYTFILEN = yytfilen

		_PCYYFLAG = -1000
		_WAS0ERR = 0
		_WAS1ERR = 1
		_WAS2ERR = 2
		_WAS3ERR = 3
		_YYLAST = 3903
		_YYERRCODE = 256
		_YYEXCA = (
			-1, 1, \
			0, -1, \
			-2, 0, \
			-1, 403, \
			561, 179, \
			657, 179, \
			664, 179, \
			666, 179, \
			677, 179, \
			935, 179, \
			945, 179, \
			960, 179, \
			985, 179, \
			-2, 169, \
			0, \
		)
		_YYACT = (
			75,	  74,	  67,	 276,	  28,	 152,	 299,	 330, \
			283,	  27,	 448,	  34,	 300,	  26,	  81,	  51, \
			79,	 502,	 296,	  30,	  36,	  45,	  27,	 101, \
			31,	  67,	 525,	  69,	  79,	  28,	  79,	  11, \
			37,	 494,	  27,	 581,	 578,	 332,	  86,	 154, \
			331,	 333,	 548,	 145,	 232,	  27,	  51,	 143, \
			354,	 239,	 370,	 119,	  45,	 377,	 112,	 155, \
			506,	 117,	 121,	 187,	 385,	 152,	 113,	 205, \
			179,	 133,	 178,	 129,	 367,	 473,	 146,	 495, \
			86,	 290,	  68,	 509,	  68,	   7,	 252,	 139, \
			31,	  87,	 155,	  93,	  79,	 490,	 502,	 241, \
			532,	 250,	 243,	 302,	 150,	  47,	 284,	 154, \
			443,	 139,	  41,	 145,	 459,	 300,	  39,	 143, \
			75,	  74,	  65,	 284,	  33,	 152,	 150,	  31, \
			229,	  42,	  35,	  87,	 157,	 406,	  75,	  51, \
			437,	  74,	 132,	 131,	  47,	  45,	 146,	 101, \
			34,	  41,	  68,	 434,	  79,	  39,	 440,	 139, \
			375,	  36,	 155,	  51,	 471,	 137,	  86,	 154, \
			42,	 201,	 334,	 145,	 150,	  37,	 187,	 143, \
			546,	 100,	 336,	 119,	 151,	  99,	 112,	 297, \
			282,	 117,	 121,	 147,	 431,	 225,	 113,	 187, \
			66,	 133,	  62,	 129,	 107,	  81,	 146,	  63, \
			265,	 520,	  68,	 266,	 135,	 304,	 312,	 139, \
			31,	  87,	 155,	  93,	  77,	  17,	  75,	  74, \
			20,	 262,	  58,	 152,	 150,	  47,	  49,	  14, \
			71,	 130,	  41,	 164,	 117,	 248,	  39,	 118, \
			70,	 298,	  65,	 280,	  10,	 101,	   6,	 434, \
			152,	  42,	  79,	 147,	  16,	 383,	  98,	 518, \
			165,	  33,	 132,	 131,	  86,	 154,	 529,	  35, \
			56,	 145,	  18,	 435,	 488,	 143,	  95,	  79, \
			204,	 119,	 223,	 197,	 112,	 202,	 128,	 117, \
			121,	 407,	 154,	 196,	 113,	 182,	 145,	 133, \
			530,	 129,	 143,	 127,	 146,	  19,	 126,	 122, \
			68,	 200,	 177,	 147,	  73,	 139,	  31,	  87, \
			155,	  93,	  15,	  46,	 254,	  81,	 277,	 199, \
			173,	 146,	 150,	 275,	 153,	  68,	 117,	  75, \
			74,	 149,	 139,	 286,	 152,	 155,	  13,	 247, \
			65,	  80,	 399,	 368,	 259,	 244,	 507,	 150, \
			324,	 148,	 504,	 258,	 139,	 257,	 101,	 501, \
			132,	 131,	 142,	  79,	 342,	 337,	 335,	 134, \
			81,	 150,	 125,	 328,	 285,	  86,	 154,	 311, \
			123,	 186,	 145,	 306,	 232,	 441,	 143,	 379, \
			410,	 438,	 119,	 115,	 329,	 112,	 114,	 482, \
			117,	 121,	 111,	 106,	 502,	 113,	 410,	 104, \
			133,	 147,	 129,	 237,	  91,	 146,	 164,	 371, \
			92,	  68,	  85,	  81,	  84,	 152,	 139,	  31, \
			87,	 155,	  93,	 508,	  83,	 289,	 147,	 505, \
			230,	 295,	 274,	 150,	 501,	 433,	 259,	 101, \
			81,	 391,	 472,	 265,	  79,	 258,	 266,	 257, \
			369,	  65,	  88,	 436,	 489,	 442,	 246,	 154, \
			28,	  43,	  81,	 145,	 262,	  27,	  67,	 143, \
			414,	 132,	 131,	 119,	 416,	 254,	 112,	 384, \
			439,	 117,	 121,	 366,	 186,	  28,	 113,	 117, \
			90,	 133,	  27,	 129,	 232,	 152,	 146,	  96, \
			43,	  96,	  68,	  29,	 141,	 186,	 430,	 139, \
			432,	 124,	 155,	  93,	 238,	 139,	  94,	 286, \
			376,	 365,	 147,	  30,	 150,	  86,	  78,	 152, \
			80,	 415,	 150,	 412,	  81,	 547,	 417,	 154, \
			74,	 433,	  78,	 145,	  78,	  51,	 228,	 143, \
			254,	 404,	 249,	  45,	 323,	 497,	  79,	 469, \
			285,	 125,	 132,	 131,	 224,	 468,	  69,	  96, \
			527,	 154,	  38,	  29,	 141,	 145,	 146,	 373, \
			87,	 143,	 533,	 403,	 484,	 397,	 410,	 139, \
			139,	  43,	 155,	  40,	 510,	 422,	  67,	  97, \
			25,	 533,	 445,	 152,	 150,	 150,	  24,	 259, \
			146,	 156,	  78,	 147,	 265,	  28,	 258,	 266, \
			257,	 139,	  27,	 355,	 155,	  81,	 462,	  96, \
			496,	 561,	  79,	  81,	 141,	 262,	 150,	  48, \
			405,	 124,	  23,	  47,	  86,	 154,	  94,	 109, \
			41,	 145,	 571,	  30,	  39,	 143,	  22,	 568, \
			80,	  21,	 423,	 424,	 168,	 552,	  51,	  42, \
			12,	 116,	  78,	  53,	  45,	 548,	 549,	 550, \
			52,	 156,	  96,	  50,	 146,	 553,	 554,	 265, \
			68,	 125,	 266,	 147,	 124,	 139,	  69,	  87, \
			155,	  44,	   4,	  29,	  67,	 555,	   1,	 519, \
			262,	 152,	 150,	  80,	 565,	   0,	 254,	 564, \
			522,	 523,	   0,	  28,	 419,	 147,	 536,	 573, \
			27,	   0,	   0,	 586,	 569,	  96,	   0,	   0, \
			102,	 156,	 141,	 589,	 125,	 533,	 594,	 124, \
			592,	   0,	  54,	 154,	  94,	 240,	 139,	 145, \
			0,	  30,	 501,	 143,	  47,	   0,	  80,	 141, \
			485,	  41,	  28,	 150,	 595,	  39,	  64,	  27, \
			78,	 491,	 492,	 286,	  96,	 538,	 152,	   0, \
			42,	 141,	 146,	  80,	 187,	   0,	 124,	 125, \
			516,	 147,	 517,	 139,	  69,	  78,	 155,	 307, \
			0,	  29,	 217,	  81,	  51,	  80,	  28,	   0, \
			150,	 209,	  45,	  27,	 285,	  67,	   0,	 344, \
			154,	   0,	 599,	 600,	 145,	 579,	   0,	   0, \
			214,	   0,	 405,	  75,	  74,	 208,	 125,	 156, \
			152,	   0,	 539,	 540,	   0,	 265,	  96,	   0, \
			266,	   0,	 209,	 141,	 209,	  32,	   0,	 146, \
			124,	   0,	 101,	  68,	 156,	  94,	 262,	  79, \
			139,	   0,	  30,	 155,	 284,	   0,	 273,	  80, \
			381,	  86,	 154,	   0,	 382,	 150,	 145,	 318, \
			0,	  78,	 143,	   0,	   0,	   0,	 119,	 147, \
			0,	 112,	  47,	 213,	 117,	 121,	 344,	  41, \
			125,	 113,	   0,	  39,	 133,	  69,	 129,	   0, \
			284,	 146,	  29,	   0,	   0,	  68,	  42,	 209, \
			0,	   0,	 139,	 287,	  87,	 155,	  93,	  96, \
			0,	 450,	 453,	 254,	 141,	  96,	   0,	 150, \
			152,	 124,	 141,	 350,	   0,	   0,	  94,	 124, \
			156,	 464,	 465,	 230,	 483,	  65,	   0,	 584, \
			80,	   0,	 101,	 184,	 147,	 253,	  80,	  79, \
			0,	   0,	  78,	 139,	   0,	 132,	 131,	 405, \
			0,	 152,	 154,	 378,	 313,	 217,	 145,	 388, \
			150,	 125,	 143,	   0,	 209,	  28,	 119,	 125, \
			0,	 112,	  27,	 101,	 117,	 121,	   0,	  43, \
			79,	 113,	   0,	   0,	 133,	 141,	 129,	   0, \
			208,	 146,	   0,	 154,	 254,	  68,	 147,	 145, \
			486,	  72,	 139,	 143,	   0,	 155,	  93,	 119, \
			81,	 156,	 112,	 140,	   0,	 117,	 121,	 150, \
			152,	 541,	 113,	 543,	 544,	 133,	   0,	 129, \
			0,	 308,	 146,	   0,	 139,	   0,	  68,	 428, \
			0,	   0,	 265,	 139,	   0,	 266,	 155,	  93, \
			0,	 150,	 307,	   0,	  78,	 132,	 131,	 224, \
			150,	 152,	 154,	 262,	   0,	 380,	 145,	 409, \
			0,	  26,	 143,	   0,	   0,	 386,	 227,	   3, \
			0,	   0,	 186,	 387,	 158,	 160,	 161,	   0, \
			79,	 156,	 141,	   0,	 267,	 269,	 132,	 131, \
			43,	 146,	  86,	 154,	   0,	   0,	 147,	 145, \
			272,	   0,	 139,	 143,	   0,	 155,	  80,	 119, \
			81,	 349,	 112,	 156,	   0,	 117,	 121,	 150, \
			78,	   2,	 113,	 265,	 254,	 133,	 266,	 129, \
			0,	 162,	 146,	   0,	 152,	   0,	  68,	 147, \
			547,	   0,	   0,	 139,	 262,	  87,	 155,	 230, \
			358,	  81,	 361,	 363,	 105,	 245,	 101,	   0, \
			150,	 392,	   0,	  79,	 139,	   0,	   0,	 217, \
			0,	 191,	 360,	 281,	 338,	   0,	 154,	   0, \
			0,	 150,	 145,	   0,	 345,	 347,	 143,	 156, \
			141,	   0,	 119,	   0,	   0,	 112,	 132,	 131, \
			117,	 121,	   0,	   0,	 320,	 113,	 147,	   0, \
			133,	   0,	 129,	   0,	   0,	 146,	 152,	   0, \
			307,	  68,	   0,	   0,	 215,	   0,	 139,	   0, \
			0,	 155,	  93,	 227,	   0,	  76,	  43,	 447, \
			449,	   0,	   0,	 150,	   0,	  79,	  28,	 147, \
			152,	   0,	 209,	  27,	 227,	 426,	 427,	   0, \
			154,	  81,	   0,	 265,	 145,	 141,	 266,	 357, \
			143,	   0,	 101,	   0,	 475,	   0,	 562,	  79, \
			402,	 132,	 131,	 327,	 262,	   0,	   0,	   0, \
			487,	  67,	 154,	   0,	   0,	 156,	 145,	 146, \
			0,	   0,	 143,	  68,	   0,	   0,	 119,	 152, \
			139,	 112,	 226,	 155,	 117,	 121,	 499,	   0, \
			0,	 113,	  96,	   0,	 133,	 150,	 129,	 141, \
			0,	 146,	 147,	   0,	 124,	  68,	 388,	 476, \
			477,	  94,	 139,	   0,	  81,	 155,	  93,	 278, \
			0,	 154,	 500,	  80,	   0,	 145,	 227,	 150, \
			152,	 214,	   0,	   0,	   0,	  78,	 108,	 413, \
			0,	 227,	 156,	 512,	 513,	 207,	 514,	   0, \
			141,	   0,	   0,	   0,	 125,	   0,	 215,	   0, \
			146,	  69,	   0,	   0,	  68,	 132,	 131,	 215, \
			0,	 139,	 154,	   0,	 155,	 152,	 145,	   0, \
			0,	 542,	 143,	   0,	 147,	   0,	 150,	   0, \
			215,	 551,	   0,	   0,	   0,	   0,	   0,	 338, \
			0,	 215,	  96,	   0,	 156,	   0,	 503,	 141, \
			0,	 146,	 222,	 320,	 124,	  68,	 147,	 154, \
			0,	  94,	 139,	 145,	   0,	 155,	 400,	 143, \
			81,	  28,	   0,	  80,	 411,	   0,	  27,	 150, \
			0,	 141,	   0,	  96,	 418,	  78,	   0,	   0, \
			141,	   0,	   0,	   0,	 152,	 124,	 146,	   0, \
			0,	   0,	  94,	   0,	 125,	   0,	   0,	 139, \
			226,	   0,	 155,	   0,	  80,	 147,	 101,	 315, \
			0,	 278,	   0,	  79,	 150,	 152,	  78,	 394, \
			315,	   0,	   0,	   0,	   0,	 278,	 154,	   0, \
			0,	   0,	 145,	   0,	   0,	 125,	 143,	   0, \
			0,	   0,	 119,	 574,	 156,	 112,	   0,	 141, \
			117,	 121,	   0,	   0,	 400,	 113,	 147,	 154, \
			133,	   0,	 129,	 145,	 227,	 146,	   0,	 143, \
			0,	  68,	   0,	   0,	   0,	   0,	 139,	   0, \
			444,	 155,	  93,	  96,	   0,	 156,	   0,	   0, \
			141,	   0,	   0,	 150,	 152,	 124,	 146,	   0, \
			0,	   0,	 596,	 147,	  26,	 222,	   0,	 139, \
			0,	 141,	 155,	   0,	  80,	   0,	   9,	   0, \
			461,	   0,	   0,	  79,	 150,	   0,	  78,	 163, \
			400,	 132,	 131,	   0,	   0,	  86,	 154,	 171, \
			172,	   0,	 145,	   0,	   0,	 125,	 143,	 254, \
			0,	   0,	 119,	   0,	 156,	 112,	   0,	   0, \
			117,	 121,	   0,	   0,	 531,	 113,	  96,	 537, \
			133,	   0,	 129,	 141,	   0,	 146,	   0,	   0, \
			124,	  68,	 147,	   0,	 206,	  94,	 139,	 139, \
			87,	 155,	 400,	   0,	  81,	 156,	   0,	  80, \
			0,	   0,	   0,	 150,	 150,	   0,	   0,	   0, \
			0,	  78,	   0,	 147,	   0,	   0,	 535,	   0, \
			0,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			125,	   0,	   0,	 229,	   0,	   0,	   0,	 227, \
			227,	 132,	 131,	   0,	   0,	   0,	   0,	   0, \
			0,	 548,	   0,	   0,	   0,	 141,	   0,	   0, \
			0,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	 152,	   0,	   0,	   0, \
			156,	   0,	  96,	   0,	   0,	   0,	 265,	 141, \
			0,	 266,	 147,	  78,	 124,	   0,	   0,	   0, \
			0,	  94,	   0,	  79,	  81,	   0,	 401,	 262, \
			0,	   0,	   0,	  80,	   0,	  86,	 154,	 585, \
			0,	 370,	 145,	   0,	   0,	  78,	 143,	  28, \
			0,	   0,	 119,	   0,	  27,	 112,	   0,	 524, \
			117,	 121,	   0,	   0,	 125,	 113,	 141,	 152, \
			133,	   0,	 129,	   0,	   0,	 146,	   0,	   0, \
			0,	  68,	 156,	   0,	   0,	   0,	 139,	   0, \
			87,	 155,	   0,	   0,	   0,	 545,	  79,	   0, \
			28,	   0,	   0,	 150,	   0,	  27,	   0,	   0, \
			0,	 154,	   0,	   0,	 156,	 145,	   0,	 141, \
			0,	 143,	   0,	   0,	   0,	 119,	   0,	 560, \
			112,	   0,	   0,	 117,	 121,	   0,	 566,	 567, \
			113,	 132,	 131,	 133,	   0,	 129,	   0,	   0, \
			146,	   0,	   0,	   0,	  68,	   0,	   0,	   0, \
			0,	 139,	 119,	   0,	 155,	 112,	   0,	   0, \
			117,	 121,	   0,	 156,	   0,	 113,	 150,	 101, \
			133,	 577,	 129,	   0,	  79,	   0,	   0,	   0, \
			0,	   0,	 147,	   0,	 290,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	  81,	   0,	   0,	   0, \
			0,	   0,	   0,	 119,	 132,	 131,	 112,	   0, \
			0,	 117,	 121,	   0,	 156,	   0,	 113,	   0, \
			152,	 133,	   0,	 129,	   0,	   0,	  96,	   0, \
			0,	   0,	   0,	 141,	 588,	   0,	 590,	 591, \
			124,	 132,	 131,	  93,	 460,	  94,	   0,	  79, \
			0,	   0,	   0,	   0,	   0,	 147,	   0,	  80, \
			0,	 156,	 154,	   0,	 141,	   0,	 145,	  81, \
			0,	  78,	 143,	   0,	   0,	   0,	 119,	   0, \
			0,	 112,	 101,	   0,	 117,	 121,	   0,	  79, \
			125,	 113,	 132,	 131,	 133,	 254,	 129,	   0, \
			0,	 146,	   0,	   0,	  81,	  68,	   0,	 117, \
			0,	   0,	 139,	   0,	   0,	 155,	 119,	   0, \
			0,	 112,	   0,	   0,	 117,	 121,	   0,	 150, \
			254,	 113,	   0,	   0,	 133,	 139,	 129,	   0, \
			156,	 101,	 117,	 141,	 141,	   0,	  79,	   0, \
			124,	   0,	 150,	   0,	   0,	  81,	  93,	   0, \
			0,	   0,	   0,	   0,	   0,	 132,	 131,	  80, \
			139,	 156,	   0,	   0,	   0,	 119,	   0,	   0, \
			112,	  78,	   0,	 117,	 121,	 150,	   0,	   0, \
			113,	 228,	   0,	 133,	   0,	 129,	   0,	   0, \
			125,	   0,	   0,	   0,	 119,	 132,	 131,	 112, \
			0,	 254,	 117,	 121,	   0,	  93,	 147,	 113, \
			0,	   0,	 133,	 117,	 129,	   0,	   0,	 259, \
			534,	   0,	   0,	   0,	 265,	   0,	 258,	 266, \
			257,	   0,	   0,	   0,	   0,	   0,	   0,	 246, \
			156,	 139,	   0,	  81,	   0,	 262,	   0,	 369, \
			0,	   0,	 259,	 254,	 132,	 131,	 150,	 265, \
			81,	 258,	 266,	 257,	   0,	 117,	   0,	   0, \
			0,	  86,	 246,	   0,	 547,	   0,	  81,	   0, \
			262,	   0,	   0,	 132,	 131,	   0,	 119,	   0, \
			0,	 112,	   0,	 139,	 117,	 121,	   0,	   0, \
			0,	 113,	   0,	   0,	 133,	   0,	 129,	   0, \
			150,	   0,	   0,	 141,	   0,	   0,	   0,	  81, \
			124,	   0,	   0,	   0,	  87,	   0,	   0,	   0, \
			0,	 242,	   0,	 259,	   0,	   0,	   0,	  80, \
			265,	   0,	 258,	 266,	 257,	   0,	  81,	 119, \
			289,	  78,	 112,	 246,	   0,	 117,	 121,	  81, \
			0,	 262,	 113,	   0,	  60,	 133,	   0,	 129, \
			125,	 119,	   0,	   0,	 112,	 132,	 131,	 117, \
			121,	  96,	   0,	   0,	 113,	 259,	 141,	 133, \
			0,	 129,	 265,	 124,	 258,	 266,	 257,	   0, \
			0,	  82,	   0,	   0,	   0,	 246,	   0,	   0, \
			0,	  81,	  80,	 262,	   0,	 193,	  96,	   0, \
			156,	   0,	   0,	   0,	  78,	   0,	   0,	   0, \
			124,	   0,	   0,	 210,	  61,	   0,	 132,	 131, \
			81,	   0,	   0,	 125,	   0,	   0,	   0,	  80, \
			183,	   0,	   0,	 195,	   0,	   0,	   0,	 232, \
			132,	 131,	   0,	   0,	   0,	   0,	   0,	  96, \
			0,	   0,	   0,	   0,	 210,	   0,	 210,	   0, \
			125,	 124,	 292,	 181,	   0,	   0,	  94,	   0, \
			0,	   0,	   0,	 156,	 303,	   0,	   0,	   0, \
			80,	  81,	   0,	   0,	   0,	   0,	   0,	   0, \
			0,	   0,	  78,	 279,	   0,	   0,	 288,	   0, \
			0,	   0,	   0,	  81,	   0,	   0,	   0,	   0, \
			0,	 125,	   0,	   0,	   0,	   0,	   0,	   0, \
			309,	   0,	   0,	   0,	   0,	   0,	   0,	 141, \
			0,	 210,	   0,	   0,	 124,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	   0,	  96,	   0,	 305, \
			0,	   0,	 141,	 310,	   0,	 314,	   0,	 124, \
			0,	   0,	  96,	   0,	 348,	  78,	 314,	   0, \
			0,	   0,	   0,	   0,	 124,	   0,	  80,	   0, \
			96,	  94,	   0,	   0,	 125,	 141,	   0,	   0, \
			0,	   0,	 124,	  80,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	   0,	  78,	 210,	 125, \
			0,	  80,	   0,	   0,	   0,	   0,	   0,	 364, \
			0,	  96,	   0,	   0,	 125,	 374,	   0,	   0, \
			0,	   0,	   0,	 124,	 156,	   0,	   0,	   0, \
			94,	 359,	 125,	 362,	   0,	   0,	   0,	   0, \
			96,	   0,	  80,	   0,	   0,	   0,	   0,	   0, \
			0,	  96,	 124,	   0,	  78,	   0,	 141,	   0, \
			0,	 364,	   0,	 124,	   0,	   0,	   0,	   0, \
			0,	  80,	   8,	 125,	   0,	   0,	   0,	  55, \
			0,	   0,	  80,	   0,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	 421,	   0,	   0,	   0, \
			458,	   0,	 125,	  96,	   0,	   0,	   0,	   0, \
			141,	   0,	   0,	 125,	   0,	 124,	   0,	   0, \
			0,	   0,	 451,	 452,	   0,	   0,	 185,	   0, \
			194,	   0,	  96,	   0,	  80,	 279,	   0,	   0, \
			0,	   0,	 216,	   0,	 124,	   0,	 211,	   0, \
			0,	 220,	   0,	 185,	 211,	   0,	   0,	   0, \
			474,	   0,	   0,	  80,	   0,	 125,	   0,	 481, \
			0,	   0,	 268,	 268,	   0,	   0,	   0,	 185, \
			0,	   0,	   0,	   0,	   0,	   0,	 268,	 211, \
			0,	 211,	   0,	  96,	 125,	 268,	   0,	   0, \
			478,	 479,	   0,	   0,	   0,	 124,	   0,	 268, \
			0,	   0,	   0,	   0,	   0,	  96,	   0,	 319, \
			185,	   0,	   0,	   0,	  80,	   0,	   0,	 124, \
			0,	 185,	   0,	   0,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	   0,	   0,	  80,	   0, \
			0,	   0,	 185,	   0,	   0,	 125,	   0,	 351, \
			0,	 346,	   0,	   0,	 211,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	   0,	   0,	   0,	 125, \
			0,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			0,	   0,	 303,	   0,	 210,	 526,	   0,	   0, \
			0,	   0,	   0,	   0,	 216,	 185,	   0,	   0, \
			0,	   0,	   0,	 303,	 185,	 216,	 185,	   0, \
			0,	 194,	   0,	   0,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	   0,	   0,	 216,	   0, \
			0,	 211,	 211,	   0,	 220,	   0,	 389,	 216, \
			0,	   0,	   0,	 220,	   0,	   0,	   0,	   0, \
			0,	 220,	   0,	   0,	 189,	  89,	   0,	 220, \
			0,	  89,	  89,	  89,	  89,	  89,	   0,	   0, \
			408,	   0,	   0,	   0,	   0,	  89,	  89,	  89, \
			0,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			0,	 185,	   0,	   0,	   0,	 575,	   0,	 216, \
			0,	   0,	 185,	   0,	  89,	   0,	   0,	   0, \
			0,	   0,	 220,	 220,	   0,	   0,	   0,	   0, \
			0,	   0,	  89,	  89,	   0,	 303,	 219,	   0, \
			0,	 231,	   0,	 268,	 268,	 120,	 597,	 220, \
			0,	   0,	   0,	   0,	 260,	   0,	 319,	 268, \
			0,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			0,	   0,	 185,	 185,	  89,	 185,	  89,	   0, \
			0,	 598,	 291,	   0,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			198,	   0,	   0,	   0,	   0,	 216,	 260,	   0, \
			0,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	   0,	   0,	  89,	   0, \
			0,	   0,	   0,	   0,	   0,	 256,	   0,	   0, \
			0,	   0,	   0,	 185,	   0,	   0,	   0,	   0, \
			0,	  89,	   0,	   0,	   0,	   0,	   0,	   0, \
			216,	   0,	   0,	   0,	  89,	   0,	 389,	   0, \
			0,	   0,	   0,	 408,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	   0,	   0,	 408,	 256, \
			0,	   0,	   0,	   0,	   0,	 408,	   0,	   0, \
			0,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			0,	   0,	 260,	   0,	  89,	  89,	   0,	   0, \
			0,	  89,	   0,	   0,	  89,	   0,	  89,	 231, \
			0,	 219,	  89,	 219,	   0,	 268,	   0,	 211, \
			219,	 220,	   5,	   0,	   0,	   0,	 219,	 159, \
			0,	   0,	 268,	   0,	 231,	   0,	 268,	 166, \
			167,	 169,	 170,	   0,	   0,	   0,	   0,	 260, \
			0,	   0,	 260,	   0,	   0,	   0,	 185,	   0, \
			174,	 175,	 176,	   0,	   0,	   0,	   0,	   0, \
			260,	 260,	 260,	 256,	   0,	   0,	 260,	   0, \
			0,	   0,	 203,	   0,	   0,	   0,	   0,	 219, \
			219,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	 233,	   0,	 234,	 235, \
			236,	   0,	   0,	   0,	 219,	 389,	 408,	   0, \
			0,	 270,	   0,	   0,	 408,	   0,	   0,	   0, \
			256,	   0,	 138,	 256,	   0,	   0,	   0,	   0, \
			0,	 293,	   0,	 294,	   0,	   0,	   0,	   0, \
			301,	 256,	 256,	 256,	   0,	   0,	   0,	 256, \
			268,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			321,	 268,	 322,	   0,	   0,	 325,	   0,	 326, \
			0,	   0,	   0,	   0,	 408,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	   0,	   0,	 341,	   0, \
			343,	   0,	   0,	   0,	 268,	 268,	 268,	   0, \
			352,	 353,	   0,	   0,	   0,	   0,	 356,	   0, \
			0,	   0,	 251,	   0,	 110,	   0,	   0,	   0, \
			0,	   0,	   0,	 219,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	   0,	 260,	   0,	   0, \
			0,	 260,	   0,	   0,	 260,	   0,	   0,	   0, \
			260,	 260,	 260,	 260,	   0,	 260,	 260,	   0, \
			190,	  59,	   0,	 260,	 251,	  59,	  59,	  59, \
			59,	  59,	   0,	   0,	   0,	   0,	   0,	   0, \
			0,	  59,	  59,	  59,	   0,	   0,	   0,	   0, \
			136,	   0,	   0,	 393,	  89,	   0,	 219,	 395, \
			0,	 396,	   0,	   0,	 261,	   0,	   0,	   0, \
			59,	 398,	   0,	   0,	   0,	   0,	 256,	   0, \
			0,	   0,	 256,	   0,	   0,	 256,	  59,	   0, \
			0,	 256,	 256,	 256,	 256,	   0,	 256,	 256, \
			0,	 425,	   0,	   0,	 256,	   0,	   0,	   0, \
			255,	   0,	   0,	   0,	   0,	   0,	 261,	 446, \
			0,	   0,	   0,	   0,	   0,	   0,	 454,	 455, \
			251,	 456,	   0,	   0,	 457,	   0,	   0,	   0, \
			264,	   0,	   0,	 463,	   0,	   0,	 466,	 467, \
			0,	   0,	 219,	   0,	   0,	   0,	 260,	 470, \
			260,	 317,	 255,	   0,	   0,	   0,	   0,	 260, \
			0,	   0,	 317,	   0,	   0,	   0,	   0,	   0, \
			0,	   0,	  59,	 251,	 260,	 493,	   0,	   0, \
			251,	 251,	 264,	 498,	   0,	   0,	 251,	   0, \
			0,	 251,	   0,	   0,	   0,	   0,	 251,	   0, \
			0,	   0,	   0,	   0,	 251,	   0,	 511,	   0, \
			59,	 339,	 261,	   0,	   0,	   0,	   0,	   0, \
			0,	 339,	 339,	   0,	 264,	   0,	   0,	 256, \
			0,	 256,	   0,	   0,	   0,	   0,	 317,	   0, \
			256,	   0,	   0,	 521,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	 144,	 256,	 255,	   0, \
			59,	  59,	   0,	   0,	 528,	  59,	   0,	 261, \
			59,	 251,	 261,	   0,	   0,	   0,	  59,	   0, \
			0,	   0,	   0,	   0,	   0,	   0,	 264,	   0, \
			261,	 261,	 261,	   0,	   0,	   0,	 261,	   0, \
			0,	   0,	   0,	   0,	 556,	   0,	   0,	 557, \
			0,	   0,	 558,	 255,	   0,	 559,	 255,	   0, \
			0,	   0,	   0,	 563,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	 255,	 255,	 255,	 570, \
			0,	 264,	 255,	   0,	 263,	 251,	 264,	 264, \
			0,	   0,	   0,	 572,	 264,	   0,	   0,	 264, \
			0,	   0,	   0,	   0,	 264,	   0,	 576,	   0, \
			264,	 264,	 264,	 251,	   0,	   0,	   0,	   0, \
			0,	 251,	 251,	 251,	 251,	   0,	 251,	   0, \
			580,	   0,	   0,	   0,	 582,	   0,	 263,	 583, \
			0,	 251,	   0,	 317,	 317,	   0,	   0,	 251, \
			0,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			0,	 587,	   0,	   0,	   0,	   0,	   0,	 264, \
			263,	   0,	   0,	   0,	   0,	   0,	 593,	   0, \
			0,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			339,	   0,	   0,	   0,	 339,	 261,	   0,	   0, \
			0,	 261,	   0,	 339,	 261,	   0,	   0,	   0, \
			261,	 261,	 261,	 261,	   0,	 261,	 261,	   0, \
			0,	   0,	   0,	 261,	   0,	   0,	   0,	   0, \
			0,	   0,	 263,	   0,	   0,	   0,	   0,	   0, \
			0,	 255,	   0,	 264,	   0,	 255,	   0,	   0, \
			255,	   0,	   0,	   0,	 255,	 255,	 255,	 255, \
			0,	 255,	 255,	   0,	 251,	   0,	 251,	 255, \
			0,	 264,	   0,	   0,	   0,	 251,	   0,	 264, \
			264,	 264,	 264,	   0,	 264,	 263,	   0,	   0, \
			0,	   0,	 263,	 263,	   0,	   0,	   0,	 264, \
			263,	   0,	   0,	 263,	   0,	 264,	   0,	   0, \
			263,	   0,	   0,	   0,	 263,	 263,	 263,	 103, \
			0,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	   0,	   0,	   0,	 317, \
			188,	  57,	   0,	   0,	   0,	  57,	  57,	  57, \
			57,	  57,	   0,	   0,	   0,	   0,	 261,	   0, \
			261,	  57,	  57,	  57,	   0,	   0,	 180,	 261, \
			192,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	 263,	 261,	   0,	   0,	   0, \
			57,	 218,	   0,	 221,	   0,	   0,	   0,	   0, \
			0,	   0,	 255,	   0,	 255,	   0,	  57,	 212, \
			0,	   0,	 212,	 255,	   0,	 212,	   0,	 271, \
			0,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			255,	   0,	 264,	   0,	 264,	   0,	   0,	   0, \
			0,	   0,	   0,	 264,	   0,	   0,	   0,	 264, \
			212,	   0,	 212,	   0,	   0,	   0,	   0,	 263, \
			316,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			0,	 316,	   0,	   0,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	   0,	 263,	   0,	   0, \
			0,	   0,	 340,	 263,	 263,	 263,	 263,	   0, \
			263,	   0,	  57,	   0,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	 263,	   0,	   0,	   0,	   0, \
			0,	 263,	   0,	   0,	   0,	 212,	   0,	   0, \
			0,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			57,	   0,	   0,	   0,	   0,	 316,	   0,	   0, \
			0,	   0,	   0,	   0,	 218,	   0,	 221,	   0, \
			0,	 372,	   0,	   0,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	 218,	   0,	   0,	   0, \
			57,	  57,	   0,	   0,	   0,	  57,	   0,	   0, \
			57,	   0,	 212,	 212,	   0,	 212,	  57,	 390, \
			0,	   0,	   0,	   0,	 212,	   0,	   0,	   0, \
			0,	   0,	 212,	   0,	   0,	   0,	   0,	   0, \
			212,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			0,	 420,	   0,	   0,	   0,	   0,	 263,	   0, \
			263,	   0,	 429,	   0,	   0,	   0,	   0,	 263, \
			0,	   0,	   0,	 263,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	 212,	 212,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			212,	   0,	 316,	 316,	   0,	 480,	   0,	   0, \
			0,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	 515,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	   0,	   0,	   0,	 390, \
			0,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			212,	   0,	 212,	   0,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	   0,	   0,	 316,	   0, \
			0,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	   0,	   0,	   0,	   0, \
			0,	   0,	   0,	   0,	   0,	   0,	 390, \
		)
		_YYPACT = (
			-504,   -1000,	-413,   -1000,	-400,	-314,	-314,	-504, \
			-217,   -1000,	-387,	-387,	 165,	  47,	 165,	 165, \
			-217,	-217,	 203,   -1000,   -1000,   -1000,   -1000,   -1000, \
			-1000,   -1000,   -1000,   -1000,   -1000,	 165,	 165,	-473, \
			-1000,	-515,	-517,   -1000,   -1000,   -1000,	 412,	-504, \
			759,	1079,	-663,   -1000,	-560,   -1000,	-380,	 165, \
			-1000,   -1000,	-936,	-518,   -1000,	-217,	 571,	 153, \
			-1000,	-448,   -1000,	1179,	-144,	-581,   -1000,   -1000, \
			-1000,	 165,   -1000,	 165,	 165,	 165,	-207,	1290, \
			-1000,   -1000,	1258,	1258,   -1000,   -1000,	 165,	 545, \
			-1000,   -1000,   -1000,   -1000,   -1000,   -1000,	1258,	 759, \
			-963,	 759,   -1000,	-908,	1404,	1258,	 165,   -1000, \
			165,   -1000,   -1000,	-947,	-909,	 165,   -1000,	1211, \
			-1000,   -1000,	-470,   -1000,   -1000,	 379,	1355,   -1000, \
			847,	1290,   -1000,   -1000,	-921,	 165,   -1000,	 165, \
			-207,	 991,	 165,   -1000,	 165,   -1000,   -1000,   -1000, \
			-1000,	-504,	-998,	-658,	-661,	-656,	-362,   -1000, \
			784,   -1000,	 545,	 165,	-386,	 165,   -1000,	 784, \
			696,	 -54,	1079,	-486,	 324,	 165,	 165,   -1000, \
			-1000,   -1000,	-545,	 -50,   -1000,   -1000,   -1000,	-314, \
			-1000,   -1000,   -1000,   -1000,   -1000,	-387,   -1000,   -1000, \
			-1000,   -1000,   -1000,   -1000,   -1000,   -1000,   -1000,   -1000, \
			-1000,   -1000,   -1000,   -1000,	 -89,	-293,	 -89,	-106, \
			-1000,	 659,   -1000,   -1000,	 545,	1079,	1179,	-188, \
			-206,	 479,	 659,	1281,	-203,	1290,	-203,	 203, \
			203,   -1000,   -1000,   -1000,	 203,   -1000,	-196,	 203, \
			-1000,	 759,	 291,	 618,	-448,	 203,	-448,   -1000, \
			-516,   -1000,   -1000,	-448,	 618,	-183,   -1000,   -1000, \
			165,	-448,   -1000,   -1000,	 165,   -1000,	 165,	1050, \
			-470,   -1000,   -1000,   -1000,   -1000,   -1000,	 165,   -1000, \
			848,   -1000,	-357,	-391,   -1000,	-275,	 429,	-908, \
			-1000,   -1000,   -1000,	 429,	-909,   -1000,	 429,   -1000, \
			-207,	 545,	1079,	1332,	-357,	-357,	 165,	-486, \
			-486,	1290,	 545,	-384,	-896,	 -41,   -1000,	-136, \
			-122,	-160,	-448,	-448,	 165,	-970,	-970,	-970, \
			1079,	1079,	1079,	 165,	 165,   -1000,	 165,   -1000, \
			-1000,	 165,   -1000,	1258,	1120,   -1000,   -1000,	-448, \
			165,	1079,	1079,	 165,	 165,   -1000,   -1000,	1211, \
			-1000,	-581,	 784,	-921,	 165,	-187,	1422,   -1000, \
			-183,   -1000,	-293,	   6,	-470,	1050,	 244,	 784, \
			784,   -1000,   -1000,   -1000,	-183,   -1000,   -1000,	-171, \
			784,	 784,	 165,	-666,   -1000,	-494,	 784,	 696, \
			165,   -1000,   -1000,	 696,	-970,   -1000,   -1000,   -1000, \
			92,   -1000,	 -80,   -1000,	-200,   -1000,	-181,	-531, \
			-1000,   -1000,   -1000,	 165,   -1000,   -1000,   -1000,	-197, \
			-106,   -1000,	-197,   -1000,	-970,   -1000,   -1000,   -1000, \
			-1000,   -1000,   -1000,	 545,	-206,   -1000,	-206,   -1000, \
			-1000,   -1000,	 -79,   -1000,   -1000,   -1000,   -1000,   -1000, \
			165,   -1000,	-196,	-196,	-170,	-525,	-502,   -1000, \
			-470,   -1000,   -1000,   -1000,   -1000,   -1000,   -1000,   -1000, \
			-275,	 165,   -1000,   -1000,	-357,   -1000,	 429,	1198, \
			429,	 429,   -1000,	-275,	-357,	-357,	-357,	-970, \
			-357,	-357,	-239,   -1000,	-214,	-214,	1225,	-970, \
			-187,   -1000,   -1000,   -1000,	 317,	-214,   -1000,   -1000, \
			-125,	 165,   -1000,   -1000,	 165,   -1000,   -1000,	 165, \
			-1000,   -1000,	 165,   -1000,	-170,	1211,   -1000,	 759, \
			165,	-448,	1079,	-170,	-170,   -1000,   -1000,   -1000, \
			-1000,   -1000,	1120,	-885,	 165,   -1000,	1211,   -1000, \
			-1000,   -1000,   -1000,   -1000,   -1000,   -1000,   -1000,   -1000, \
			165,   -1000,	-187,   -1000,   -1000,   -1000,	-293,	-581, \
			-470,   -1000,   -1000,	 165,   -1000,   -1000,	  92,   -1000, \
			-1000,   -1000,   -1000,   -1000,   -1000,   -1000,	-662,   -1000, \
			-1000,   -1000,   -1000,	 784,   -1000,	 165,   -1000,   -1000, \
			-628,	 165,   -1000,   -1000,	 165,   -1000,   -1000,   -1000, \
			-1000,   -1000,   -1000,	-206,   -1000,   -1000,   -1000,   -1000, \
			-1000,   -1000,   -1000,   -1000,   -1000,	-502,	-581,   -1000, \
			-1000,	-138,   -1000,	-275,   -1000,   -1000,	 165,   -1000, \
			-1000,	-239,	1198,	-170,	-170,   -1000,	  55,   -1000, \
			-1000,   -1000,   -1000,	 165,   -1000,   -1000,   -1000,	-357, \
			-1000,   -1000,   -1000,   -1000,   -1000,   -1000,   -1000,   -1000, \
			1211,   -1000,   -1000,   -1000,   -1000,   -1000,   -1000,   -1000, \
			-970,	1258,   -1000,   -1000,   -1000,   -1000,   -1000,	-581, \
			-1000,   -1000,   -1000,   -1000,   -1000,   -1000,   -1000,   -1000, \
			-1000,	-921,   -1000,   -1000,   -1000,   -1000,   -1000,   -1000, \
			-1000,   -1000,   -1000,   -1000,	1258,	1120,	1120,   -1000, \
			-1000, \
		)
		_YYPGO = (
				 0,	 598,	 977,	 935,	 594,	2698,	 214,	2242, \
				1374,	 220,	 189,	 234,	 261,	 725,	 593,	 543, \
				579,	 576,	 571,	 221,	 634,	2247,	 232,	3376, \
				194,	2896,	1972,	 181,	2028,	 170,	 175,	 654, \
				568,	 561,	 558,	 546,	 518,	 512,	 507,	3359, \
				299,	2001,	 165,	 490,	 819,	 836,	 449,	1069, \
				188,	2476,	 793,	 424,	 394,	 378,	1162,	  91, \
				238,	 157,	 377,	 624,	 873,	 372,	 364,	 362, \
				360,	 787,	 100,	 160,	 356,	 211,	 927,	 511, \
				153,	 159,	 209,	 351,	 347,	1174,	2860,	 140, \
				346,	 637,	 343,	 342,	 339,	 182,	 268,	 337, \
				333,	1004,	 172,	 551,	 331,	 569,	 328,	 201, \
				323,	 319,	 180,	2920,	2786,	 141,	 318,	 883, \
				314,	3092,	 306,	 821,	 305,	 302,	 164,	 208, \
				355,	 200,	 298,	  87,	1005,	 256,	  90,	 301, \
				249,	  88,	 230,	 205,	  89,	 152,	 295,	 474, \
				78,	2541,	 294,	 289,	 284,	 212,	 192,	 275, \
				198,	 199,	 274,	 156,	 263,	 262,	 259,	 246, \
				236,	 235,	 136,	 223,	 222,	 207,	 168, \
			)
		_YYR1 = (
				 0,	   1,	   2,	   2,	   2,	   2,	   2,	   2, \
				 3,	   3,	   8,	   8,	   8,	   8,	  12,	  12, \
				13,	  13,	  14,	  14,	  14,	  15,	  15,	  15, \
				16,	  16,	  16,	  16,	  17,	  17,	  17,	  17, \
				17,	  17,	  17,	  17,	  17,	  17,	  20,	  20, \
				 5,	   5,	  32,	  32,	  32,	  32,	  32,	  35, \
				35,	  35,	  35,	  35,	  33,	  33,	  33,	  33, \
				33,	  33,	  33,	  34,	  31,	  31,	  48,	  48, \
				48,	  51,	  51,	  47,	  47,	  52,	  52,	  56, \
				56,	  57,	  57,	  59,	  59,	  59,	  55,	  55, \
				26,	  26,	  60,	  60,	  60,	  60,	  61,	  61, \
				62,	  62,	  41,	  41,	  41,	  68,	  68,	  71, \
				71,	  71,	  72,	  72,	  75,	  75,	  75,	  75, \
				76,	  76,	  77,	  77,	  77,	  77,	  77,	  77, \
				77,	  83,	  83,	  85,	  85,	  85,	  85,	  45, \
				45,	  45,	  45,	  45,	  28,	  28,	  86,	  86, \
				39,	  39,	  89,	  89,	  90,	  90,	  91,	  91, \
				93,	  93,	  93,	  94,	  94,	  94,	  95,	  95, \
				95,	  95,	  98,	  97,	  97,	 101,	 101,	 103, \
				103,	 103,	 103,	 103,	 103,	 103,	 103,	 103, \
				103,	  30,	  30,	  29,	  29,	  25,	  25,	  81, \
				81,	  81,	 115,	 115,	 118,	 118,	 118,	 120, \
				120,	 117,	 122,	 122,	 116,	 116,	 116,	 123, \
				123,	 124,	 124,	 107,	 107,	 107,	 107,	 107, \
				107,	 119,	 119,	 119,	 126,	 126,	 127,	 127, \
				127,	 128,	 128,	 128,	 128,	 128,	 128,	 128, \
				80,	  80,	  80,	   6,	   6,	 130,	 130,	 104, \
				104,	 131,	 131,	 131,	 131,	  11,	  11,	  11, \
				 4,	   4,	 133,	 133,	 134,	 134,	 134,	 134, \
				134,	 134,	 134,	  43,	  43,	  43,	 135,	 135, \
				136,	 136,	  67,	  67,	  67,	   7,	   7,	   7, \
				 7,	 108,	 108,	 139,	 139,	 139,	 139,	  84, \
				84,	 140,	 140,	 140,	 140,	 141,	 142,	 143, \
				38,	  38,	  92,	  92,	 102,	 102,	  23,	  23, \
				18,	  18,	 144,	 144,	  65,	  65,	  65,	  42, \
				42,	 121,	 121,	 121,	 109,	 109,	 109,	  19, \
				19,	  19,	  27,	  27,	  27,	  44,	  44,	 145, \
				145,	 145,	  40,	  40,	  66,	  66,	  66,	 112, \
				112,	 112,	 146,	 146,	  79,	  79,	  79,	  87, \
				87,	  87,	 106,	 106,	 106,	  54,	  54,	  54, \
				110,	 110,	 110,	  46,	  46,	  88,	  88,	  88, \
				113,	 114,	 114,	 114,	  82,	  82,	  82,	 125, \
				125,	 125,	 147,	 147,	 105,	 105,	 148,	 148, \
				99,	  99,	  78,	  78,	  78,	  36,	  36,	  36, \
				64,	  64,	  21,	  21,	  37,	  22,	  22,	  73, \
				73,	  69,	  69,	 138,	 137,	  49,	  49,	 100, \
				100,	 149,	 149,	  63,	  63,	  10,	  10,	 111, \
				58,	  58,	  53,	  53,	 150,	 150,	 150,	  50, \
				50,	 129,	  24,	  24,	   9,	   9,	  96,	  96, \
				74,	  74,	  70,	  70,	 132, \
			)
		_YYR2 = (
			0,	   2,	   1,	   2,	   2,	   2,	   3,	   2, \
			2,	   1,	   2,	   2,	   2,	   1,	   1,	   0, \
			1,	   3,	   1,	   3,	   2,	   1,	   3,	   2, \
			1,	   3,	   4,	   4,	   1,	   1,	   1,	   1, \
			2,	   1,	   1,	   1,	   1,	   1,	   2,	   3, \
			1,	   2,	   1,	   1,	   1,	   1,	   1,	   3, \
			3,	   4,	   5,	   4,	   3,	   4,	   4,	   3, \
			4,	   3,	   2,	   3,	   1,	   1,	   4,	   2, \
			1,	   3,	   2,	   1,	   5,	   1,	   4,	   1, \
			4,	   1,	   2,	   4,	   4,	   2,	   2,	   1, \
			1,	   2,	   1,	   1,	   1,	   1,	   2,	   2, \
			7,	   6,	   1,	   4,	   4,	   1,	   3,	   1, \
			3,	   3,	   1,	   4,	   1,	   2,	   3,	   4, \
			1,	   2,	   3,	   4,	   1,	   2,	   3,	   1, \
			1,	   3,	   3,	   1,	   2,	   2,	   3,	   1, \
			2,	   2,	   3,	   2,	   1,	   3,	   3,	   3, \
			2,	   1,	   1,	   2,	   1,	   3,	   1,	   2, \
			1,	   3,	   4,	   1,	   3,	   3,	   1,	   3, \
			1,	   2,	   4,	   1,	   3,	   1,	   2,	   1, \
			3,	   2,	   3,	   2,	   3,	   4,	   2,	   2, \
			3,	   3,	   4,	   2,	   3,	   2,	   3,	   1, \
			3,	   2,	   1,	   4,	   1,	   3,	   4,	   1, \
			2,	   3,	   1,	   1,	   1,	   3,	   4,	   1, \
			4,	   1,	   3,	   1,	   2,	   2,	   2,	   3, \
			3,	   1,	   4,	   4,	   1,	   3,	   1,	   3, \
			3,	   1,	   2,	   3,	   3,	   3,	   4,	   3, \
			1,	   2,	   2,	   1,	   2,	   1,	   2,	   1, \
			2,	   1,	   1,	   1,	   2,	   1,	   2,	   2, \
			1,	   2,	   1,	   2,	   1,	   1,	   2,	   2, \
			1,	   1,	   1,	   1,	   1,	   2,	   1,	   2, \
			1,	   2,	   1,	   1,	   2,	   1,	   2,	   1, \
			2,	   1,	   3,	   1,	   2,	   2,	   3,	   1, \
			2,	   1,	   1,	   1,	   3,	   4,	   2,	   3, \
			1,	   2,	   1,	   2,	   1,	   2,	   1,	   2, \
			1,	   2,	   1,	   1,	   1,	   2,	   1,	   1, \
			2,	   1,	   2,	   1,	   1,	   2,	   1,	   1, \
			2,	   1,	   1,	   2,	   1,	   1,	   1,	   1, \
			2,	   1,	   1,	   1,	   1,	   2,	   1,	   1, \
			2,	   1,	   1,	   1,	   1,	   2,	   1,	   1, \
			2,	   1,	   1,	   2,	   1,	   1,	   2,	   1, \
			1,	   2,	   1,	   1,	   1,	   1,	   2,	   1, \
			1,	   1,	   2,	   1,	   1,	   2,	   1,	   1, \
			2,	   1,	   1,	   1,	   1,	   2,	   1,	   2, \
			1,	   2,	   1,	   2,	   1,	   3,	   4,	   3, \
			1,	   1,	   1,	   3,	   1,	   1,	   2,	   1, \
			2,	   1,	   2,	   1,	   1,	   1,	   2,	   1, \
			2,	   1,	   2,	   1,	   2,	   1,	   2,	   1, \
			1,	   2,	   1,	   2,	   1,	   2,	   3,	   1, \
			2,	   1,	   1,	   2,	   1,	   2,	   1,	   2, \
			1,	   2,	   1,	   2,	   1, \
		)
		_YYCHK = (
			-1000,	  -1,	  -2,	  -3,	  -4,	  -5,	  -6,	 581, \
			-7,	  -8,	-133,	 535,	 -32,	-130,	-137,	-138, \
			-9,	 -10,	 -11,	 -12,	-134,	 -33,	 -34,	 -35, \
			-36,	 -37,	 517,	 930,	 925,	 995,	 955,	 584, \
			-13,	 612,	 515,	 618,	 524,	 536,	 -43,	 606, \
			-38,	 602,	 617,	 905,	 -14,	 525,	-135,	 597, \
			-15,	-136,	 -16,	 519,	 -17,	 -18,	 -20,	 -21, \
			-22,	 -23,	 -24,	 -25,	 -26,	 -28,	 -29,	 -30, \
			-31,	 610,	-150,	 910,	 578,	 990,	-111,	-113, \
			-60,	 -86,	 505,	 504,	 -47,	 -48,	 970,	 532, \
			960,	 677,	 -41,	 -61,	 -62,	 -63,	 542,	 585, \
			-52,	 -49,	 -51,	 -68,	 -64,	 587,	 950,	 -56, \
			935,	 -71,	-148,	 -57,	 -72,	 527,	 -59,	 -39, \
			-75,	 -89,	 -76,	 -90,	 -77,	 -91,	 -78,	 -80, \
			558,	 566,	 -83,	 -84,	 -93,	 561,	-149,	 555, \
			-129,	 562,	-140,	 -94,	 945,	 985,	-141,	-142, \
			-143,	 571,	 -95,	 627,	 626,	 569,	 -97,	 -98, \
			-99,	-101,	-100,	 583,	-103,	 940,	-104,	 551, \
			-105,	 547,	 574,	 667,	-108,	-131,	 596,	-139, \
			509,	-132,	 543,	 586,	1025,	 529,	  -3,	  -5, \
			-3,	  -3,	  -2,	  -8,	-134,	-133,	  -5,	  -5, \
			517,	  -5,	  -5,	  -8,	  -8,	 -12,	  -5,	  -5, \
			-5,	 -11,	 581,	 581,	 -39,	 -28,	  -6,	 -41, \
			-44,	 -21,	 526,	 256,	 -23,	 -49,	 -25,	  -2, \
			-39,	 -26,	 -21,	 -41,	-111,	-113,	-129,	 -11, \
			-9,	 525,	-136,	  -5,	 -10,	 581,	  -8,	 610, \
			-31,	 -20,	 -26,	 -21,	 -23,	 610,	 551,	 -89, \
			-7,	 -59,	 -39,	 -49,	 -21,	 -39,	 -77,	 -27, \
			628,	 -42,	 -47,	 -60,	 614,	 256,	 520,	 -49, \
			625,	  -5,	  -5,	  -5,	  -5,	-112,	 651,	 256, \
			-81,	-115,	 655,	-118,	-119,	-116,	 673,	-126, \
			-123,	-127,	-124,	-100,	-128,	-107,	 551,	 -25, \
			-129,	 666,	 664,	 657,	 -49,	 -78,	 679,	-105, \
			-99,	 662,	 665,	 -60,	 -21,	 -60,	  -5,	 -39, \
			-60,	 -31,	 -53,	 -24,	 966,	 -48,	 -47,	 -41, \
			-69,	 -70,	 -67,	 916,	1015,	 -22,	-137,	 -65, \
			-41,	 556,	 256,	 -49,	 -26,	  -5,	  -5,	 -58, \
			965,	 -73,	 -74,	 915,	1010,	  -5,	 -55,	 -26, \
			-27,	 -28,	 -92,	 -93,	 518,	 -41,	 -28,	  -6, \
			-85,	 -45,	 -28,	 -77,	 -39,	 -25,	 -81,	  -7, \
			-70,	  -5,	  -5,	-112,	 -85,	  -5,	  -5,	  -2, \
			-96,	 -74,	1005,	 698,	 698,	 697,	 508,	-102, \
			516,	 -98,	-103,	 -99,	 -39,	  -5,	 -30,	  -5, \
			-91,	-103,	 -21,	-103,	 -41,	-107,	 -31,	  -7, \
			-5,	  -5,	 593,	 581,	  -5,	  -3,	 -44,	 -28, \
			-45,	 -44,	 -28,	 -44,	 -41,	 -46,	 607,	 256, \
			-40,	 598,	 256,	 -42,	 -39,	 -40,	 -41,	-146, \
			651,	 256,	 -81,	-146,	 -13,	 -15,	 -15,	 -19, \
			611,	 256,	 -13,	 -13,	 -59,	 -21,	 -23,	-150, \
			-65,	  -5,	 -47,	  -5,	  -5,	 -86,	  -5,	-114, \
			-116,	 678,	 256,	-117,	-122,	-119,	 508,	-120, \
			-7,	 -70,	-118,	-116,	 -69,	 -70,	 -67,	-123, \
			-73,	 -74,	-116,	-112,	 -39,	 -41,	-120,	-119, \
			-119,	  -5,	-107,	-107,	 -81,	 -39,	 -29,	-110, \
			-29,	 506,	 256,	-145,	 531,	 256,	 -87,	 538, \
			256,	 -88,	 557,	 256,	 -47,	 -56,	  -5,	 -50, \
			980,	 -50,	 -50,	 -41,	 -41,	 -71,	  -5,	  -5, \
			-5,	  -5,	 -26,	 -66,	 588,	 256,	 -56,	  -5, \
			-71,	 -71,	  -5,	  -5,	 -27,	 -90,	  -5,	 -79, \
			573,	 256,	 -41,	 -65,	 -45,	 -45,	 -28,	 -28, \
			-39,	 -41,	 -82,	 568,	 256,	 -94,	 -91,	 -65, \
			-144,	 567,	 256,	 -94,	 -94,	  -5,	 699,	 565, \
			-95,	-101,	  -5,	 -50,	 -54,	 550,	 256,	-103, \
			-106,	 575,	 256,	-109,	 552,	 256,	-139,	  -5, \
			-44,	 -44,	 -44,	 -39,	 -40,	 -40,	-147,	 678, \
			256,	  -5,	 -19,	 -19,	 -54,	 551,	 -28,	-115, \
			-5,	-122,	-117,	-116,	-121,	-118,	 658,	 256, \
			-123,	-116,	-120,	-119,	-119,	-127,	 -50,	-127, \
			-127,	 -54,	-125,	 675,	 256,	-125,	-125,	 -50, \
			-79,	-125,	-125,	-110,	  -5,	  -5,	  -5,	  -5, \
			-54,	 -55,	 -31,	  -5,	 -57,	 -72,	 -54,	 -54, \
			-66,	 -67,	  -5,	 -55,	  -5,	 -79,	 -45,	 -28, \
			-5,	 -54,	 698,	 -95,	  -5,	 663,	  -5,	  -5, \
			-40,	-116,	-115,	  -5,	 -54,	-121,	 -54,	 -54, \
			-124,	  -5,	-128,	 -55,	 -50,	 -26,	 -26,	 -66, \
			-66, \
		)
		_YYDEF = (
			15,	  -2,	   0,	   2,	  15,	  15,	  15,	  15, \
			15,	   9,	 224,	   0,	  40,	 211,	 245,	 247, \
			15,	  15,	  15,	  13,	 226,	  42,	  43,	  44, \
			45,	  46,	 213,	 364,	 363,	 388,	 373,	 221, \
			14,	 228,	 229,	 232,	 233,	 234,	   0,	  15, \
			 0,	   0,	   0,	 356,	  16,	 235,	 236,	 264, \
			18,	 238,	  21,	 240,	  24,	  15,	  37,	 352, \
			28,	  29,	  30,	  31,	   0,	  33,	  34,	  35, \
			36,	 272,	 354,	 357,	 270,	 386,	   0,	   0, \
			80,	 124,	   0,	   0,	  60,	  61,	 380,	   0, \
			375,	 328,	  82,	  83,	  84,	  85,	   0,	   0, \
			67,	   0,	  64,	  90,	   0,	   0,	 371,	  69, \
			365,	  93,	 353,	  71,	  95,	 342,	  73,	   0, \
			98,	 129,	 100,	 130,	 104,	 132,	   0,	 108, \
			 0,	   0,	 111,	 112,	 134,	 346,	 348,	 208, \
			 0,	   0,	 255,	 136,	 369,	 385,	 257,	 258, \
			259,	  15,	 139,	   0,	   0,	   0,	 142,	 144, \
			 0,	 147,	   0,	 344,	 149,	 367,	 151,	   0, \
			 0,	   0,	   0,	   0,	   0,	 215,	 340,	 249, \
			217,	 218,	 219,	 251,	 396,	   1,	   3,	  15, \
			 4,	   5,	   7,	   8,	 227,	 225,	  41,	 212, \
			214,	 246,	 248,	  10,	  11,	  12,	 389,	 374, \
			222,	 223,	 230,	 231,	   0,	   0,	   0,	   0, \
			58,	   0,	 293,	 294,	   0,	   0,	   0,	   0, \
			 0,	   0,	 352,	   0,	   0,	   0,	   0,	   0, \
			20,	 237,	 239,	 265,	  23,	 241,	   0,	   0, \
			63,	   0,	   0,	 352,	   0,	   0,	   0,	 128, \
			 0,	  77,	 131,	   0,	   0,	   0,	 105,	  32, \
			38,	   0,	  66,	  81,	 290,	 292,	 279,	   0, \
			 0,	 273,	 358,	 271,	 387,	 165,	 303,	 305, \
			 0,	 167,	   0,	 170,	 172,	   0,	   0,	 193, \
			180,	 196,	 183,	   0,	 198,	 185,	   0,	 201, \
			 0,	   0,	   0,	   0,	   0,	   0,	 187,	   0, \
			 0,	   0,	   0,	 163,	 352,	   0,	 381,	   0, \
			 0,	   0,	   0,	   0,	 378,	   0,	   0,	  82, \
			 0,	   0,	   0,	 361,	 394,	 242,	 243,	  86, \
			87,	 276,	 278,	   0,	   0,	 372,	 366,	   0, \
			376,	   0,	   0,	 359,	 392,	 343,	  74,	   0, \
			79,	 101,	   0,	 135,	 266,	   0,	   0,	 109, \
			 0,	 115,	   0,	   0,	 119,	   0,	   0,	   0, \
			 0,	 347,	 209,	 210,	   0,	 256,	 370,	   0, \
			 0,	   0,	 390,	   0,	 262,	   0,	   0,	   0, \
			268,	 145,	 159,	   0,	   0,	 345,	 150,	 368, \
			 0,	 153,	   0,	 155,	   0,	 158,	   0,	   0, \
			216,	 341,	 220,	 252,	 253,	   6,	  52,	   0, \
			 0,	  55,	   0,	  57,	   0,	  59,	 323,	 324, \
			47,	 298,	 299,	   0,	   0,	  48,	   0,	 349, \
			306,	 307,	   0,	 351,	  17,	  19,	  22,	  25, \
			287,	 289,	   0,	   0,	   0,	   0,	   0,	 355, \
			102,	  39,	  65,	 291,	 280,	 125,	 304,	 166, \
			 0,	 329,	 331,	  -2,	   0,	 178,	   0,	   0, \
			 0,	   0,	 175,	   0,	   0,	   0,	   0,	   0, \
			 0,	   0,	   0,	 202,	   0,	   0,	   0,	   0, \
			 0,	 188,	 189,	 190,	   0,	   0,	 164,	 161, \
			 0,	 320,	 322,	 382,	 295,	 297,	 126,	 311, \
			313,	 127,	 325,	 327,	   0,	   0,	 379,	   0, \
			383,	   0,	   0,	   0,	   0,	  94,	 362,	 395, \
			244,	 277,	   0,	   0,	 300,	 302,	   0,	 377, \
			96,	  97,	 360,	 393,	  78,	 133,	 267,	 106, \
			308,	 310,	   0,	 113,	 116,	 117,	   0,	 120, \
			121,	 123,	 110,	 332,	 334,	 137,	   0,	 114, \
			260,	 274,	 275,	 140,	 141,	 391,	   0,	 263, \
			143,	 148,	 269,	   0,	 152,	 317,	 319,	 154, \
			156,	 314,	 316,	 160,	 284,	 286,	 250,	 254, \
			53,	  54,	  56,	   0,	  51,	  49,	 350,	 338, \
			339,	 288,	  26,	  27,	  76,	   0,	 103,	 168, \
			330,	   0,	 179,	   0,	 173,	 176,	 281,	 283, \
			181,	   0,	   0,	   0,	   0,	 197,	   0,	 199, \
			200,	 186,	 203,	 335,	 337,	 204,	 205,	   0, \
			207,	 191,	 192,	 162,	 321,	 296,	 312,	 326, \
			 0,	  70,	  62,	 384,	  75,	  99,	  91,	  92, \
			 0,	   0,	 301,	  72,	 309,	 107,	 118,	 122, \
			333,	 138,	 261,	 146,	 318,	 157,	 315,	 285, \
			50,	 177,	 171,	 282,	 182,	 174,	 194,	 195, \
			184,	 336,	 206,	  68,	   0,	   0,	   0,	  89, \
			88, \
		)

		if not getattr(LojbanParser._yyparse, "_yyval", None):
			LojbanParser._yyparse._yyval = None
		# end if not getattr(LojbanParser._yyparse, "_yyval", None):
		if not getattr(LojbanParser._yyparse, "_yyv", None):
			LojbanParser._yyparse._yyv = [None] * _YYMAXDEPTH
		# end if not getattr(LojbanParser._yyparse, "_yyv", None):
		if not getattr(LojbanParser._yyparse, "_redseq", None):
			LojbanParser._yyparse._redseq = [0] * _YYREDMAX
		# end if not getattr(LojbanParser._yyparse, "_redseq", None):
		if not getattr(LojbanParser._yyparse, "_redcnt", None):
			LojbanParser._yyparse._redcnt = 0
		# end if not getattr(LojbanParser._yyparse, "_redcnt", None):
		if not getattr(LojbanParser._yyparse, "_pcyyerrct", None):
			LojbanParser._yyparse._pcyyerrct = 0
		# end if not getattr(LojbanParser._yyparse, "_pcyyerrct", None):
		if not getattr(LojbanParser._yyparse, "_pcyyerrfl", None):
			LojbanParser._yyparse._pcyyerrfl = False
		# end if not getattr(LojbanParser._yyparse, "_pcyyerrfl", None):

		statestack = [0] * _YYMAXDEPTH # state stack

		tmpstate = 0;
		self._pcyytoken = -1;
		if _YYDEBUG:
			tmptoken = -1;
		# end if _YYDEBUG:
		pcyyerrct = 0;
		pcyyerrfl = 0;
		#// yyps = & statestack[-1];
		yysidx = -1;
		#// yypv = & LojbanParser._yyparse._yyv[-1];
		yyvidx = -1;

		#// enstack: /* push stack */
		n = None
		while True:#// enstack loop
			skipenstack = False;
			if _YYDEBUG:
				print("at state {:d}, next token {:d}".format( tmpstate, tmptoken));
			# end if _YYDEBUG:
			yysidx += 1;
			if yysidx > _YYMAXDEPTH - 1:
				self._yyerror("pcyacc internal stack overflow");
				return True;
			# end if yysidx > _YYMAXDEPTH - 1:
			statestack[yysidx] = tmpstate;
			yyvidx += 1;
			
			LojbanParser._yyparse._yyv[yyvidx] = LojbanParser._yyparse._yyval;

			loopnewstate = True;
			while loopnewstate:
				loopnewstate = False;
				n = _YYPACT[tmpstate];

				if n > _PCYYFLAG:
					if self._pcyytoken < 0:
						self._pcyytoken = self._yylex();
						if self._pcyytoken < 0:
							self._pcyytoken = 0;
						# end if self._pcyytoken < 0:
					# end if self._pcyytoken < 0:
					n += self._pcyytoken;

					if n >= 0 and n < _YYLAST:
						n = _YYACT[n];
						if _YYCHK[n] == self._pcyytoken:
							# /* a shift */
							if _YYDEBUG:
								tmptoken = self._pcyytoken;
							# end if _YYDEBUG:
							self._pcyytoken = -1;
							LojbanParser._yyparse._yyval = self._yylval;
							tmpstate = n;
							if pcyyerrfl > 0:
								pcyyerrfl -= 1
							# end if pcyyerrfl > 0:
							skipenstack = True;
							#// goto enstack;
						# end if _YYCHK[n] == self._pcyytoken:
					# end if n >= 0 and n < _YYLAST:
				# end if n > _PCYYFLAG:
				if skipenstack:
					break; #// newstate loop
				# end if skipenstack:
				n = _YYDEF[tmpstate];
				if n == -2:
					if self._pcyytoken < 0:
						self._pcyytoken = self._yylex();
						if self._pcyytoken < 0:
							self._pcyytoken = 0;
						# end if self._pcyytoken < 0:
					# end if self._pcyytoken < 0:
					yyxi = 0;
					while(( _YYEXCA[yyxi] != (-1)) or (_YYEXCA[yyxi+1] != tmpstate)):
						yyxi += 2;
					# end while(( _YYEXCA[yyxi] != (-1)) or (_YYEXCA[yyxi+1] != tmpstate)):
					yyxi += 2;
					while ( _YYEXCA[yyxi] >= 0):
						if _YYEXCA[yyxi] == self._pcyytoken:
							break;
						# end if _YYEXCA[yyxi] == self._pcyytoken:
						yyxi += 2;
					# end while ( _YYEXCA[yyxi] >= 0):
					n = _YYEXCA[yyxi+1];

					if (n < 0):
						# /* an accept action */
						if (_YYTFLAG):
							try:
								with open(_YYTFILEN, "w") as yytfilep:
									for ti in range(LojbanParser._yyparse._redcnt - 1, -1, -1):
										tj = svdprd[LojbanParser._yyparse._redseq[ti]];
										while svdnams[tj] == "$EOP":
											yytfilep.write("{:s} ".format(svdnams[tj]));
											tj += 1
										# end while svdnams[tj] == "$EOP":
										yytfilep.write("\n");
									# end for ti in range(LojbanParser._yyparse._redcnt - 1, -1, -1):
								# end with open(_YYTFILEN, "w") as yytfilep:
							except Exception as e:
								print("Can't open t file: {:s}".format(_YYTFILEN), file = sys.stderr);
								return False;
							# end try except Exception as e:
						# end if (_YYTFLAG):
						return False;
					# end if (n < 0):
				# end if n == -2:
				if n == 0:
					# /* error situation */
					if pcyyerrfl == _WAS0ERR:
						# /* an error just occurred */
						self._yyerror("syntax error");
						pcyyerrct += 1;
					# end if pcyyerrfl == _WAS0ERR:
					if pcyyerrfl in [_WAS0ERR, _WAS1ERR, _WAS2ERR]:
						# /* try again */
						pcyyerrfl = 3;
						# /* find a state for a legal shift action */
						while (yysidx >= 0):
							n = _YYPACT[statestack[yysidx]] + _YYERRCODE;
							if (n >= 0 and n < _YYLAST and _YYCHK[_YYACT[n]] == _YYERRCODE):
								tmpstate = _YYACT[n]; #/* simulate a shift of "error" */
								skipenstack = True;
								break; #// while (yyps >= statestack)
							# end if (n >= 0 and n < _YYLAST and _YYCHK[_YYACT[n]] == _YYERRCODE):
							n = _YYPACT[statestack[yysidx]];

							# /* the current yyps has no shift on "error", pop stack */
							if _YYDEBUG:
								print("error: pop state {:d}, recover state {:d}".format(statestack[yysidx], statestack[yysidx-1]));
							# end if _YYDEBUG:
							yysidx -= 1;
							yyvidx -= 1;
							
						# end while (yysidx >= 0):
						if not skipenstack:
							if (_YYTFLAG):
								try:
									with open(_YYTFILEN, "w") as yytfilep:
										for ti in range(LojbanParser._yyparse._redcnt - 1, -1, -1):
											tj = svdprd[LojbanParser._yyparse._redseq[ti]];
											while svdnams[tj] == "$EOP":
												yytfilep.write("{:s} ".format(svdnams[tj]));
												tj += 1
											# end while svdnams[tj] == "$EOP":
											yytfilep.write("\n");
										# end for ti in range(LojbanParser._yyparse._redcnt - 1, -1, -1):
									# end with open(_YYTFILEN, "w") as yytfilep:
								except Exception as e:
									print("Can't open t file: {:s}".format(_YYTFILEN), file = sys.stderr);
									return True;
								# end try except Exception as e:
							# end if (_YYTFLAG):
							return True;
						# end if not skipenstack:
					elif pcyyerrfl == _WAS3ERR:
						# /* clobber input char */
						if _YYDEBUG:
							print("error: discard token {:d}".format(self._pcyytoken));
						# end if _YYDEBUG:
						if self._pcyytoken == 0:
							if (_YYTFLAG):
								try:
									with open(_YYTFILEN, "w") as yytfilep:
										for ti in range(LojbanParser._yyparse._redcnt - 1, -1, -1):
											tj = svdprd[LojbanParser._yyparse._redseq[ti]];
											while svdnams[tj] == "$EOP":
												yytfilep.write("{:s} ".format(svdnams[tj]));
												tj += 1
											# end while svdnams[tj] == "$EOP":
											yytfilep.write("\n");
										# end for ti in range(LojbanParser._yyparse._redcnt - 1, -1, -1):
									# end with open(_YYTFILEN, "w") as yytfilep:
								except Exception as e:
									print("Can't open t file: {:s}".format(_YYTFILEN), file = sys.stderr);
									return True;
								# end try except Exception as e:
							# end if (_YYTFLAG):
							return True;
						# end if self._pcyytoken == 0:
						self._pcyytoken = -1;
						loopnewstate = True;
						#// goto newstate;
					# end if pcyyerrfl == ?
				# end if n == 0:
			# end while loopnewstate:
			if not skipenstack:
				# /* reduction, given a production n */
				if _YYDEBUG:
					print("reduce with rule {:d}".format(n));
				# end if _YYDEBUG:
				if _YYTFLAG and LojbanParser._yyparse._redcnt < _YYREDMAX:
					LojbanParser._yyparse._redseq[LojbanParser._yyparse._redcnt] = n;
					LojbanParser._yyparse._redcnt += 1
				# end if _YYTFLAG and LojbanParser._yyparse._redcnt < _YYREDMAX:
				yysidx -= _YYR2[n];
				yyvtidx = yyvidx;
				yyvidx -= _YYR2[n];
				
				LojbanParser._yyparse._yyval = LojbanParser._yyparse._yyv[yyvidx+1];

				m = n;
				# /* find next state from goto table */
				n = _YYR1[n];
				j = _YYPGO[n] + statestack[yysidx] + 1;
	
				if j < _YYLAST:
					tmpstate = _YYACT[j];   
				# end if j < _YYLAST:
				if (j >= _YYLAST or _YYCHK[_YYACT[j]] != -n):
					tmpstate = _YYACT[_YYPGO[n]];
				# end if (j >= _YYLAST or _YYCHK[_YYACT[j]] != -n):
				if m == 1:
					LojbanParser._yyparse._yyval = self._toplevel(LojbanParser._yyparse._yyv[yyvtidx -1]);
				elif m == 2:
					LojbanParser._yyparse._yyval = self._node(10000, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 3:
					LojbanParser._yyparse._yyval = self._node(10000, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 4:
					LojbanParser._yyparse._yyval = self._node(10000, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 5:
					LojbanParser._yyparse._yyval = self._node(10000, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 6:
					LojbanParser._yyparse._yyval = self._node(10000, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 7:
					LojbanParser._yyparse._yyval = self._node(10000, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 8:
					LojbanParser._yyparse._yyval = self._node(1, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 9:
					LojbanParser._yyparse._yyval = self._node(1, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 10:
					LojbanParser._yyparse._yyval = self._node(2, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 11:
					LojbanParser._yyparse._yyval = self._node(2, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 12:
					LojbanParser._yyparse._yyval = self._node(2, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 13:
					LojbanParser._yyparse._yyval = self._node(2, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 14:
					LojbanParser._yyparse._yyval = self._node(3, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 15:
					LojbanParser._yyparse._yyval = self._elidable(Constants.FAhO_529);
				elif m == 16:
					LojbanParser._yyparse._yyval = self._node(4, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 17:
					LojbanParser._yyparse._yyval = self._node(4, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 18:
					LojbanParser._yyparse._yyval = self._node(10, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 19:
					LojbanParser._yyparse._yyval = self._node(10, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 20:
					LojbanParser._yyparse._yyval = self._node(10, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 21:
					LojbanParser._yyparse._yyval = self._node(11, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 22:
					LojbanParser._yyparse._yyval = self._node(11, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 23:
					LojbanParser._yyparse._yyval = self._node(11, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 24:
					LojbanParser._yyparse._yyval = self._node(12, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 25:
					LojbanParser._yyparse._yyval = self._node(12, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 26:
					LojbanParser._yyparse._yyval = self._node(12, LojbanParser._yyparse._yyv[yyvtidx -3], LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 27:
					LojbanParser._yyparse._yyval = self._node(12, LojbanParser._yyparse._yyv[yyvtidx -3], LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 28:
					LojbanParser._yyparse._yyval = self._node(20, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 29:
					LojbanParser._yyparse._yyval = self._node(20, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 30:
					LojbanParser._yyparse._yyval = self._node(20, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 31:
					LojbanParser._yyparse._yyval = self._node(20, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 32:
					LojbanParser._yyparse._yyval = self._node(20, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 33:
					LojbanParser._yyparse._yyval = self._node(20, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 34:
					LojbanParser._yyparse._yyval = self._node(20, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 35:
					LojbanParser._yyparse._yyval = self._node(20, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 36:
					LojbanParser._yyparse._yyval = self._node(20, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 37:
					LojbanParser._yyparse._yyval = self._node(20, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 38:
					LojbanParser._yyparse._yyval = self._node(30, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 39:
					LojbanParser._yyparse._yyval = self._node(30, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 40:
					LojbanParser._yyparse._yyval = self._node(32, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 41:
					LojbanParser._yyparse._yyval = self._node(32, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 42:
					LojbanParser._yyparse._yyval = self._node(33, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 43:
					LojbanParser._yyparse._yyval = self._node(33, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 44:
					LojbanParser._yyparse._yyval = self._node(33, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 45:
					LojbanParser._yyparse._yyval = self._node(33, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 46:
					LojbanParser._yyparse._yyval = self._node(33, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 47:
					LojbanParser._yyparse._yyval = self._node(34, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 48:
					LojbanParser._yyparse._yyval = self._node(34, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 49:
					LojbanParser._yyparse._yyval = self._node(34, LojbanParser._yyparse._yyv[yyvtidx -3], LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 50:
					LojbanParser._yyparse._yyval = self._node(34, LojbanParser._yyparse._yyv[yyvtidx -4], LojbanParser._yyparse._yyv[yyvtidx -3], LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 51:
					LojbanParser._yyparse._yyval = self._node(34, LojbanParser._yyparse._yyv[yyvtidx -3], LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 52:
					LojbanParser._yyparse._yyval = self._node(35, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 53:
					LojbanParser._yyparse._yyval = self._node(35, LojbanParser._yyparse._yyv[yyvtidx -3], LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 54:
					LojbanParser._yyparse._yyval = self._node(35, LojbanParser._yyparse._yyv[yyvtidx -3], LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 55:
					LojbanParser._yyparse._yyval = self._node(35, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 56:
					LojbanParser._yyparse._yyval = self._node(35, LojbanParser._yyparse._yyv[yyvtidx -3], LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 57:
					LojbanParser._yyparse._yyval = self._node(35, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 58:
					LojbanParser._yyparse._yyval = self._node(35, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 59:
					LojbanParser._yyparse._yyval = self._node(36, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 60:
					LojbanParser._yyparse._yyval = self._node(40, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 61:
					LojbanParser._yyparse._yyval = self._node(40, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 62:
					LojbanParser._yyparse._yyval = self._node(41, LojbanParser._yyparse._yyv[yyvtidx -3], LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 63:
					LojbanParser._yyparse._yyval = self._node(41, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 64:
					LojbanParser._yyparse._yyval = self._node(41, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 65:
					LojbanParser._yyparse._yyval = self._node(42, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 66:
					LojbanParser._yyparse._yyval = self._node(42, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 67:
					LojbanParser._yyparse._yyval = self._node(50, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 68:
					LojbanParser._yyparse._yyval = self._node(50, LojbanParser._yyparse._yyv[yyvtidx -4], LojbanParser._yyparse._yyv[yyvtidx -3], LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 69:
					LojbanParser._yyparse._yyval = self._node(51, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 70:
					LojbanParser._yyparse._yyval = self._node(51, LojbanParser._yyparse._yyv[yyvtidx -3], LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 71:
					LojbanParser._yyparse._yyval = self._node(52, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 72:
					LojbanParser._yyparse._yyval = self._node(52, LojbanParser._yyparse._yyv[yyvtidx -3], LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 73:
					LojbanParser._yyparse._yyval = self._node(53, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 74:
					LojbanParser._yyparse._yyval = self._node(53, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 75:
					LojbanParser._yyparse._yyval = self._node(54, LojbanParser._yyparse._yyv[yyvtidx -3], LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 76:
					LojbanParser._yyparse._yyval = self._node(54, LojbanParser._yyparse._yyv[yyvtidx -3], LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 77:
					LojbanParser._yyparse._yyval = self._node(54, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 78:
					LojbanParser._yyparse._yyval = self._node(71, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 79:
					LojbanParser._yyparse._yyval = self._node(71, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 80:
					LojbanParser._yyparse._yyval = self._node(80, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 81:
					LojbanParser._yyparse._yyval = self._node(80, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 82:
					LojbanParser._yyparse._yyval = self._node(81, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 83:
					LojbanParser._yyparse._yyval = self._node(81, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 84:
					LojbanParser._yyparse._yyval = self._node(81, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 85:
					LojbanParser._yyparse._yyval = self._node(81, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 86:
					LojbanParser._yyparse._yyval = self._node(82, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 87:
					LojbanParser._yyparse._yyval = self._node(82, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 88:
					LojbanParser._yyparse._yyval = self._node(83, LojbanParser._yyparse._yyv[yyvtidx -6], LojbanParser._yyparse._yyv[yyvtidx -5], LojbanParser._yyparse._yyv[yyvtidx -4], LojbanParser._yyparse._yyv[yyvtidx -3], LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 89:
					LojbanParser._yyparse._yyval = self._node(83, LojbanParser._yyparse._yyv[yyvtidx -5], LojbanParser._yyparse._yyv[yyvtidx -4], LojbanParser._yyparse._yyv[yyvtidx -3], LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 90:
					LojbanParser._yyparse._yyval = self._node(90, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 91:
					LojbanParser._yyparse._yyval = self._node(90, LojbanParser._yyparse._yyv[yyvtidx -3], LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 92:
					LojbanParser._yyparse._yyval = self._node(90, LojbanParser._yyparse._yyv[yyvtidx -3], LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 93:
					LojbanParser._yyparse._yyval = self._node(91, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 94:
					LojbanParser._yyparse._yyval = self._node(91, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 95:
					LojbanParser._yyparse._yyval = self._node(92, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 96:
					LojbanParser._yyparse._yyval = self._node(92, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 97:
					LojbanParser._yyparse._yyval = self._node(92, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 98:
					LojbanParser._yyparse._yyval = self._node(93, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 99:
					LojbanParser._yyparse._yyval = self._node(93, LojbanParser._yyparse._yyv[yyvtidx -3], LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 100:
					LojbanParser._yyparse._yyval = self._node(94, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 101:
					LojbanParser._yyparse._yyval = self._node(94, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 102:
					LojbanParser._yyparse._yyval = self._node(94, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 103:
					LojbanParser._yyparse._yyval = self._node(94, LojbanParser._yyparse._yyv[yyvtidx -3], LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 104:
					LojbanParser._yyparse._yyval = self._node(95, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 105:
					LojbanParser._yyparse._yyval = self._node(95, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 106:
					LojbanParser._yyparse._yyval = self._node(96, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 107:
					LojbanParser._yyparse._yyval = self._node(96, LojbanParser._yyparse._yyv[yyvtidx -3], LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 108:
					LojbanParser._yyparse._yyval = self._node(96, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 109:
					LojbanParser._yyparse._yyval = self._node(96, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 110:
					LojbanParser._yyparse._yyval = self._node(96, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 111:
					LojbanParser._yyparse._yyval = self._node(96, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 112:
					LojbanParser._yyparse._yyval = self._node(96, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 113:
					LojbanParser._yyparse._yyval = self._node(110, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 114:
					LojbanParser._yyparse._yyval = self._node(110, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 115:
					LojbanParser._yyparse._yyval = self._node(111, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 116:
					LojbanParser._yyparse._yyval = self._node(111, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 117:
					LojbanParser._yyparse._yyval = self._node(111, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 118:
					LojbanParser._yyparse._yyval = self._node(111, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 119:
					LojbanParser._yyparse._yyval = self._node(112, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 120:
					LojbanParser._yyparse._yyval = self._node(112, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 121:
					LojbanParser._yyparse._yyval = self._node(112, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 122:
					LojbanParser._yyparse._yyval = self._node(112, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 123:
					LojbanParser._yyparse._yyval = self._node(112, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 124:
					LojbanParser._yyparse._yyval = self._node(121, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 125:
					LojbanParser._yyparse._yyval = self._node(121, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 126:
					LojbanParser._yyparse._yyval = self._node(122, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 127:
					LojbanParser._yyparse._yyval = self._node(122, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 128:
					LojbanParser._yyparse._yyval = self._node(130, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 129:
					LojbanParser._yyparse._yyval = self._node(130, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 130:
					LojbanParser._yyparse._yyval = self._node(131, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 131:
					LojbanParser._yyparse._yyval = self._node(131, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 132:
					LojbanParser._yyparse._yyval = self._node(132, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 133:
					LojbanParser._yyparse._yyval = self._node(132, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 134:
					LojbanParser._yyparse._yyval = self._node(133, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 135:
					LojbanParser._yyparse._yyval = self._node(133, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 136:
					LojbanParser._yyparse._yyval = self._node(134, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 137:
					LojbanParser._yyparse._yyval = self._node(134, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 138:
					LojbanParser._yyparse._yyval = self._node(134, LojbanParser._yyparse._yyv[yyvtidx -3], LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 139:
					LojbanParser._yyparse._yyval = self._node(135, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 140:
					LojbanParser._yyparse._yyval = self._node(135, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 141:
					LojbanParser._yyparse._yyval = self._node(135, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 142:
					LojbanParser._yyparse._yyval = self._node(136, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 143:
					LojbanParser._yyparse._yyval = self._node(136, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 144:
					LojbanParser._yyparse._yyval = self._node(136, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 145:
					LojbanParser._yyparse._yyval = self._node(136, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 146:
					LojbanParser._yyparse._yyval = self._node(137, LojbanParser._yyparse._yyv[yyvtidx -3], LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 147:
					LojbanParser._yyparse._yyval = self._node(150, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 148:
					LojbanParser._yyparse._yyval = self._node(150, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 149:
					LojbanParser._yyparse._yyval = self._node(151, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 150:
					LojbanParser._yyparse._yyval = self._node(151, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 151:
					LojbanParser._yyparse._yyval = self._node(152, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 152:
					LojbanParser._yyparse._yyval = self._node(152, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 153:
					LojbanParser._yyparse._yyval = self._node(152, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 154:
					LojbanParser._yyparse._yyval = self._node(152, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 155:
					LojbanParser._yyparse._yyval = self._node(152, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 156:
					LojbanParser._yyparse._yyval = self._node(152, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 157:
					LojbanParser._yyparse._yyval = self._node(152, LojbanParser._yyparse._yyv[yyvtidx -3], LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 158:
					LojbanParser._yyparse._yyval = self._node(152, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 159:
					LojbanParser._yyparse._yyval = self._node(152, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 160:
					LojbanParser._yyparse._yyval = self._node(152, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 161:
					LojbanParser._yyparse._yyval = self._node(160, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 162:
					LojbanParser._yyparse._yyval = self._node(160, LojbanParser._yyparse._yyv[yyvtidx -3], LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 163:
					LojbanParser._yyparse._yyval = self._node(161, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 164:
					LojbanParser._yyparse._yyval = self._node(161, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 165:
					LojbanParser._yyparse._yyval = self._node(300, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 166:
					LojbanParser._yyparse._yyval = self._node(300, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 167:
					LojbanParser._yyparse._yyval = self._node(310, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 168:
					LojbanParser._yyparse._yyval = self._node(310, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 169:
					LojbanParser._yyparse._yyval = self._node(310, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 170:
					LojbanParser._yyparse._yyval = self._node(311, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 171:
					LojbanParser._yyparse._yyval = self._node(311, LojbanParser._yyparse._yyv[yyvtidx -3], LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 172:
					LojbanParser._yyparse._yyval = self._node(312, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 173:
					LojbanParser._yyparse._yyval = self._node(312, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 174:
					LojbanParser._yyparse._yyval = self._node(312, LojbanParser._yyparse._yyv[yyvtidx -3], LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 175:
					LojbanParser._yyparse._yyval = self._node(313, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 176:
					LojbanParser._yyparse._yyval = self._node(313, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 177:
					LojbanParser._yyparse._yyval = self._node(330, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 178:
					LojbanParser._yyparse._yyval = self._node(332, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 179:
					LojbanParser._yyparse._yyval = self._node(332, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 180:
					LojbanParser._yyparse._yyval = self._node(370, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 181:
					LojbanParser._yyparse._yyval = self._node(370, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 182:
					LojbanParser._yyparse._yyval = self._node(370, LojbanParser._yyparse._yyv[yyvtidx -3], LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 183:
					LojbanParser._yyparse._yyval = self._node(371, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 184:
					LojbanParser._yyparse._yyval = self._node(371, LojbanParser._yyparse._yyv[yyvtidx -3], LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 185:
					LojbanParser._yyparse._yyval = self._node(372, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 186:
					LojbanParser._yyparse._yyval = self._node(372, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 187:
					LojbanParser._yyparse._yyval = self._node(374, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 188:
					LojbanParser._yyparse._yyval = self._node(374, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 189:
					LojbanParser._yyparse._yyval = self._node(374, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 190:
					LojbanParser._yyparse._yyval = self._node(374, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 191:
					LojbanParser._yyparse._yyval = self._node(374, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 192:
					LojbanParser._yyparse._yyval = self._node(374, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 193:
					LojbanParser._yyparse._yyval = self._node(381, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 194:
					LojbanParser._yyparse._yyval = self._node(381, LojbanParser._yyparse._yyv[yyvtidx -3], LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 195:
					LojbanParser._yyparse._yyval = self._node(381, LojbanParser._yyparse._yyv[yyvtidx -3], LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 196:
					LojbanParser._yyparse._yyval = self._node(382, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 197:
					LojbanParser._yyparse._yyval = self._node(382, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 198:
					LojbanParser._yyparse._yyval = self._node(383, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 199:
					LojbanParser._yyparse._yyval = self._node(383, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 200:
					LojbanParser._yyparse._yyval = self._node(383, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 201:
					LojbanParser._yyparse._yyval = self._node(385, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 202:
					LojbanParser._yyparse._yyval = self._node(385, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 203:
					LojbanParser._yyparse._yyval = self._node(385, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 204:
					LojbanParser._yyparse._yyval = self._node(385, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 205:
					LojbanParser._yyparse._yyval = self._node(385, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 206:
					LojbanParser._yyparse._yyval = self._node(385, LojbanParser._yyparse._yyv[yyvtidx -3], LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 207:
					LojbanParser._yyparse._yyval = self._node(385, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 208:
					LojbanParser._yyparse._yyval = self._node(400, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 209:
					LojbanParser._yyparse._yyval = self._node(400, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 210:
					LojbanParser._yyparse._yyval = self._node(400, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 211:
					LojbanParser._yyparse._yyval = self._node(404, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 212:
					LojbanParser._yyparse._yyval = self._node(404, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 213:
					LojbanParser._yyparse._yyval = self._node(405, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 214:
					LojbanParser._yyparse._yyval = self._node(405, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 215:
					LojbanParser._yyparse._yyval = self._node(407, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 216:
					LojbanParser._yyparse._yyval = self._node(407, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 217:
					LojbanParser._yyparse._yyval = self._node(408, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 218:
					LojbanParser._yyparse._yyval = self._node(408, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 219:
					LojbanParser._yyparse._yyval = self._node(408, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 220:
					LojbanParser._yyparse._yyval = self._node(408, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 221:
					LojbanParser._yyparse._yyval = self._node(410, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 222:
					LojbanParser._yyparse._yyval = self._node(410, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 223:
					LojbanParser._yyparse._yyval = self._node(410, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 224:
					LojbanParser._yyparse._yyval = self._node(411, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 225:
					LojbanParser._yyparse._yyval = self._node(411, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 226:
					LojbanParser._yyparse._yyval = self._node(412, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 227:
					LojbanParser._yyparse._yyval = self._node(412, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 228:
					LojbanParser._yyparse._yyval = self._node(413, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 229:
					LojbanParser._yyparse._yyval = self._node(413, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 230:
					LojbanParser._yyparse._yyval = self._node(413, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 231:
					LojbanParser._yyparse._yyval = self._node(413, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 232:
					LojbanParser._yyparse._yyval = self._node(413, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 233:
					LojbanParser._yyparse._yyval = self._node(413, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 234:
					LojbanParser._yyparse._yyval = self._node(413, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 235:
					LojbanParser._yyparse._yyval = self._node(415, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 236:
					LojbanParser._yyparse._yyval = self._node(415, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 237:
					LojbanParser._yyparse._yyval = self._node(415, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 238:
					LojbanParser._yyparse._yyval = self._node(416, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 239:
					LojbanParser._yyparse._yyval = self._node(416, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 240:
					LojbanParser._yyparse._yyval = self._node(417, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 241:
					LojbanParser._yyparse._yyval = self._node(417, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 242:
					LojbanParser._yyparse._yyval = self._node(421, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 243:
					LojbanParser._yyparse._yyval = self._node(421, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 244:
					LojbanParser._yyparse._yyval = self._node(421, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 245:
					LojbanParser._yyparse._yyval = self._node(422, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 246:
					LojbanParser._yyparse._yyval = self._node(422, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 247:
					LojbanParser._yyparse._yyval = self._node(422, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 248:
					LojbanParser._yyparse._yyval = self._node(422, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 249:
					LojbanParser._yyparse._yyval = self._node(425, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 250:
					LojbanParser._yyparse._yyval = self._node(425, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 251:
					LojbanParser._yyparse._yyval = self._node(426, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 252:
					LojbanParser._yyparse._yyval = self._node(426, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 253:
					LojbanParser._yyparse._yyval = self._node(426, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 254:
					LojbanParser._yyparse._yyval = self._node(426, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 255:
					LojbanParser._yyparse._yyval = self._node(432, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 256:
					LojbanParser._yyparse._yyval = self._node(432, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 257:
					LojbanParser._yyparse._yyval = self._node(433, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 258:
					LojbanParser._yyparse._yyval = self._node(433, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 259:
					LojbanParser._yyparse._yyval = self._node(433, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 260:
					LojbanParser._yyparse._yyval = self._node(433, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 261:
					LojbanParser._yyparse._yyval = self._node(434, LojbanParser._yyparse._yyv[yyvtidx -3], LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 262:
					LojbanParser._yyparse._yyval = self._node(435, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 263:
					LojbanParser._yyparse._yyval = self._node(436, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 264:
					LojbanParser._yyparse._yyval = self._node(440, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 265:
					LojbanParser._yyparse._yyval = self._node(440, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 266:
					LojbanParser._yyparse._yyval = self._node(443, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 267:
					LojbanParser._yyparse._yyval = self._node(443, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 268:
					LojbanParser._yyparse._yyval = self._node(444, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 269:
					LojbanParser._yyparse._yyval = self._node(444, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 270:
					LojbanParser._yyparse._yyval = self._node(445, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 271:
					LojbanParser._yyparse._yyval = self._node(445, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 272:
					LojbanParser._yyparse._yyval = self._node(447, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 273:
					LojbanParser._yyparse._yyval = self._node(447, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 274:
					LojbanParser._yyparse._yyval = self._node(448, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 275:
					LojbanParser._yyparse._yyval = self._elidable(Constants.LIhU_567);
					pcyyerrfl = 0;
				elif m == 276:
					LojbanParser._yyparse._yyval = self._node(450, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 277:
					LojbanParser._yyparse._yyval = self._node(450, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 278:
					LojbanParser._yyparse._yyval = self._elidable(Constants.KU_556);
					pcyyerrfl = 0;
				elif m == 279:
					LojbanParser._yyparse._yyval = self._node(451, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 280:
					LojbanParser._yyparse._yyval = self._node(451, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 281:
					LojbanParser._yyparse._yyval = self._node(452, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 282:
					LojbanParser._yyparse._yyval = self._node(452, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 283:
					LojbanParser._yyparse._yyval = self._elidable(Constants.KUhE_658);
					pcyyerrfl = 0;
				elif m == 284:
					LojbanParser._yyparse._yyval = self._node(453, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 285:
					LojbanParser._yyparse._yyval = self._node(453, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 286:
					LojbanParser._yyparse._yyval = self._elidable(Constants.KEI_552);
					pcyyerrfl = 0;
				elif m == 287:
					LojbanParser._yyparse._yyval = self._node(454, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 288:
					LojbanParser._yyparse._yyval = self._node(454, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 289:
					LojbanParser._yyparse._yyval = self._elidable(Constants.TUhU_611);
					pcyyerrfl = 0;
				elif m == 290:
					LojbanParser._yyparse._yyval = self._node(456, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 291:
					LojbanParser._yyparse._yyval = self._node(456, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 292:
					LojbanParser._yyparse._yyval = self._elidable(Constants.VAU_614);
					pcyyerrfl = 0;
				elif m == 293:
					LojbanParser._yyparse._yyval = self._node(457, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 294:
					LojbanParser._yyparse._yyval = self._elidable(Constants.DOhU_526);
					pcyyerrfl = 0;
				elif m == 295:
					LojbanParser._yyparse._yyval = self._node(458, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 296:
					LojbanParser._yyparse._yyval = self._node(458, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 297:
					LojbanParser._yyparse._yyval = self._elidable(Constants.FEhU_531);
					pcyyerrfl = 0;
				elif m == 298:
					LojbanParser._yyparse._yyval = self._node(459, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 299:
					LojbanParser._yyparse._yyval = self._elidable(Constants.SEhU_598);
					pcyyerrfl = 0;
				elif m == 300:
					LojbanParser._yyparse._yyval = self._node(460, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 301:
					LojbanParser._yyparse._yyval = self._node(460, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 302:
					LojbanParser._yyparse._yyval = self._elidable(Constants.NUhU_588);
					pcyyerrfl = 0;
				elif m == 303:
					LojbanParser._yyparse._yyval = self._node(461, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 304:
					LojbanParser._yyparse._yyval = self._node(461, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 305:
					LojbanParser._yyparse._yyval = self._elidable(Constants.BOI_651);
					pcyyerrfl = 0;
				elif m == 306:
					LojbanParser._yyparse._yyval = self._node(462, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 307:
					LojbanParser._yyparse._yyval = self._elidable(Constants.BOI_651);
					pcyyerrfl = 0;
				elif m == 308:
					LojbanParser._yyparse._yyval = self._node(463, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 309:
					LojbanParser._yyparse._yyval = self._node(463, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 310:
					LojbanParser._yyparse._yyval = self._elidable(Constants.LUhU_573);
					pcyyerrfl = 0;
				elif m == 311:
					LojbanParser._yyparse._yyval = self._node(464, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 312:
					LojbanParser._yyparse._yyval = self._node(464, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 313:
					LojbanParser._yyparse._yyval = self._elidable(Constants.GEhU_538);
					pcyyerrfl = 0;
				elif m == 314:
					LojbanParser._yyparse._yyval = self._node(465, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 315:
					LojbanParser._yyparse._yyval = self._node(465, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 316:
					LojbanParser._yyparse._yyval = self._elidable(Constants.MEhU_575);
					pcyyerrfl = 0;
				elif m == 317:
					LojbanParser._yyparse._yyval = self._node(466, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 318:
					LojbanParser._yyparse._yyval = self._node(466, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 319:
					LojbanParser._yyparse._yyval = self._elidable(Constants.KEhE_550);
					pcyyerrfl = 0;
				elif m == 320:
					LojbanParser._yyparse._yyval = self._node(467, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 321:
					LojbanParser._yyparse._yyval = self._node(467, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 322:
					LojbanParser._yyparse._yyval = self._elidable(Constants.BEhO_506);
					pcyyerrfl = 0;
				elif m == 323:
					LojbanParser._yyparse._yyval = self._node(468, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 324:
					LojbanParser._yyparse._yyval = self._elidable(Constants.TOI_607);
					pcyyerrfl = 0;
				elif m == 325:
					LojbanParser._yyparse._yyval = self._node(469, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 326:
					LojbanParser._yyparse._yyval = self._node(469, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 327:
					LojbanParser._yyparse._yyval = self._elidable(Constants.KUhO_557);
					pcyyerrfl = 0;
				elif m == 328:
					LojbanParser._yyparse._yyval = self._node(470, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 329:
					LojbanParser._yyparse._yyval = self._node(471, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 330:
					LojbanParser._yyparse._yyval = self._node(471, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 331:
					LojbanParser._yyparse._yyval = self._elidable(Constants.VEhO_678);
					pcyyerrfl = 0;
				elif m == 332:
					LojbanParser._yyparse._yyval = self._node(472, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 333:
					LojbanParser._yyparse._yyval = self._node(472, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 334:
					LojbanParser._yyparse._yyval = self._elidable(Constants.LOhO_568);
					pcyyerrfl = 0;
				elif m == 335:
					LojbanParser._yyparse._yyval = self._node(473, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 336:
					LojbanParser._yyparse._yyval = self._node(473, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 337:
					LojbanParser._yyparse._yyval = self._elidable(Constants.TEhU_675);
					pcyyerrfl = 0;
				elif m == 338:
					LojbanParser._yyparse._yyval = self._node(474, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 339:
					LojbanParser._yyparse._yyval = self._elidable(Constants.VEhO_678);
					pcyyerrfl = 0;
				elif m == 340:
					LojbanParser._yyparse._yyval = self._node(480, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 341:
					LojbanParser._yyparse._yyval = self._node(480, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 342:
					LojbanParser._yyparse._yyval = self._node(481, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 343:
					LojbanParser._yyparse._yyval = self._node(481, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 344:
					LojbanParser._yyparse._yyval = self._node(482, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 345:
					LojbanParser._yyparse._yyval = self._node(482, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 346:
					LojbanParser._yyparse._yyval = self._node(483, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 347:
					LojbanParser._yyparse._yyval = self._node(483, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 348:
					LojbanParser._yyparse._yyval = self._node(483, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 349:
					LojbanParser._yyparse._yyval = self._node(486, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 350:
					LojbanParser._yyparse._yyval = self._node(486, LojbanParser._yyparse._yyv[yyvtidx -3], LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 351:
					LojbanParser._yyparse._yyval = self._node(486, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 352:
					LojbanParser._yyparse._yyval = self._node(490, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 353:
					LojbanParser._yyparse._yyval = self._node(490, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 354:
					LojbanParser._yyparse._yyval = self._node(491, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 355:
					LojbanParser._yyparse._yyval = self._node(491, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 356:
					LojbanParser._yyparse._yyval = self._node(801, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 357:
					LojbanParser._yyparse._yyval = self._node(802, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 358:
					LojbanParser._yyparse._yyval = self._node(802, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 359:
					LojbanParser._yyparse._yyval = self._node(803, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 360:
					LojbanParser._yyparse._yyval = self._node(803, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 361:
					LojbanParser._yyparse._yyval = self._node(804, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 362:
					LojbanParser._yyparse._yyval = self._node(804, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 363:
					LojbanParser._yyparse._yyval = self._node(805, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 364:
					LojbanParser._yyparse._yyval = self._node(806, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 365:
					LojbanParser._yyparse._yyval = self._node(807, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 366:
					LojbanParser._yyparse._yyval = self._node(807, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 367:
					LojbanParser._yyparse._yyval = self._node(808, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 368:
					LojbanParser._yyparse._yyval = self._node(808, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 369:
					LojbanParser._yyparse._yyval = self._node(809, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 370:
					LojbanParser._yyparse._yyval = self._node(809, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 371:
					LojbanParser._yyparse._yyval = self._node(810, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 372:
					LojbanParser._yyparse._yyval = self._node(810, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 373:
					LojbanParser._yyparse._yyval = self._node(811, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 374:
					LojbanParser._yyparse._yyval = self._node(811, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 375:
					LojbanParser._yyparse._yyval = self._node(812, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 376:
					LojbanParser._yyparse._yyval = self._node(813, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 377:
					LojbanParser._yyparse._yyval = self._node(813, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 378:
					LojbanParser._yyparse._yyval = self._node(814, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 379:
					LojbanParser._yyparse._yyval = self._node(814, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 380:
					LojbanParser._yyparse._yyval = self._node(815, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 381:
					LojbanParser._yyparse._yyval = self._node(815, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 382:
					LojbanParser._yyparse._yyval = self._node(815, LojbanParser._yyparse._yyv[yyvtidx -2], LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 383:
					LojbanParser._yyparse._yyval = self._node(816, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 384:
					LojbanParser._yyparse._yyval = self._node(816, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 385:
					LojbanParser._yyparse._yyval = self._node(817, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 386:
					LojbanParser._yyparse._yyval = self._node(818, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 387:
					LojbanParser._yyparse._yyval = self._node(818, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 388:
					LojbanParser._yyparse._yyval = self._node(819, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 389:
					LojbanParser._yyparse._yyval = self._node(819, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 390:
					LojbanParser._yyparse._yyval = self._node(821, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 391:
					LojbanParser._yyparse._yyval = self._node(821, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 392:
					LojbanParser._yyparse._yyval = self._node(822, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 393:
					LojbanParser._yyparse._yyval = self._node(822, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 394:
					LojbanParser._yyparse._yyval = self._node(823, LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 395:
					LojbanParser._yyparse._yyval = self._node(823, LojbanParser._yyparse._yyv[yyvtidx -1], LojbanParser._yyparse._yyv[yyvtidx -0]);
				elif m == 396:
					LojbanParser._yyparse._yyval = self._node(824, LojbanParser._yyparse._yyv[yyvtidx -0]);
				# end if m == ?
			# end if not skipenstack:
		# end while True:#// enstack loop
	# end def _yyparse(self):

	#
	# High level methods
	# These can be called from any script
	#
	def setparameters(self, *parameters):
		"""
		Sets the parameters using a list of arguments:

		-dv prints each valsi as read.
		-dL prints each token as lexed by the compounder.
		-dR prints each compounder reduction as attempted.
		-dl prints each token as lexed by the YACC parser.
		-dr prints each YACC reduction as executed.
		-de prints each elidable terminator as inserted.
		-d* is equivalent to all other -d options together.

		-t produces a dump of the internal tree in TAB-separated columns:
			column 1 is a node number;
			column 2 is a rule/selma'o name;
			column 3 is a word for terminals;
			columns 3-n are numbers of subnodes for non-terminals;
			there are no forward references to nodes.

		-p outputs the text as a Prolog datum, with rule/selma'o names used 
			as functors.

		If neither -t nor -p is set then the nodes are listed in Lisp format.

		-e omits the insertion of elidables.

		-p outputs the text as a Prolog datum, with rule/selma'o names
			used as functors.

		-f outputs a full parse: normally, tree nodes with one
			child are omitted (most useful with -t or -p).

		-c print the list of cmavo and exits.

		-l sets logging mode to true (used only when reading from file)

		-m MAXLINE: sets maximum number of characters per line for output.
			MAXLINE should be an integer. Zero of negative values for no limit.
			Defaults to 75.

		--maxdepth MAXDEPTH sets maximum parsing tree depth
			MAXDEPTH should be an integer. 
			Zero of negative values for default value (200).

		--redmax REDMAX sets maximum number of pasring reductions
			REDMAX should be an integer. 
			Zero of negative values for default value (100).

		-d sets grammar debug mode on

		-g sets grammar error logging mode on

		--tfile FILE sets grammar error logging file.
			Used only when grammar error logging mode is on (default "grammar.tmp").
		"""
		self._parameters.setparameters(*parameters)
		if self._parameters.mkcmavo:
			LojbanParser._mkcmavo()
			sys.exit(0)
		# end if self._parameters.mkcmavo:
	# end def setparameters(self, parameters):

	def reset(self):
		"""
		Clears old data.
		Should be used before any new parsing.
		This method is called from all high level parsing methods (parseString, parseFile, parse)
		"""
		self._interactive = False

		self._pushback = None # _gettoken _fail
		self._head = None # _fail _release
		self._tail = None # _fail _release

		# variables (those that were global in C code)
		# value assigned during parsing (defined in grammar.c)
		self._yylval = None
		# pcyytoken (defined in grammar.h)
		# input token
		self._pcyytoken = -1

		# line and column of input (globals defined in getword.c)		
		self._line = 1
		self._column = 0
		# index of last reduction (defined in node.c)
		self._lastreduce = -1
		# error identifiers (defined in node.c)
		self._errline = -1
		self._errcol = -1
		self._errtype = -1
		self._errlastreduce = -1
		# memory used by tokens
		self._tokspace = 0
		# memory used for strings
		self._stringspace = 0
		# token objects
		self._freelist = None
		self._newtoken_result = None
		self._results = None
		# the actual list of token objects generated in each call of makefree
		self._tokenslist = []
	# end def reset(self):

	#
	# Delegate methods
	#
	def print(self, tok, endline = True):
		Token.print(tok, endline, singlemode = self._parameters.singlemode, \
			maxline = self._parameters.maxline)
	# end def print(tok, endline = True):
	
	def rprint(self, tok, endline = True):
		Token.rprint(tok, endline, singlemode = self._parameters.singlemode, \
			maxline = self._parameters.maxline)
	# end def rprint(self, tok, endline = True):

	def tprint(self, tok):
		Token.tprint(tok)
	# end def tprint(tok):

	#
	# Utility methods for parsing
	#
	def parseString(self, s):
		"""
		Parses a string.
		"""
		self.reset()
		#  backup stdin 
		sysstdin = sys.stdin
		self._interactive = False

		sys.stdin = StringIO(s)
		if self._yyparse(yymaxdepth = self._parameters.yymaxdepth, 
			yyredmax = self._parameters.yyredmax, 
			yydebug = self._parameters.yydebug, 
			yytflag = self._parameters.yytflag, 
			yytfilen = self._parameters.yytfilen):
			print( \
				"Problem with selma'o {:s} at or before line {:d} column {:d}".format(\
					Constants.rulename(self._errtype), self._errline, \
					self._errcol), file = sys.stderr)
			print("Last good construct was: {:s}".format( \
				Constants.rulename(self._errlastreduce)), file = sys.stderr)
			#  reset stdin 
			self._results = None
		# end if yyparse():

		sys.stdin = sysstdin
		return self._results() if self._results else None
	# end def parseString(self, s):

	def parseStdin(self):
		"""
		Parses standard input.
		"""
		if self._yyparse(yymaxdepth = self._parameters.yymaxdepth, 
			yyredmax = self._parameters.yyredmax, 
			yydebug = self._parameters.yydebug, 
			yytflag = self._parameters.yytflag, 
			yytfilen = self._parameters.yytfilen):
			print( \
				"Problem with selma'o {:s} at or before line {:d} column {:d}".format(\
					Constants.rulename(self._errtype), self._errline, \
					self._errcol), file = sys.stderr)
			print("Last good construct was: {:s}".format( \
				Constants.rulename(self._errlastreduce)), file = sys.stderr)
			#  reset stdin 
			self._results = None
		# end if yyparse():
		return self._results() if self._results else None
	# end def parseStdin(self):
# end class LojbanParser:
		

if __name__ == '__main__':
	print("Module '{:s}' cannot be executed directly.".format(__file__))
# end if __name__ == '__main__':
