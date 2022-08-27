# Make
# Make is verbose in Linux. Make it silent.
# MAKEFLAGS += --silent

.PHONY: all

all:
	@echo "Compiling trane_bacnet:" $^
	./make.py

release:
	@echo "Release trane_bacnet:" $^
	./release.sh

clean:
	@echo "Clean trane_bacnet:" $^
	rm -rf trane_bacnet_release bacnet_test_release