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
('endif','TK_ENDIF'),			#Placed before end to satisfy principal of longest match
('else','TK_ELSE'),
('return','TK_RET'),
('endwhile','TK_EWHILE'),       #Placed before end to satisfy principal of longest match
('end','TK_END'),
('int','TK_INT'),
('float','TK_FLOAT'),
('read','TK_READ'),
('call','TK_CALL'),
('println','TK_PRINTLN'),
('print','TK_PRINT'),
(r'\(','TK_ORD'),
(r'\)','TK_CRD'),
('while','TK_WHILE'),
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

nonTerminals = [
'<Program>',
'<O_functions>',
'<main_function>',
'<stmts>',
'<O_stmts>',
'<stmt>',
'<gen_stmt>',
'<print_stmts>',
'<print_stmt>',
'<println_stmt>',
'<all_var>',
'<id>',
'<id_1>',
'<id_2>',
'<read_stmt>',
'<declrtv_stmts>',
'<declrtv_stmt>',
'<d_s>',
'<global_stmt>',
'<type>',
'<arithmetic_expression>',
'<a_e>',
'<term>',
'<t_e>',
'<factor>',
'<var>',
'<Boolean_expression>',
'<b_e>',
'<logical_operator>',
'<relational_operator>',
'<cond_stmt>',
'<c_s>',
'<iterative_stmt>',
'<funcall_Stmt>',
'<list_var>',
'<next>',
'<break_stmt>',
'<assignm_stmt>',
'<function>',
'<input_parameters>',
'<i_p>',
'<output_parameters>',
'<o_p>',
'<parameter_list>',
'<nextpl>',
'<return_stmt>',
'<r_s>'
]

terminals = [
'TK_ASSIGN',	'TK_ID',	'TK_NUM', 'TK_RNUM',	'TK_IPP',	
'TK_OPP',	'TK_FUNC',	'TK_OSQ', 'TK_CSQ',	'TK_SCLN',	
'TK_RET',	'TK_END',	'TK_MAIN',	'TK_INT',	'TK_FLOAT',	
'TK_READ',	'TK_CALL',	'TK_PRINT',	'TK_PRINTLN',	'TK_ORD',	
'TK_CRD',	'TK_WHILE',	'TK_EWHILE',	'TK_IF',	'TK_ENDIF',	
'TK_ELSE',	'TK_EQ',	'TK_LTE',	'TK_LESS',	'TK_GTE',	
'TK_GRTR',	'TK_NOT',	'TK_NOTEQ',	'TK_AND',	'TK_OR',	
'TK_PLUS',	'TK_MINUS',	'TK_MUL',	'TK_DIV',	'TK_BREAK',	
'TK_COMMA',	'TK_GLOBAL',	'TK_VOID',	'$',	'TK_STRLIT'
]

BoolTerms = [
'TK_AND','TK_OR','TK_EQ','TK_LTE',
'TK_LESS','TK_GRTR','TK_GTE','TK_NOTEQ',
'TK_NOT','TK_MINUS','TK_MUL','TK_DIV',
'TK_ORD','TK_CRD','TK_NUM','TK_RNUM']

ArithTerms = [
'TK_PLUS','TK_MINUS','TK_MUL','TK_DIV',
'TK_ORD','TK_CRD','TK_NUM','TK_RNUM']

# stores input paramter and output parameter values for each function name. indexed by lineno+pos of the function declration
functionTab = {}
# stores the keys associated with a function name. | useful in case of function overloading
functionKeyList = {}
