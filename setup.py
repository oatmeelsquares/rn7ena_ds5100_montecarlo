from setuptools import setup

setup(
	name = "Monte Carlo Simulator",
	version = "0.1",
	description = "DS5100 Final project",
	url = "https://github.com/oatmeelsquares/rn7ena_ds5100_montecarlo",
	author = "Becky Desrosiers",
	license = "LICENSE.txt",
	long_description = "README.md",
	packages = ["montecarlo"],
	install_requires = ["numpy >= 1.11.1", "pandas >= 1.0"],
)
