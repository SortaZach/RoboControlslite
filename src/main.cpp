#include <avr/io.h>
#include <util/delay.h>

// PORTB is Digital Pins 8-13
// PORTC is Analog Pins A0-A5
// PORTD is Digital Pins 0-6
#define LED_PIN PD5 // Pin 05 on Arduino Uno

void setupPWM();
void setBrightness(uint8_t brightness);

int main() {
    setupPWM(); // Initialize PWM
    
    while (1) {
        for(uint8_t i = 0; i < 255; i++) {
            setBrightness(i); // Increase brightness
            _delay_ms(10);
        }

        for(uint8_t i = 255; i > 0; i--) {
            setBrightness(i);
            _delay_ms(10);
        }
    }
}


// Timer function to have a smooth transition for blinking of a LED
void setupPWM(){

    // Set LED pin as output (|= is setting a bit of memory in this case bit 5 for PD5 of arduino board)
    // DDRD (Data Direction Register D) controls whether pins in PORTD are inputs or outputs
    DDRD |= (1 << LED_PIN);
    
    // Example of seting a pin as an input:
    // DDRD |= ~(1 << LED_PIN);

    // TCCR0A (Timer/Counter Control Register 0A) a register that contfigures Timer0
    // TCCR0A has 8 bits, each controlling ifferent timer settings:
    // Bit 7: COM0A1 (Compare Match Output A)
    // Bit 6: COM0A0 (Compare Match Output A)
    // Bit 5: COM0B1 (example: Enables PWM on OC0B(Output Compare 0(belongs to Timer0) B(second compare register, first would be OC0A)))
    // Bit 4: COM0B0 (Compare Match Output B)
    // Bit 3: WGM02  (Waveform Generation Mode Bit 2)
    // Bit 2: WGM01  (Waveform Generation Mode Bit 1 (fast PWM Mode Select))
    // Bit 1: WGM00  (Waveform Generation Mode Bit 0 (fast PWM mode Select))
    // Bit 0: unused

    // TCCR0B
    // Bit 7: FOC0A	Force Output Compare A (used in non-PWM mode) forces immediate compare match    
    // Bit 6: FOC0B	Force Output Compare B (used in non-PWM mode)
    // Bit 5: -	(Unused)
    // Bit 4: - (Unused)
    // Bit 3: WGM02	Waveform Generation Mode Bit 2 (controls PWM mode)
    // Bit 2: CS02 Clock Select Bit 2 (prescaler setting) These three(bit 0, 1, 2) are used in conjunction to make the prescaler setting
    // Bit 1: CS01 Clock Select Bit 1 (prescaler setting) Basically these set timer speeds
    // Bit 0: CS00 Clock Select Bit 0 (prescaler setting)


    // Configure the Timer0 for Fast PMW mode (Pulse Width Modulation)
    TCCR0A |= (1 << COM0B1); // Clear OC0B on Compare Match, set at BOTTOM
    TCCR0A |= (1 << WGM00) | (1 << WGM01); // fast PWM Mode
    TCCR0B |= (1 << CS01);  // Set prescaler to 8 (PMW frequency = 976 Hz)
}

void setBrightness(uint8_t brightness) {
    // Output Compare Register for pin 5 (0B)
    OCR0B = brightness; // Set duty cycle (0-255)
}
