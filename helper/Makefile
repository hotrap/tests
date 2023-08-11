RM	= rm -f
bin/%: %.rs
	@mkdir -p bin
	rustc $^ -C opt-level=3 -C debuginfo=0 -o $@

RUSTSRCS	:= $(wildcard *.rs)
RUSTTARGETS	:= $(patsubst %.rs,bin/%,$(RUSTSRCS))

all: ${RUSTTARGETS}
	cd read-keys-from-dump && cargo build --release && cd - > /dev/null

clean:
	${RM} ${RUSTTARGETS}

.PHONY: all
