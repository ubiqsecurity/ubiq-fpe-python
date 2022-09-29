QUIET		:= @

all:

check:
	$(QUIET)mypy .

test:
	$(QUIET)PYTHONPATH=$$(pwd)/.. python3 -m unittest discover -p '*_test.py'

testv:
	$(QUIET)PYTHONPATH=$$(pwd)/.. python3 -m unittest discover -p '*_test.py' -v

clean:
	$(QUIET)rm -f *~

distclean: clean
	$(QUIET)rm -rf __pycache__
	$(QUIET)rm -rf .mypy_cache

.PHONY: all check test testv clean distclean
