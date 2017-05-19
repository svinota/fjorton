# 	Copyright (c) 2013-2014 Peter V. Saveliev
#
# 	This file is part of Fjorton project.
#
# 	Fjorton is free software; you can redistribute it and/or modify
# 	it under the terms of the GNU General Public License as published by
# 	the Free Software Foundation; either version 2 of the License, or
# 	(at your option) any later version.
#
# 	Fjorton is distributed in the hope that it will be useful,
# 	but WITHOUT ANY WARRANTY; without even the implied warranty of
# 	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# 	GNU General Public License for more details.
#
# 	You should have received a copy of the GNU General Public License
# 	along with Fjorton; if not, write to the Free Software
# 	Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

##
# Version and release
#
version ?= 0.1
release := $(shell git describe | sed 's/-[^-]*$$//;s/-/.post/')
##
# Python-related configuration
#
python ?= python
nosetests ?= nosetests
flake8 ?= flake8

##
# Other options
#
# root      -- install root (default: platform default)
# lib       -- lib installation target (default: platform default)
# coverage  -- whether to produce html coverage (default: false)
# pdb       -- whether to run pdb on errors (default: false)
# module    -- run only the specified test module (default: run all)
#
ifdef root
	override root := "--root=${root}"
endif

ifdef lib
	override lib := "--install-lib=${lib}"
endif

all:
	@echo targets:
	@echo
	@echo \* clean -- clean all generated files
	@echo \* test -- run tests
	@echo \* install -- install lib into the system
	@echo \* develop -- run \"setup.py develop\" \(requires setuptools\)
	@echo

clean: clean-version
	@rm -rf dist build MANIFEST
	@rm -f  tests/.coverage
	@rm -rf tests/cover
	@rm -f  tests/*xml
	@rm -rf fjorton.egg-info
	@find fjorton -name "*pyc" -exec rm -f "{}" \;
	@find fjorton -name "*pyo" -exec rm -f "{}" \;

setup.ini:
	@awk 'BEGIN {print "[setup]\nversion=${version}\nrelease=${release}"}' >setup.ini

clean-version:
	@rm -f setup.ini

force-version: clean-version update-version

update-version: setup.ini

test:
	@python2 `which nosetests` -v \
		--with-coverage \
		--cover-package=fjorton \
		--cover-html

upload: clean force-version
	${python} setup.py sdist upload

dist: clean force-version
	@${python} setup.py sdist >/dev/null 2>&1

install: clean force-version
	${python} setup.py install ${root} ${lib}

uninstall: clean
	${python} -m pip uninstall fjorton

develop: setuplib = "setuptools"
develop: clean force-version
	${python} setup.py develop
