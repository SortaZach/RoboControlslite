#include <avr/io.h>
#include <util/delay.h>
#include <stdlib.h> // for itoa() conversion

#define JOYSTICK_X PC2
#define JOYSTICK_Y PC1
#define JOYSTICK_PRESSED PB3 // Pin 11

#define U1_TRIG_PIN PB1 // Pin 9
#define U1_ECHO_PIN PB2 // Pin 10 

// Pin 2 and 3 are special because these are the only two
// that are dedicated external interrupts, we would have to use a 
// Pin change interrupt otherwise which isn't as fast
#define ROTARY_DIAL_CLK PD2 // Pin 2 
#define ROTARY_DIAL_DT PD3 // Pin 3
#define ROTARY_DIAL_SW PD4 // Pin 4

// for buttons we can add a 0.1uf capcaitor to help debounce it if we're experence button bouncing (triggering multiple times)
// we can also fix this in the code though using a _delay_ms(20) so it will create a small delay between button presses.
#define BUTTON_1 PB5

void setupADC();
uint16_t readADC(uint8_t channel);
void setupUltrasonic();
void setupEncoder();
volatile int encoder_value;

uint16_t getDistance();
void setupUART();
void uartTransmit(char data);
void uartPrint(const char *str);
void parseToJSON(uint16_t joyX1, uint16_t joyY1, uint8_t joySW1, uint8_t b1, uint16_t u1);

int main(){

    setupADC();
    setupUltrasonic();
    setupUART();
    setupEncoder();

    while(1) {
        uint16_t xValue = readADC(JOYSTICK_X); 
        uint16_t yValue = readADC(JOYSTICK_Y);
        uint8_t swValue = 0; // false or not pressed
        uint8_t b1Value = 0;
        uint16_t u1 = 0;
        uint8_t

        uint16_t u1Value = getDistance(); // Get ultrasonic sensor reading
        // turn on the Input for pressed use & for pointer otherwise we overwrite the entire DDRD register instead of just where the pin is
        DDRD &= ~(1 << JOYSTICK_PRESSED);
        PORTD |= (1 << JOYSTICK_PRESSED);
        
        DDRD &= ~(1 << BUTTON_1);
        PORTD |= (1 << BUTTON_1);
        // Check if Joystick is pressed (LOW = Pressed)
        // PIND  is a hardware register for AVR that stores the current state of all digital input pins on PORT D
        // the & symbol is a bitwise and, meaning we can point to specific registers
        if(!(PIND & (1 << JOYSTICK_PRESSED))){
            swValue = 1;
        }

        if(!(PIND & (1 << BUTTON_1))){
            b1Value = 1;
        }
        
        parseToJSON(xValue, yValue, swValue, b1Value, u1Value);
        _delay_ms(500); // Delay for readablity
    }
}

// Analog to Digital Conversion (ADC)
void setupADC(){
    // ADMUX (ADC Multiplexer Selection Register: configuration register)
        // selects reference voltage
        // input channel
        // how ADC results are stored
    ADMUX |= (1 << REFS0); // Use AVCC (5V) as reference voltage (Ensures ADC reads between 0V and 5V)(REFS0/REFS1 controllers reference Voltage)
                           // setting REFS0 makes 0v = 0 and 5V = 1023 in ADC readings

    // ADCSRA (ADC Control and Status Register A)
        // ADC enable/disable
        // ADC start conversion
        // ADC clock prescaler
        // ADC interrupt settings
    ADCSRA |= (1 << ADEN); // Enable ADC (ADEN: bit 7 of ADCSRA, enables ADC if 1)
    ADCSRA |= (1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0); // set prescaler to 128 (16 Mhz / 128 = 125khz ADC clock)
}

uint16_t readADC(uint8_t channel){
    ADMUX = (ADMUX & 0xF8) | channel; // Select ADC channel (A0 or A1 in this setup)
    ADCSRA |= (1 << ADSC); // Start conversion
    while (ADCSRA & (1 << ADSC)); // Wait for conversion to complete
    return ADC; // Return 10-bit ADC value (0-1023)
}

void setupUltrasonic(){
    DDRB &= ~(1 << U1_ECHO_PIN); // input
    DDRB |= (1 << U1_TRIG_PIN); // output
}

void setupEncoder(){
    DDRD &= ~(1 << ROTARY_DIAL_CLK | 1 << ROTARY_DIAL_DT | 1 << ROTARY_DIAL_SW);
    _delay_us(2);
    // Enable the INT0 and INT1 for encoder (special interupts for the PD2 PD3)
    // We're using the External Interupt Control Register A (EICRA) which configures
    // when the INT0 and INT1 should trigger an interrupt
    // Each interrupt has two bits that define its trigger condition that are mapped to ISCx1 and ISCx0
    EICRA |= (1 << ISC00) | (1 << ISC10);
    _delay_us(2);
    // The External Interrupt Mask Register (EIMSK) enables specific external interrupts
    EIMSK |= (1 << INT0) | (1 << INT1);
    _delay_us(2);
    sei(); // needed to enable global interrupts (set enable interupts (sei))
} 

ISR(INT0_vect){
    if(PIND & (1 << ROTARY_DIAL_CLK)){
        encoder_value++;
    } else {
        encoder_value--;
    }
}

// the ISR Triggers when PD2 changes
ISR(INT1_vect){
    if(PIND & (1 << ROTARY_DIAL_DT)){
        encoder_value++;
    } else {
        encoder_value--;
    }
}


uint16_t getDistance(){
    PORTB &= ~(1 << U1_TRIG_PIN);
    _delay_us(2);
    PORTB |= (1 << U1_TRIG_PIN);
    _delay_us(10); // 10 microseconds, this is used to measure.
    PORTB &= ~(1 << U1_TRIG_PIN);
    // Measure how long ECHO is HIGH
    TCNT1 = 0; // TCNT1 is a timer that we're using and resetting here
    uint16_t timeout = 30000;
    while(!(PINB & (1 << U1_ECHO_PIN))){
        if (--timeout == 0){ return 9999;}
    }; // Wait for HIGH signal
    
    timeout = 30000; // reset timeout
    while(PINB & (1 << U1_ECHO_PIN)) {
        if(--timeout == 0){ return 9999;}
        TCNT1++;
        _delay_us(1); 
    }
    // Convert time to distance (in cm)
    return TCNT1 / 58; // Formula is ** Distance (cm) = Duration (us) / 58 **
}



void parseToJSON(uint16_t joyX1, uint16_t joyY1, uint8_t joySW1, uint8_t b1, uint16_t u1){
    char buffer[10];
    //Indenting to indicate JSON Formatting
    uartPrint("{\"input\":{");
        uartPrint("\"js1\":{");
            uartPrint("\"X\":"); itoa(joyX1, buffer, 10); uartPrint(buffer); uartPrint(",");
            uartPrint("\"Y\":"); itoa(joyY1, buffer, 10); uartPrint(buffer); uartPrint(",");
            uartPrint("\"SW\":"); itoa(joySW1, buffer, 10); uartPrint(buffer); 
        uartPrint("},");
        uartPrint("\"buttons\":{");
            uartPrint("\"b1\":"); itoa(b1, buffer, 10); uartPrint(buffer);
        uartPrint("}");
        uartPrint("\"dials\":{");
            uartPrint("\"d1\":"); itoa(d1, buffer, 10); uartPrint(buffer);
        uartPrint("}");
    uartPrint("},");
    uartPrint("\"outputs\":{");
        uartPrint("\"u1\":"); itoa(u1, buffer, 10); uartPrint(buffer);
    uartPrint("}}");

    // always end a json or a print seciton with a \n
    uartPrint("\n");
}

// Universal Asyncronous Reciver-Transmitter communication (currently can use the serial monitor in the Arduino IDE)
void setupUART() {
    UBRR0H = 0;   // UBRR0H is high byte of UART bit regist (16-bit so two registers)
    UBRR0L = 103; // 9600 baud rate for 16MHz clock (low byte, second half of 16-bit register)
    UCSR0B |= (1 << TXEN0); // Enable UART transmitter (UCSR0B is 3 bits, TXEN0 is the bit that enables it)
                            // This activates the TX pin allowing data transmission

    UCSR0C |= (1 << UCSZ01) | (1 << UCSZ00); // 8-bit data format(UCSR0C configures UART Data format. setting it as 8 bit is default or standard)
}

void uartTransmit(char data) {
    while (!(UCSR0A & (1 << UDRE0))); // Wait for buffer to be empty (UDREO is USART Data Register Empty flag)
    UDR0 = data; // send data (this is the Data Register)
} 

void uartPrint(const char *str) {
    while(*str){
        uartTransmit(*str++);
    }
}