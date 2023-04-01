# CSS-Selector-Minifier

CSS-Selector-Minifier is a Python package that minifies CSS class and id names in CSS, HTML and JavaScript files. It's a custom made project and it may not meet your requirements. I decided to share my code with you because I also couldn't find a working minifer selector.

## Installation

You can install the package using pip:

```
pip install css-selector-minifier
```

# Usage

## ** Important note **

**You have to prepare your code to make my code work**.

CSS-Selector-Minifier uses a regex pattern to find your CSS selectors, and that regex pattern needs an unique prefix.

By default, CSS-Selector-Minifier uses the prefix `'-s-'` for the beginning of the CSS selector and `'-e-'` for the end.

## Example for preparation

If you want to use `default` prefix:

CSS that **won't work**
```css
.main {
  background: yellow;
  font-size: 10px;
  opacity: 0.5;
}

#child {
  background: grey;
  font-size: 21px;
  opacity: 0.51;
}

.bettermain, .betterchild {
  background: yellow;
  font-size: 10px;
  opacity: 0.5;
}

.child .main {
  color: grey;
}
```

CSS that **will work**
```css
.-s-main-e- {
  background: yellow;
  font-size: 10px;
  opacity: 0.5;
}

#-s-child-e- {
  background: grey;
  font-size: 21px;
  opacity: 0.51;
}

.-s-bettermain-e-, .-s-betterchild-e- {
  background: yellow;
  font-size: 10px;
  opacity: 0.5;
}

.-s-child-e- .-s-main-e- {
  color: grey;
}
```


## CSS-Selector-Minifier arguments

- `css`: a list of paths to CSS files. (optional)
- `html`: a list of paths to HTML files. (optional)
- `js`: a list of paths to JavaScript files. (optional)
- `start_prefix`: a string to prefix the start of the class or id to be minified (default: -s-).
- `end_prefix`: a string to prefix the end of the class or id to be minified (default: -e-).
- `min_letters`: an integer representing the minimum length of the minified class or id name (default: 1).

## CSS-Selector-Minifier methods
- `Get_All_CSS_Selectors()`: returns a set of all CSS selectors in the specified CSS files.
- `Generate_Minifed_Selectors()`: returns a generator object containing smart generated minified CSS selectors.
- `Generate_Map_For_CSS_Selectors()`: returns a dictionary mapping original CSS selectors to their minified counterparts.
- `Replace_CSS_Selectors_With_Minifed(backup=True)`: replaces all CSS selectors in the specified CSS, HTML, and JavaScript files with their minified counterparts. If backup is set to True, a backup copy of each file will be created with a .bak extension.
- `Minify(backup=True)`: perform minification. If backup is set to True, a backup copy of each file will be created with a .bak extension.

# Example
Before CSS-Selector-Minifier

style.css
```css
.-s-main-e- {
  background: yellow;
  font-size: 10px;
  opacity: 0.5;
}

#-s-child-e- {
  background: grey;
  font-size: 21px;
  opacity: 0.51;
}

.-s-bettermain-e-, .-s-betterchild-e- {
  background: yellow;
  font-size: 10px;
  opacity: 0.5;
}

.-s-child-e- .-s-main-e- {
  color: grey;
}
```

index.html
```html
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>Test</title>
</head>
<body>
	<div class="-s-main-e-">
		<p id="-s-child-e-">Lorem ipsum. child</p>
		<form id="main">
			<input>
		</form>
	</div>
	<div class="-s-bettermain-e-">
		<p class="-s-betterchild-e-">Lorem ipsum. betterchild</p>
	</div>
</body>
</html>
```

main.js
```js
$(document).ready(function() {
	$('.-s-child-e-').text('jquery is working')
	$('#-s-child-e-').attr('message', 'child')
});
```

After CSS-Selector-Minifier

style.css
```css
.ae {
  background: yellow;
  font-size: 10px;
  opacity: 0.5;
}

#ad {
  background: grey;
  font-size: 21px;
  opacity: 0.51;
}

.ac, .aa {
  background: yellow;
  font-size: 10px;
  opacity: 0.5;
}

.ab .ae {
  color: grey;
}
```

index.html
```html
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>Test</title>
</head>
<body>
	<div class="ae">
		<p id="ab">Lorem ipsum. child</p>
		<form id="main">
			<input>
		</form>
	</div>
	<div class="ac">
		<p class="aa">Lorem ipsum. betterchild</p>
	</div>
</body>
</html>
```

main.js
```js
$(document).ready(function() {
	$('.ab').text('jquery is working')
	$('#ab').attr('message', 'child')
});
```

main.py
```python
from css_selector_minifier import Minify_CSS_Names

m = Minify_CSS_Names(
  css=['src/style.css'],
  html=['src/index.html'],
  js=['src/main.js'],
  start_prefix='-s-',
  end_prefix='-e-',
  min_letters=2
)

m.Minify()

```

src folder after running Minify_CSS_Names with default backup arg in m.Replace_CSS_Selectors_With_Minifed()

![image](https://user-images.githubusercontent.com/80158535/224487520-19151673-12d2-4f7c-a05a-e7a840f5b460.png)

This will replace the CSS selectors in your files with minified selectors.

By default, the package will back up your files before replacing the selectors. You can disable this by passing backup=False to the Replace_CSS_Selectors_With_Minifed method.

# Note

You can use glob for paths to files

```python
from css_selector_minifier import Minify_CSS_Names
import glob

m = Minify_CSS_Names(
  css=glob.glob('src/*.css'),
  html=glob.glob('src/*.html'),
  js=glob.glob('src/*.js'),
  start_prefix='-s-',
  end_prefix='-e-',
  min_letters=2
)

m.Minify()
```
