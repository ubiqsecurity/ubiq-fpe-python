QUIET		:= @

all:

check:
	$(QUIET)mypy .

test:
	$(QUIET)python3 test.py

testv:
	$(QUIET)python3 test.py -v

clean:
	$(QUIET)rm -f *~

distclean: clean
	$(QUIET)rm -rf __pycache__
	$(QUIET)rm -rf .mypy_cache

.PHONY: all check test testv clean distclean
