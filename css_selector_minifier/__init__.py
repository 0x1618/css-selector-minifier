#	                                              .__                 __                                 .__       .__  _____.__              
#	  ____   ______ ______           ______ ____ |  |   ____   _____/  |_  ___________            _____ |__| ____ |__|/ ____\__| ___________ 
#	_/ ___\ /  ___//  ___/  ______  /  ___// __ \|  | _/ __ \_/ ___\   __\/  _ \_  __ \  ______  /     \|  |/    \|  \   __\|  |/ __ \_  __ \
#	\  \___ \___ \ \___ \  /_____/  \___ \\  ___/|  |_\  ___/\  \___|  | (  <_> )  | \/ /_____/ |  Y Y  \  |   |  \  ||  |  |  \  ___/|  | \/
#	 \___  >____  >____  >         /____  >\___  >____/\___  >\___  >__|  \____/|__|            |__|_|  /__|___|  /__||__|  |__|\___  >__|   
#	     \/     \/     \/               \/     \/          \/     \/                                  \/        \/                  \/       
#
# Author: Maksymilian Sawicz (max.sawicz@gmail.com)
# Code under MIT License
# Basically, to use my code you just need to include my name and my e-mail wherever you use this code.

from itertools import combinations_with_replacement, chain
from string import ascii_letters
from math import ceil
from shutil import copyfile
from time import time
import re

class Minify_CSS_Names():
	"""
	Class for minifying CSS selectors in a given CSS file(s) and replacing them with shortened selectors.

	Args:
		css (list): List of CSS file paths to be minified.
		html (list): List of HTML file paths to be checked for CSS selectors to be minified.
		js (list): List of JS file paths to be checked for CSS selectors to be minified.
		start_prefix (str): Prefix added at the start of the selector to be minified.
		end_prefix (str): Prefix added at the end of the selector to be minified.
		min_letters (int): Minimum number of letters in the minified selector.
		start_selector (str): Unique prefix that you want to put at the start of the minifed selector.
		end_selector (str): Unique prefix that you want to put at the end of the minifed selector.

	Raises:
		ValueError: If `min_letters` is zero or negative.

	Attributes:
		prefix (dict): Dictionary containing start and end prefixes.
		css (list): List of CSS file paths to be minified.
		css_selectors (set): Set of unique CSS selectors found in `css` files.
		name_map (dict): Dictionary containing mapping of CSS selectors with their minified counterparts.
		html (list): List of HTML file paths to be checked for CSS selectors to be minified.
		js (list): List of JS file paths to be checked for CSS selectors to be minified.
		min_letters (int): Minimum number of letters in the minified selector.
		regex_pattern (str): Regular expression pattern to match CSS selectors.
		start_selector (str): Unique prefix that you want to put at the start of the minifed selector.
		end_selector (str): Unique prefix that you want to put at the end of the minifed selector.

	Methods:
		Get_All_CSS_Selectors(self) -> set:
			Returns a set of unique CSS selectors found in `css` files.

		Generate_Minifed_Selectors(self) -> generator:
			Returns a generator object which yields a series of minified selectors.

		Generate_Map_For_CSS_Selectors(self) -> dict:
			Returns a dictionary containing mapping of CSS selectors with their minified counterparts.

		Replace_CSS_Selectors_With_Minifed(self, backup=True) -> None:
			Replaces all CSS selectors in `css`, `html` and `js` files with their minified counterparts.
			If `backup` is True, creates a backup of the original files before making changes.

		Minify(self, backup=True) -> None:
			Perfoms minification using above functions.
	"""

	def __init__(self, css=None, html=None, js=None, start_prefix='-s-', end_prefix='-e-', min_letters=1, start_selector='', end_selector=''):
		self.prefix = {
			'start-prefix': start_prefix,
			'end-prefix': end_prefix
		}

		self.css = css if css else []
		self.css_selectors = set()
		self.name_map = {}
		self.html = html if html else []
		self.js = js if js else []

		self.min_letters = min_letters
		self.start_selector = start_selector
		self.end_selector = end_selector

		self.regex_pattern = rf'([.#])({self.prefix["start-prefix"]}[a-zA-Z0-9_-]+{self.prefix["end-prefix"]})'

		if self.min_letters <= 0:
			raise ValueError("min_letters cannot be equal to 0 or less than 0")

	def Get_All_CSS_Selectors(self) -> set:
		"""
		Returns a set of unique CSS selectors found in `css` files.

		Returns:
			set: Set of unique CSS selectors.
		"""

		paths = self.css

		for path in paths:
			with open(path, 'rb') as css_file:
				css = css_file.read().decode()
				for selector in re.findall(self.regex_pattern, css, re.MULTILINE):
					selector = ''.join(selector)
					selectors = filter(lambda selector: selector != '', selector.replace(',', '').split(' '))
					for selector in selectors:
						selector = selector.replace('\t', '')
						if not re.search(self.regex_pattern, selector):
							continue
						self.css_selectors.add(selector)

		return self.css_selectors

	def Generate_Minifed_Selectors(self) -> chain.from_iterable:
		"""
		Returns a generator object which yields a series of minified selectors.

		Returns:
			generator: Generator object which yields minified selectors.
		"""

		n = ceil(len(self.css_selectors) / len(ascii_letters)) + self.min_letters
		combinations = []
		for n_ in range(self.min_letters, n + 1):
			combinations.append(combinations_with_replacement(ascii_letters, n_))

		return chain.from_iterable(combinations)

	def Generate_Map_For_CSS_Selectors(self) -> dict:
		"""
		Returns a dictionary containing mapping of CSS selectors with their minified counterparts.

		Returns:
			dict: Dictionary containing mapping of CSS selectors with their minified counterparts.
		"""

		generator = self.Generate_Minifed_Selectors()
		for selector in self.css_selectors:
			self.name_map[selector] = selector[0] + self.start_selector + ''.join(next(generator)) + self.end_selector

		return self.name_map

	def Replace_CSS_Selectors_With_Minifed(self, backup=True) -> None:
		"""
		Replaces all CSS selectors in `css`, `html` and `js` files with their minified counterparts.
		If `backup` is True, creates a backup of the original files before making changes.

		Args:
			backup (bool, optional): Whether to create a backup of the original files before making changes. Defaults to True.
		Returns:
			None
		"""

		for path in self.css + self.html + self.js:
			with open(path, 'a+', encoding='utf-8') as file:
				file.seek(0)
				new_css = file.read()

				for old_selector, new_selector in self.name_map.items():
					if path.split('.')[-1] in ['html', 'js']:
						old_selector = ''.join(list(old_selector)[1:])
						new_selector = ''.join(list(new_selector)[1:])
						new_css = new_css.replace(old_selector, new_selector)
					else:
						new_css = new_css.replace(old_selector, new_selector)

				if backup:
					copyfile(path, path + f'-{time()}.bak')

				file.truncate(0)
				file.write(new_css)
	
	def Minify(self, backup=True) -> None:
		"""
		Perform minification.

		Args:
			backup (bool, optional): Whether to create a backup of the original files before making changes. Defaults to True.
		Returns:
			None
		"""

		self.Get_All_CSS_Selectors()
		self.Generate_Map_For_CSS_Selectors()
		self.Replace_CSS_Selectors_With_Minifed(backup=backup)

if __name__ == "__main__":
	import glob
	m = Minify_CSS_Names(
		css=['main.css'],
		html=[],
		js=[],
		start_prefix='-s-',
		end_prefix='-e-',
		min_letters=2,
		start_selector='l',
		end_selector='s'
	)

	m.Minify()