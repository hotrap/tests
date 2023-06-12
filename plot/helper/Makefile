RM	= rm -f
%: %.rs
	rustc $^ -C opt-level=3 -C debuginfo=0 -o $@

RUSTSRCS	:= $(wildcard *.rs)
RUSTTARGETS	:= $(patsubst %.rs,%,$(RUSTSRCS))

all: ${RUSTTARGETS}
	cd src/hit && cargo build --release && cd - > /dev/null

clean:
	${RM} ${RUSTTARGETS}

.PHONY: all
