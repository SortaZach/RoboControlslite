#include <avr/io.h>
#include <util/delay.h>

#define LED_PIN PD5 // Pin 05 on Arduino Uno

int main() {

    DDRB |= (1 << LED_PIN); // Set LED pin as output

    while (1) {
        PORTB ^= (1 << LED_PIN); // Toggle LED
        _delay_ms(500);          // Wait 500ms
    }
}