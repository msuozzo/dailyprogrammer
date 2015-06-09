
CC=clang++
FLAGS=-Wall -g -std=c++14

SRCDIR=src
OBJDIR=obj
BINDIR=bin

all: $(BINDIR)/lines

$(OBJDIR):
	mkdir $@

$(SRCDIR):
	mkdir $@

$(BINDIR):
	mkdir $@

$(OBJDIR)/%.o: $(SRCDIR)/%.cpp | $(OBJDIR)
	$(CC) $(FLAGS) -c -o $@ $<

$(BINDIR)/lines: $(OBJDIR)/lines.o | $(BINDIR)
	$(CC) $(FLAGS) -o $@ $^


clean:
	rm -rf $(OBJDIR)/* $(BINDIR)/*

bleach:
	rm -rf $(OBJDIR) $(BINDIR)
