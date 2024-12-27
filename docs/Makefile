GPU = 10de:1b80
AUD = 10de:10f0
DEVICES := $(GPU) $(AUD)
LSPCI_OPTS = -nnk
PEARAPCI_OPTS = -v

$(foreach device,$(DEVICES), \
    $(eval PEARAPCI_OPTS+= -d $(device)) \
)

reset:
	sudo pearapci $(PEARAPCI_OPTS) device remove rescan
	# sudo modprobe -f nvidia

lspci:
	@for device in $(DEVICES); do \
		lspci $(LSPCI_OPTS) -d $$device; \
	done

demo:
	GPU=$(GPU) AUD=$(AUD) ./demo.zsh | asciinema rec --overwrite demo.cast --stdin

clean: reset lspci

.PHONY: clean reset lspci demo
