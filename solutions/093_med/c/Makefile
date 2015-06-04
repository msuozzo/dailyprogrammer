
CC=clang
FLAGS=-Wall -g

SRCDIR=src
OBJDIR=obj
BINDIR=bin

all: $(BINDIR)/z_order

$(OBJDIR):
	mkdir $@

$(SRCDIR):
	mkdir $@

$(BINDIR):
	mkdir $@

$(OBJDIR)/%.o: $(SRCDIR)/%.c | $(OBJDIR)
	$(CC) $(FLAGS) -c -o $@ $<

$(BINDIR)/z_order: $(OBJDIR)/z_order.o | $(BINDIR)
	$(CC) $(FLAGS) -o $@ $^


clean:
	rm -rf $(OBJDIR)/* $(BINDIR)/*

bleach:
	rm -rf $(OBJDIR) $(BINDIR)


