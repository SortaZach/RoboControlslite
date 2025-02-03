#include <avr/io.h>
#include <avr/delay.h>
#include <stdlib.h> // For atoi() conversion

void setupUART();
char uartReceive();
void uartPrint(const char *str);

int main(){
    setupUART();

    char buffer[64]; // buffer for received message
    uint8_t index = 0;

    while (1) {
        char received = uartReceive();

        if(received == '\n') { // newLine marks end of message
            buffer[index] = '\0'; // null-terminate the string

            // print received data
            uartPrint("Received: ");
            uartPrint(buffer);
            uartPrint("\n");

            index = 0; // reset the buffer for next message
        } else {
            buffer[index++] = received; // store characters in buffer
            if (index >= 63) index = 0; // prevent buffer overflow
         }
    }
}

// Setup UART for receiving Data
void setupUART() {
    UBRR0H = 0;
    UBRR0L = 103;
    UCSR0B |= (1 << RXEN0); // Enable UART reciever
    UCSR0C |= (1 << UCSZ01 | UCSZ00); // Set 8-bit data format
}

char uartReceive() {
    while (!(UCSR0A & (1 << RXC0))); // wait till data is received
    return UDR0; // Return recieved byte
}

void uartPrint(const char *str) {
    while (*str) {
        while (!(UCSR0A & (1 << UDRE0)));
        UDR0 = *str++;
    }
}