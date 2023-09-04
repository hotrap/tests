RM	= rm -f
bin/%: %.rs
	@mkdir -p bin
	rustc $^ -C opt-level=3 -C debuginfo=0 -o $@

RUSTSRCS	:= $(wildcard *.rs)
RUSTTARGETS	:= $(patsubst %.rs,bin/%,$(RUSTSRCS))

all: ${RUSTTARGETS}
	cd src/read-keys-from-dump && cargo build --release && cd - > /dev/null
	cd src/latency-percentile && cargo build --release && cd - > /dev/null

clean:
	${RM} ${RUSTTARGETS}

.PHONY: all
