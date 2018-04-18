
PY=python
nad=nad.py
FLAGS=
LIST=
DICT=../dict.json
START=1

.PHONY: default
default: translate-only

.PHONY: translate-only
translate-only:
	$(PY) $(nad) $(FLAGS) -s $(LIST) -d $(DICT)

.PHONY: latex
latex:
	$(PY) $(nad) $(FLAGS) -s $(LIST) -d $(DICT) -l -b $(START) -c

.PHONY: csv
csv:
	$(PY) $(nad) $(FLAGS) -s $(LIST) -d $(DICT) --csv -c

.PHONY: word-mode
word-mode:
	$(PY) $(nad) $(FLAGS) -s $(LIST) -d $(DICT) --word_mode