# Demo Options
GPU = 10de:1b80
AUD = 10de:10f0
LSPCI_OPTS = -nnk
PEARAPCI_OPTS = -v
DEVICES := $(GPU) $(AUD)
$(foreach device,$(DEVICES), \
    $(eval PEARAPCI_OPTS+= -d $(device)) \
)
# Asciinema Options
TITLE = "[32m  pearapci demo  "
COLS = 120
ROWS = 24
ASCIINEMA_OPTS :=\
--stdin \
--overwrite \
--cols=$(COLS) \
--rows=$(ROWS)
# Agg Options
FONT_FAMILY = "Iosevka Peara,DejaVu Sans Mono,Symbols Nerd Font Mono" # Customized Iosevka font, used for custom glyphs in demo. Replace with your own font.
FONT_SIZE = 14
FPS = 60
RENDERER = fontdue
THEME = "1c1b19,fce8c3,1c1b19,ef2f27,519f50,fbb829,2c78bf,e02c6d,0aaeb3,baa67f,918175,f75341,98bc37,fed06e,68a8e4,ff5c8f,2be4d0,fce8c3" # srcery colors
AGG_OPTS :=\
--font-family $(FONT_FAMILY) \
--font-size $(FONT_SIZE) \
--fps-cap $(FPS) \
--renderer $(RENDERER) \
--theme $(THEME)

clean:
	sudo pearapci $(PEARAPCI_OPTS) device remove rescan
	rm demo.cast
	rm demo.gif

lspci:
	@for device in $(DEVICES); do \
		lspci $(LSPCI_OPTS) -d $$device; \
	done

demo.cast:
	GPU=$(GPU) AUD=$(AUD) ./demo.zsh | asciinema rec -i 2 $(ASCIINEMA_OPTS) $@

demo.gif: demo.cast
	agg $(AGG_OPTS) $< $@


all:
demo: demo.cast demo.gif

.PHONY: clean lspci demo all
