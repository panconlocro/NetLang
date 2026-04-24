FILENAME = grammar/NetLang.g4
PREFIX = $(basename $(FILENAME))

all:
	java -jar /usr/local/lib/antlr-4.13.1-complete.jar -Dlanguage=Python3 -visitor $(FILENAME)

clean:
	rm -f $(PREFIX)*.py $(PREFIX)*.tokens $(PREFIX)*.interp
