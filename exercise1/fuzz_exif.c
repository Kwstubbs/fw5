#include <stdint.h>
#include <stdlib.h>
#include <string.h>

int process_EXIF(unsigned char *ExifSection, int length);

int ShowTags = 0;
int DumpExifMap = 0;
int SupressNonFatalErrors = 1;

/* jhead.c owns main(), so it is left out of the build and the few globals it
   would have provided are stubbed here. */
void ErrNonfatal(const char *msg, int a1, int a2) { (void)msg; (void)a1; (void)a2; }
void ErrFatal(const char *msg) { (void)msg; abort(); }
void FileTimeAsString(char *TimeStr) { TimeStr[0] = 0; }

int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {
    if (Size < 16 || Size > 65536) return 0;

    /* Copy to an exact-sized heap block so reads past the end are real
       out-of-bounds reads rather than reads into the fuzzer's own buffer. */
    unsigned char *buf = malloc(Size);
    memcpy(buf, Data, Size);
    process_EXIF(buf, (int)Size);
    free(buf);
    return 0;
}
