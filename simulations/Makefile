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
	cd src/promote-stable-hot && cargo build --release && cd - > /dev/null

clean:
	${RM} ${RUSTTARGETS}
	rm -rf src/lru/target
	rm -rf src/promote-when-get/target
	rm -rf src/promote-when-second-get
	rm -rf src/promote-when-get-demote-when-full
	rm -rf src/promote-when-second-get-demote-when-full
	rm -rf src/promote-stable-hot

.PHONY: all
