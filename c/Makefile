CC = gcc
CFLAGS = -Wall -Wextra -O3
LIBS = -lm
TARGET = prime_partition
SRC = prime_partition.c

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $(TARGET) $(SRC) $(LIBS)

run: $(TARGET)
	./$(TARGET)

clean:
	rm -f $(TARGET)

.PHONY: all run clean
