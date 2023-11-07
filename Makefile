.PHONY: all test venv clean

VENV=.venv

all: test

test: requirements.txt venv
	. $(VENV)/bin/activate && py.test tests

clean:
	rm -rf .venv
	rm -rf rmdparser/__pycache__

venv: .venv/touchfile

.venv/touchfile: requirements.txt
	test -d $(VENV) || python3 -m venv $(VENV) && . $(VENV)/bin/activate &&  $(VENV)/bin/python -m pip install -r requirements.txt && touch $(VENV)/touchfile


