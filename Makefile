
CLEAN_LIST = build Dict.spec

default: all

all:
	pyinstaller Dict.py -F --clean

release: all clean

clean:
	rm -rf $(CLEAN_LIST)

cleanall: clean
	rm -rf dist