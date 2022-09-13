QUIET		:= @

all:

check:
	$(QUIET)mypy .

test:
	$(QUIET)python3 test.py

testv:
	$(QUIET)python3 test.py -v

.PHONY: all check test testv
