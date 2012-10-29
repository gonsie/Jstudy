from bs4 import BeautifulSoup
import re
import sys

class Clue:
	def __init__(self, clue_html):
		c = clue_html.find('div')
		temp = c.get('onclick').split("'")[1].split("_")
		self.round = temp[1] # J, DJ, FJ
		if self.round != "FJ":
			self.value = c.find(class_=re.compile("clue_value")).text
			self.x = int(temp[2]) # col
			self.y = int(temp[3]) # row
		else:
			self.value = -1
			self.x = 1
			self.y = 1
		# daily double flag
		if c.find(class_="clue_value"):
			self.special = False
		else:
			self.special = True
		self.text = ''.join(c.get('onmouseout').split(",")[2:])[0:-1]
		temp = BeautifulSoup(''.join(c.get('onmouseover').split(",")[2:]))
		self.soln = temp.find(class_=re.compile("correct_response")).text
		# print "clue__init", str(self.round), str(self.x), str(self.y)

	def __repr__(self):
		output = ""
		output += "Q: " + self.text + "\tA: " + self.soln
		return output


class Category:
	def __init__(self, category_html, col):
		self.name = category_html.find(class_="category_name").text
		self.clues = []
		self.col = col
		# print "category__init:", self.name

	def append(self, clue):
		self.clues.append(clue)

	def __repr__(self):
		output = ""
		output += self.name + "\n"
		for clue in self.clues:
			output += "\t" + str(clue) + "\n"
		return output

class Game:
	def __init__(self, game_html):
		self.rounds = []
		for round in game_html.find_all(id=re.compile("jeopardy_round")):
			self.rounds.append([])
			counter = 0
			for category in round.find_all(class_="category"):
				self.rounds[-1].append(Category(category, counter))
				counter += 1
			for clue in round.find_all(class_="clue"):
				# special case for final jeopardy
				if counter == 1:
					temp = round.find(class_="category")
					self.rounds[-1][0].append(Clue(temp))
				# empty spots for unreached clues
				elif len(list(clue.children)) > 1:
					self.rounds[-1][counter % 6].append(Clue(clue))
				counter += 1

	def __repr__(self):
		output = ""
		for r in self.rounds:
			for c in r:
				output += str(c)
		return output

def main(html_file_name):
	soup = BeautifulSoup(open(html_file_name))
	g = Game(soup)
	print g

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print "Usage: python", sys.argv[0], "html_file_name"
	else:
		main(sys.argv[1])
