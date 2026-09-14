import java.io.StringReader;

public class fuzzer {
    
    // Jazzer expects a public static method named fuzzerTestOneInput
    public static void fuzzerTestOneInput(byte[] data) {
    
        // Convert the input byte array into the appropriate format for parsing
        
        try {
        // Let's fuzz parseBooking API!
          BookingForm.parseBooking();
          
        } catch (IllegalArgumentException ignored) {
        }
    }
}

