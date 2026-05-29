from Lexer import *

class Parser:
	lex = None
	token = None

	def __init__(self, filepath):
		self.lex = Lexer(filepath)
		self.token = None

		""" DEFINE FIRST SET """
		self.firstPrimaryExpression = set((Tag.ID, Tag.NUMBER, Tag.TRUE, Tag.FALSE, ord('(')))
		self.firstUnaryExpression = self.firstPrimaryExpression.union( set((ord('-'), ord('!'))) )
		self.firstExtendedMultiplicativeExpression = set((ord('*'), ord('/'), Tag.MOD))
		self.firstMultiplicativeExpression = self.firstUnaryExpression
		self.firstExtendedAdditiveExpression = set((ord('+'), ord('-')))
		self.firstAdditiveExpression = self.firstMultiplicativeExpression

	def error(self, extra = None):
		text = 'Line ' + str(self.lex.line) + " - " 
		if extra == None:
			text = text + "."
		else:
			text = text + extra
		raise Exception(text)

	def check(self, tag):
		if self.token.tag == tag:
			self.token = self.lex.scan()
			#print("", self.token)
		else:
			text = 'expected '
			if self.token.tag != Tag.ID:
				#print("tag = ", self.token.tag)
				aux = Token(tag)
				text = text + str(aux) + " before " + str(self.token) 
			else:
				text = text + "an identifier before " + str(self.token) 
			self.error(text)
	
	def analize(self):
		self.token = self.lex.scan()
		self.program()
		if self.token.tag == Tag.EOF:
			print("ACCEPTED")
	
	#<primary-expression> ::= <identifier> || <number> || <true>	|| <false> ||  '(' <expression> ')'
	def primaryExpression(self):
		if self.token.tag in self.firstPrimaryExpression:
			if self.token.tag == Tag.ID:
				self.check(Tag.ID)
			elif self.token.tag == Tag.NUMBER:
				self.check(Tag.NUMBER)
			elif self.token.tag == Tag.TRUE:
				self.check(Tag.TRUE)
			elif self.token.tag == Tag.FALSE:
				self.check(Tag.FALSE)
			elif self.token.tag == ord('('):
				self.check(ord('('))
				self.expression()
				self.check(ord(')'))
		else:
			self.error("expected a primary expression before " + str(self.token)) 

	#<unary-expression> ::= '-' <unary-expression> || '!' <unary-expression> || <primary-expression>
	def unaryExpression(self):
		if self.token.tag in self.firstUnaryExpression:
			if self.token.tag == ord('-'):
				self.check(ord('-'))
				self.unaryExpression()
			elif self.token.tag == ord('!'):
				self.check(ord('!'))
				self.unaryExpression()
			else:
				self.primaryExpression()
		else: 
			self.error("expected an unary expression before " + str(self.token))

	#<extended-multiplicative-expression> ::= '*' <unary-expression> <extended-multiplicative-expression>
	#<extended-multiplicative-expression> ::= '/' <unary-expression> <extended-multiplicative-expression>
	#<extended-multiplicative-expression> ::= MOD <unary-expression> <extended-multiplicative-expression>
	#<extended-multiplicative-expression> ::= ' '
	def extendedMultiplicativeExpression(self):
		if self.token.tag in self.firstExtendedMultiplicativeExpression:
			if self.token.tag == ord('*'):
				self.check(ord('*'))
				self.unaryExpression()
				self.extendedMultiplicativeExpression()
			elif self.token.tag == ord('/'):
				self.check(ord('/'))
				self.unaryExpression()
				self.extendedMultiplicativeExpression()
			elif self.token.tag == Tag.MOD:
				self.check(Tag.MOD)
				self.unaryExpression()
				self.extendedMultiplicativeExpression()
		else:
			pass

	#<multiplicative-expression> ::= <unary-expression> <extended-multiplicative-expression>
	def multiplicative_expression(self):
		if self.token.tag in self.firstMultiplicativeExpression:
			self.unaryExpression()
			self.extendedMultiplicativeExpression()
		else:
			self.error("expected a multiplicative expression before " + str(self.token))

	#<extended-additive-expression> ::= '+' <multiplicative-expression> <extended-additive-expression>
	#<extended-additive-expression> ::= '-' <multiplicative-expression> <extended-additive-expression>
	#<extended-additive-expression> ::= ' '
	def extended_additive_expression(self):
		if self.token.tag in self.firstExtendedAdditiveExpression:
			if self.token.tag == ord('+'):
				self.check(ord('+'))
				self.multiplicative_expression()
				self.extended_additive_expression()
			elif self.token.tag == ord('-'):
				self.check(ord('-'))
				self.multiplicative_expression()
				self.extended_additive_expression()
		else:
			pass
	#<additive-expression> ::= <multiplicative-expression> <extended-additive-expression>
	def additive_expression(self):
		if self.token.tag in self.firstAdditiveExpression:
			if self.token.tag in self.firstMultiplicativeExpression:
				self.multiplicative_expression()
				self.extended_additive_expression()
			else:
				self.error("expected a multiplicative expression before " + str(self.token))
		else:
			self.error("expected an additive expression before " + str(self.token))

	#<extended-relational-expression> := '<' <additive-expression> <extended-relational-expression>
	#<extended-relational-expression> ::= '<''=' <additive-expression> <extended-relational-expression>
	#<extended-relational-expression> := '>' <additive-expression> <extended-relational-expression>
	#<extended-relational-expression> ::= '>''=' <additive-expression> <extended-relational-expression>
	#<extended-relational-expression> ::= ' '
	def extended_relational_expression(self):
		if self.token.tag == ord('<'):
			self.check(ord('<'))
			self.additive_expression()
			self.extended_relational_expression()
		elif self.token.tag == Tag.LE:
			self.check(Tag.LE)
			self.additive_expression()
			self.extended_relational_expression()
		elif self.token.tag == ord('>'):
			self.check(ord('>'))
			self.additive_expression()
			self.extended_relational_expression()
		elif self.token.tag == Tag.GE:
			self.check(Tag.GE)
			self.additive_expression()
			self.extended_relational_expression()
		else:
			pass
	
	#<relational-expression> ::= <additive-expression> <extended-relational-expression>
	def relational_expression(self):
		if self.token.tag in self.firstAdditiveExpression:
			self.additive_expression()
			self.extended_relational_expression()
		else:
			self.error("expected an additive expression before " + str(self.token))
	
	#<extended-equality-expression> := '=' <relational-expression> <extended-equality-expression>
	#<extended-equality-expression> := '<''>' <relational-expression> <extended-equality-expression>
	#<extended-equality-expression> ::= ' '
	def extended_equality_expression(self):
		if self.token.tag == ord('='):
			self.check(ord('='))
			self.relational_expression()
			self.extended_equality_expression()
		elif self.token.tag == Tag.NE:
			self.check(Tag.NEQ)
			self.relational_expression()
			self.extended_equality_expression()
		else:
			pass
	
	#<equality-expression> ::= <relational-expression> <extended-equality-expression>
	def equality_expression(self):
		if self.token.tag in self.firstAdditiveExpression:
			self.relational_expression()
			self.extended_equality_expression()
		else:
			self.error("expected an additive expression before " + str(self.token))
	
	#<extended-conditional-term> ::= AND <equality-expression> <extended-conditional-term>
	#<extended-boolean-term> ::= ' '
	def extended_conditional_term(self):
		if self.token.tag == Tag.AND:
			self.check(Tag.AND)
			self.equality_expression()
			self.extended_conditional_term()
		else:
			pass

	#<conditional-term> ::= <equality-expression> <extended-conditional-term>
	def conditional_term(self):
		if self.token.tag in self.firstAdditiveExpression:
			self.equality_expression()
			self.extended_conditional_term()
		else:
			self.error("expected an additive expression before " + str(self.token))
	
	#<extended-conditional-expression> ::= OR <conditional-term> <extended-conditional-expression>
	#<extended-conditional-expression> ::= ' '
	def extended_conditional_expression(self):
		if self.token.tag == Tag.OR:
			self.check(Tag.OR)
			self.conditional_term()
			self.extended_conditional_expression()
		else:
			pass

	#<conditional-expression> ::= <conditional-term> <extended-conditional-expression>
	def conditional_expression(self):
		if self.token.tag in self.firstAdditiveExpression:
			self.conditional_term()
			self.extended_conditional_expression()
		else:
			self.error("expected an additive expression before " + str(self.token))
	
	#<expression> ::= <conditional-expression>
	def expression(self):
		if self.token.tag in self.firstAdditiveExpression:
			self.condional_expression()
		else:
			self.error("expected an additive expression before " + str(self.token))
	
	#<text-statement> ::= PRINT '(' <expression> )'
	def text_statement(self):
		if self.token.tag == Tag.PRINT:
			self.check(Tag.PRINT)
			self.check(ord('('))
			self.expression()
			self.check(ord(')'))
		else:
			self.error("expected PRINT before " + str(self.token))

	#<assigment-statement> ::= <identifier> ':''=' <expression>
	
	#<statement> ::= <assignment-statement> | <text-statement>
	
	#<statement-sequence> ::= <statement> <statement-sequence>
	#<statement-sequence> ::= ' '
	
	#<identifier-list> ::= ',' <identifier> <identifier-list>
	#<identifier-list> ::= ' '
	
	#<declaration-sequence> ::= VAR <identifier> <identifier-list>
	
	#<program> ::= <declaration-sequence> <statement-sequence>
	def program(self):
		if self.token.tag in self.firstProgram:
			self.declarationSequence()
			self.statementSequence()
		else: 
			self.error("expected a program before " + str(self.token))
		