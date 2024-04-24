from setuptools import setup, find_packages

with open("README.md", "r") as f:
	long_description = f.read()

setup(
	name = "PyJsBitwise",
	version = "1.0.2",
	author = "Pairman",
	author_email = "pairmanxlr@gmail.com",
	description = "JavaScript-flavored bitwise operations.",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	license = "GNU General Public License v3 (GPLv3)",
	keywords = ["javascript", "js", "bitwise", "shift"],
	classifiers = [
		"Programming Language :: Python :: 3",
	],
	python_requires = ">= 3.0",
	url = "https://github.com/Pairman/PyJsBitwise",
	project_urls = {
		"Homepage": "https://github.com/Pairman/PyJsBitwise",
		"Changelog": "https://github.com/Pairman/PyJsBitwise/blob/main/CHANGELOG.md",
	},
	packages = find_packages(where = "src", include = ["pyjsbitwise*"]),
	package_dir = {"": "src"},
)
