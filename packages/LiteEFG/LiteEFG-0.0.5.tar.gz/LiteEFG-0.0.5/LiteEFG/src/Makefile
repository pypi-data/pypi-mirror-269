# Define compiler
CC=g++

# Include directory
OBJDIR := build
INCLUDE_DIR := $(shell pwd)
PYBIND11_INCLUDES := $(shell python3 -m pybind11 --includes)
PYBIND11_SUFFIX := $(shell python3-config --extension-suffix)

# Source files
SOURCES := $(shell find . -name '*.cpp' ! -path "./libef/*")
HEADERS := $(shell find . -name '*.h' ! -path "./libef/*")

# Object files
OBJECTS := $(SOURCES:.cpp=.o)
#OBJECTS:=$(foreach obj,$(OBJECTS),$(OBJDIR)/$(notdir $(obj)))

# Executable name
EXECUTABLE := LiteEFG

# Compiler flags, add include directory
CFLAGS := -g -std=c++23 -I$(INCLUDE_DIR)

# The first rule is the one executed when no target is specified.
all: $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS) $(HEADERS)
	$(CC) $(CFLAGS) -o $@ $^

%.o: %.cpp
	$(CC) $(CFLAGS) -c $< -o $@

# Clean rule
clean:
	rm -f $(OBJECTS) $(EXECUTABLE)

# Other rules and dependencies can go here
