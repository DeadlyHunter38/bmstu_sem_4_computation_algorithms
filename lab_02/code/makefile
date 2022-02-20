APPDIR := ./src/
LIBDIR := ./inc/
OUTDIR := ./out/

CC := gcc
CFLAGS := -std=c99 -Wall -Werror -pedantic -c

all: main.exe

main.exe: $(OUTDIR)main.o $(OUTDIR)read.o $(OUTDIR)process_matrix.o $(OUTDIR)multiply_interpolation.o
		$(CC) -o $@ $^

$(OUTDIR)main.o: $(APPDIR)main.c $(LIBDIR)defines.h $(LIBDIR)struct.h $(LIBDIR)read.h $(LIBDIR)process_matrix.h\
				 $(LIBDIR)multiply_interpolation.h
		$(CC) $(CFLAGS) $< -o $@

$(OUTDIR)read.o: $(APPDIR)read.c $(LIBDIR)defines.h $(LIBDIR)struct.h $(LIBDIR)read.h $(LIBDIR)process_matrix.h
		$(CC) $(CFLAGS) $< -o $@

$(OUTDIR)process_matrix.o: $(APPDIR)process_matrix.c $(LIBDIR)process_matrix.h $(LIBDIR)struct.h
		$(CC) $(CFLAGS) $< -o $@

$(OUTDIR)multiply_interpolation.o: $(APPDIR)multiply_interpolation.c $(LIBDIR)multiply_interpolation.h\
									$(LIBDIR)defines.h $(LIBDIR)struct.h
		$(CC) $(CFLAGS) $< -o $@

.PHONY: clean
clean:
		rm -rf $(OUTDIR)*.o *.exe