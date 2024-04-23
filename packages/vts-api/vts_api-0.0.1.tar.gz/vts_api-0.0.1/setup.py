"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
	name="vts-api",

	version="2.0.0",

	description="API Wrapper for VTube Studio",

	long_description=long_description,
	long_description_content_type="text/markdown",

	url="https://github.com/pypa/sampleproject",

	author="Timtaran",
	author_email="timtaran@clowns.dev",
	classifiers=[
		"Development Status :: 1 - Planning",
		"Natural Language :: EnglishNatural Language :: English",
		"Intended Audience :: Developers",
		"Topic :: Software Development :: Build Tools",
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"Programming Language :: Python :: 3.9",
		"Programming Language :: Python :: 3.10",
		"Programming Language :: Python :: 3 :: Only",
	],

	keywords="api, development",
	packages=find_packages(where="src"),

	python_requires=">=3.7, <4",

	install_requires=["websockets", "pydantic", "numpy", "loguru", "ujson"],
	extras_require={
		"dev": ["pytest", "ruff"],
		"test": ["pytest", "ruff"],
	},

	project_urls={
		"Source Code": "https://github.com/Timtaran/vts-api",
		"Bug Reports": "https://github.com/Timtaran/vts-api/issues"
	},
)
