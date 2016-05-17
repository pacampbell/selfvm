CC = gcc
CFLAGS = -Wall -Werror
BIN = selfhosted
PBIN = pselfhosted
SRC=src
PAYLOAD = sample.data
SNAME = sname
INCLUDE = -Iinclude
SRC = $(wildcard src/*.c)
LIBS =

.PHONY: all clean help check

all: $(BIN) ## Generates all programs that this makefile can generate.

debug: CFLAGS += -g -DDEBUG
debug: $(BIN) ## Generates a binary with debugging symbols and debug print statements.

$(BIN): $(SRC) ## Generates the self hosted progam
	$(CC) $(FLAGS) $(INCLUDE) -o $@ $^ $(LIBS)
	objcopy --add-section $(SNAME)=$(PAYLOAD) $(BIN) $(PBIN)
	@mv $(PBIN) bin
	@rm $(BIN) 

clean: ## Removes all source binaries and object files.
	rm -f $(BIN) $(PBIN) *.o

help: ## Generates this help menu.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

BADFUNCS='[^_.>a-zA-Z0-9](str(n?cpy|n?cat|xfrm|n?dup|str|pbrk|tok|_)|stpn?cpy|a?sn?printf|byte_)'
check: ## Checks program for bad functions.
	@echo Files with potentially dangerous functions.
	@egrep -Hn $(BADFUNCS) $(SRC) || true
