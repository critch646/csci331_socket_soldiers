# Makefile for CSCI 331 Socket Soldiers Project
# @author: Zeke Critchlow
# @Date: 2023/04/03

# Directories
virtualEnvDir = .venv
projectDir = project/

# Files
requirementsFile = requirements.txt
serverFile = socksy_server
clientFile = socksy_client



.PHONY: help run_client run_server install uninstall clean

help:
	@echo "CSCI 331 Makefile Commands:"
	@echo "make install"
	@echo "  Creates Python virtual enviornment and installs packages in requirements.txt."
	@echo "make uninstall"
	@echo "  Removes Python virtual enviornment."
	@echo "make run_client"
	@echo "  Runs Socksy client using the virtual enviornment."
	@echo "make run_server"
	@echo "  Runs Socksy server using the virtual enviornment."
	@echo "make clean"
	@echo "  Removes .pyc files from cache."

run_client:
	( \
		. $(projectDir)$(virtualEnvDir)/bin/activate; \
		cd $(projectDir); \
		python3 -m $(clientFile); \
	)

run_server:
	( \
		. $(projectDir)$(virtualEnvDir)/bin/activate; \
		cd $(projectDir); \
		python3 -m $(serverFile); \
	)

install: requirements.txt
	( \
		python3 -m venv $(projectDir)$(virtualEnvDir); \
		. $(projectDir)$(virtualEnvDir)/bin/activate; \
		python3 -m pip install -r $(requirementsFile); \
	)

uninstall: 
	rm -Rf  $(projectDir)$(virtualEnvDir)

clean:
	find -iname "*.pyc" -delete