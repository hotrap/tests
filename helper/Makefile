RM	= rm -f
bin/%: %.rs
	@mkdir -p bin
	rustc $^ -C opt-level=3 -C debuginfo=0 -o $@

RUSTSRCS	:= $(wildcard *.rs)
RUSTTARGETS	:= $(patsubst %.rs,bin/%,$(RUSTSRCS))

all: ${RUSTTARGETS}
	cd src/hit && cargo build --release && cd - > /dev/null
	cd src/latency-after && cargo build --release && cd - > /dev/null
	cd src/read-keys-from-dump && cargo build --release && cd - > /dev/null
	cd src/twitter-to-plain && cargo build --release && cd - > /dev/null
	cd src/analyze-plain && cargo build --release && cd - > /dev/null

clean:
	${RM} ${RUSTTARGETS}
	rm -rf src/hit/target
	rm -rf src/latency-after/target
	rm -rf src/read-keys-from-dump/target
	rm -rf src/twitter-to-plain/target
	rm -rf src/analyze-plain/target

.PHONY: all
