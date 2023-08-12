RM	= rm -f
%: src/%.rs
	rustc $^ -C opt-level=3 -C debuginfo=0 -o $@

RUSTSRCS	:= $(wildcard src/*.rs)
RUSTTARGETS	:= $(patsubst src/%.rs,%,$(RUSTSRCS))

all: ${RUSTTARGETS}
	cd src/lru && cargo build --release && cd - > /dev/null
	cd src/promote-when-get && cargo build --release && cd - > /dev/null
	cd src/promote-when-second-get && cargo build --release && cd - > /dev/null
	cd src/promote-when-get-demote-when-full && cargo build --release && cd - > /dev/null
	cd src/promote-when-second-get-demote-when-full && cargo build --release && cd - > /dev/null

clean:
	${RM} ${RUSTTARGETS}

.PHONY: all
