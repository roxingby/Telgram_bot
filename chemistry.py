from chempy import balance_stoichiometry

equation_example = "Write the equation in the form of:\n 'H2 + O2 == H2O'"
balance_error = "Something went wrong during the balance of the equation."

class Chemistry:
	'''
	everything that can be useful in chemistry
	'''

	def __init__(self, equation):
		# makes it that python can understand it
		equation = str(equation).replace(" ", "")
		equation = equation.replace("==", "=")
		equation = equation.replace("=", " == ")
		equation = equation.replace("+", " + ")
		self.equationstring = "".join(equation)

		self.ogequation = self.equationstring
		self.equationstring = self.remove_balance()

		self.equationsplit = self.ogequation.split(" == ")
		self.left = self.equationsplit[0]
		try:
			self.right = self.equationsplit[1]
			self.right_compounds = self.right.split(" + ")
		except:
			self.right = "None"
			self.right_compounds = []
			pass
		self.left_compounds = self.left.split(" + ")

		self.left_elements = []
		self.right_elements = []

	def balance(self):
		#balances equation
		reaction_list, product_list = self.balanceself()
		try:
			reac, prod = balance_stoichiometry(reaction_list, product_list)
		except:
			return False

		reaction = []  # e.g.["2KCl", ...]
		product = []
		final = ""
		# balances
		for compound in reaction_list:  # appends to reaction
			for k, v in reac.items():
				if k == compound:
					if v != 1:
						reaction.append(str(v) + compound)
					if v == 1:
						reaction.append(compound)

		for compound in product_list:  # appends to product
			for k, v in prod.items():
				if k == compound:
					if v != 1:
						product.append(str(v) + compound)
					if v == 1:
						product.append(compound)

		for x in reaction:  # prints from reaction
			if x == reaction[-1]:
				final += x + " == "
			else:
				final += x + " + "

		for x in product:  # prints from product
			if x == product[-1]:
				final += x
			else:
				final += x + " + "
		if "nan" in final:
			return False
		return final

	def getElement(self):
		reaction = {}
		product = {}
		elements = {}
		side = -1
		for part in [self.left_compounds, self.right_compounds]:  # gets both left n right
			side += 1
			for compound in part:
				multiplier = 1
				p1 = len(compound)  # parenthesis place in index
				p2 = -1
				for letter in compound:  # searches for (, int, upper
					# values needed
					element = ""
					number = 1
					plus = 1
					if letter == "(":
						parenthesis_multiplier = int()
						p1 = compound.index("(")  # gets indexes of parenthesises
						p2 = compound.index(")")
						try:
							tempparenthesis = ""
							for ind in range(compound.index(")")+1, len(compound)):
								# searches for int after ")"
								if compound[ind].isdigit():
									tempparenthesis += compound[ind]
								else:
									break
						except IndexError:  # shouldn't ever happen
							pass
						if tempparenthesis != "":
							parenthesis_multiplier = int(tempparenthesis)

					if letter == compound[0]:
						try:
							tempmultiplier = ""
							for ind in range(0, len(compound)):
								if compound[ind].isdigit():
									tempmultiplier += compound[ind]
								else:
									break
						except IndexError:
							pass
						if tempmultiplier != "":
							multiplier = int(tempmultiplier)
					if letter.isupper():  # searches for element with upper
						try:
							# tries to see if its a 2 letter element or not
							index = compound.index(letter)
							if compound[index+1].islower():
								element = compound[index] + compound[index+1]
								plus = 2
							else:
								element = compound[index]
						except IndexError:  # could happen
							element = letter
						try:  # sees for value number of the element
							tempnumber = ""
							for ind in range(index+plus, len(compound)):
								if compound[ind].isdigit():
									tempnumber += compound[ind]
								else:
									break
						except IndexError:
							pass
						if tempnumber != "":
							number = int(tempnumber)
					if element != "":  # checks for new elements and updates olders
						if compound.index(element) < p2 and compound.index(element) > p1:
							number *= parenthesis_multiplier
						if element in elements:
							elements[element] += (number * multiplier)
						if not element in elements:
							elements[element] = number * multiplier
			# checks what side it's working on
			if side == 0:
				reaction = elements
				elements = {}
			else:
				product = elements
				elements = {}
		if product == {} and reaction == {}:
			return False
		elif product == {}:
			return reaction
		elif reaction == {}:
			return product
		return reaction, product

	def returnElements(self):
		reac_prod = [self.getElement()]
		if type(reac_prod[0]) == tuple:
			reac_prod = [reac_prod[0][0], reac_prod[0][1]]
		finalstr = ""
		finalr = "Reaction: "
		finalp = "Product: "
		if reac_prod[0] == False:
			return False
		elif len(reac_prod) == 1:
			final = reac_prod[0]
			for k,v in final.items():
				v = str(v)
				finalstr += k + ": " + v + "\n"
			return finalstr
		elif len(reac_prod) == 2:
			reac = reac_prod[0]
			prod = reac_prod[1]
			for k,v in reac.items():
				v = str(v)
				finalr += k + ": " + v + "; "
			for k,v in prod.items():
				v = str(v)
				finalp += k + ": " + v + "; "
			return finalr + "\n" + finalp





	def printifBalanced(self):
		# prints if the raction is balanced with the product or not

		if self.balance() == False:
			return False
		if self.ogequation == self.balance():
			return "This equation is balanced"
		else:
			return "This equation isn't balanced"

	def check_equation(self):
		equation = list(self.equationstring)
		for ch in equation:
			ch = str(ch)
			ind = equation.index(ch)
			if ch.islower():
				try:
					if equation[ind+1].islower():
						return False
				except IndexError:
					pass
		return True

	def remove_balance(self):
		equation = list(self.equationstring)
		start_at = -1
		while True:
			if equation[0].isdigit():
				equation.remove(equation[0])
			else:
				break
		for ch in equation:
			try:
				ind = equation.index(ch, start_at + 1)
			except ValueError:
				break
			else:
				if equation[ind].isdigit() and equation[ind-1] == " ":
					del equation[ind]
				start_at = ind

		return "".join(equation)

	def balanceself(self):
		equationsplit = self.equationstring.split(" == ")
		left = equationsplit[0]
		try:
			right = equationsplit[1]
			right_compounds = right.split(" + ")
		except:
			right_compounds = []
			pass
		left_compounds = left.split(" + ")
		return left_compounds, right_compounds
