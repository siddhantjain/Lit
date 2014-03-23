regexes = [
(r'#.*$','TK_CMNT'),
('_main','TK_MAIN'),			#placed before functions since functions have a similar starting character
(r'\$[a-zA-Z]+','TK_ID'),
(r'\"(\\.|[^"])*\"','TK_STRLIT'),
('[0-9]+\.[0-9][0-9]','TK_RNUM'), 	#Placed before following line for PoLM			
(r'\d+','TK_NUM'),
('global','TK_GLOBAL'),
('input_parameters','TK_IPP'),
('output_parameters','TK_OPP'),
('_[a-zA-Z][a-zA-Z]*','TK_FUNC'),	
(r'\[','TK_OSQ'),
(r'\]','TK_CSQ'),
(r';','TK_SCLN'),
('if','TK_IF'),
('endif','TK_EIF'),			#Placed before end to satisfy principal of longest match
('else','TK_ELSE'),
('return','TK_RET'),
('end','TK_FEND'),
('int','TK_INT'),
('float','TK_FLOAT'),
('read','TK_READ'),
('call','TK_CALL'),
('println','TK_PRINTLN'),
('print','TK_PRINT'),
(r'\(','TK_ORD'),
(r'\)','TK_CRD'),
('while','TK_WHILE'),
('endwhile','TK_EWHILE'),
(r'<\-','TK_ASSIGN'),		
('==','TK_EQ'),
('<=','TK_LTE'),		    #NOTE: Ordering is important for principal of longest match
('<','TK_LESS'),
('>=','TK_GTE'),		    #NOTE: Ordering is important for principal of longest match
('>','TK_GRTR'),
('~','TK_NOT'),
('!=','TK_NOTEQ'),
('&&','TK_AND'),
(r'\|\|','TK_OR'),
(r'\+','TK_PLUS'),
(r'\-','TK_MINUS'),
(r'\*','TK_MUL'),
(r'/','TK_DIV'),
(r'%','TK_MOD'),
(r',','TK_COMMA'),
('void','TK_VOID')

    ]
