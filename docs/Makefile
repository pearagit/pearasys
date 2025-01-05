# Demo Options
GPU = 10de:1b80
AUD = 10de:10f0
LSPCI_OPTS = -nnk
PEARASYS_OPTS = -v
DEVICES := $(GPU) $(AUD)
$(foreach device,$(DEVICES), \
    $(eval PEARASYS_OPTS+= -d $(device)) \
)
# Asciinema Options
TITLE = "[32m  pearasys demo  "
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
	rm -f demo.cast
	rm -f demo.gif
	rm -f USAGE.md

reset:
	sudo pearasys $(PEARASYS_OPTS) pci device remove rescan

demo.cast:
	GPU=$(GPU) AUD=$(AUD) ./demo.zsh | ASCIINEMA_TITLE=$(TITLE) asciinema rec -i 2 $(ASCIINEMA_OPTS) $@

demo.gif: demo.cast
	agg $(AGG_OPTS) $< $@

demo: demo.cast demo.gif

docs:
USAGE.md:
	typer pearasys utils docs --name pearasys --title "CLI Reference" --output USAGE.md

all: docs demo

.PHONY: clean demo docs all
