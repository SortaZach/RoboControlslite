MCU = atmega328p
F_CPU = 16000000UL
BAUD = 115200
PORT = COM3

CC = avr-gcc
OBJCOPY = avr-objcopy
AVRDUDE = avrdude

CFLAGS = -mmcu=$(MCU) -DF_CPU=$(F_CPU) -Os
TARGET = main
SRC_DIR = src
OBJ_DIR = obj

# Ensure obj directory exists (Windows compatible)
ifeq ($(OS),Windows_NT)
    SHELL = cmd
    MKDIR = if not exist $(OBJ_DIR) mkdir $(OBJ_DIR)
else
    SHELL = /bin/sh
    MKDIR = mkdir -p $(OBJ_DIR)
endif

# Create obj directory
$(shell $(MKDIR))

all: $(TARGET).hex

# Compile the C++ file into an object file
$(OBJ_DIR)/$(TARGET).o: $(SRC_DIR)/$(TARGET).cpp
	$(CC) $(CFLAGS) -c -o $@ $<

# Convert object file to ELF executablea
$(TARGET).elf: $(OBJ_DIR)/$(TARGET).o
	$(CC) $(CFLAGS) -o $@ $^

# Convert ELF to HEX file (fix incorrect OBJCOPY syntax)
$(TARGET).hex: $(TARGET).elf
	$(OBJCOPY) -O ihex $< $(TARGET).hex

# Upload to Arduino
flash: $(TARGET).hex
	$(AVRDUDE) -c arduino -p $(MCU) -P $(PORT) -b $(BAUD) -U flash:w:$(TARGET).hex:i

# Clean up build files
clean:
	rm -f $(OBJ_DIR)/*.o $(TARGET).hex $(TARGET).elf

run:
	python .\GUI\main.py