#when you run 'make' in the terminal, it will run the help command
#use '@' in front of command so that it won't show up in the terminal when you run it

hello: # hello world
	@echo "hello world this is my first make command"

install: # install requirements
	@echo "Installing ... "
	poetry install
