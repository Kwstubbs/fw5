import java.io.IOException;
import java.io.OutputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.security.MessageDigest;
import java.util.Random;

/**
 * Very simple random-based fuzzer for warmup/target.py.
 * Generates random byte inputs, pipes them into "python3.11 target.py" via stdin,
 * and saves any input that makes the process crash (non-zero exit code) to crashes/.
 */
public class Fuzzer {
    private static final int MAX_LEN = 64;
    private static final int ITERATIONS = 10;

    public static void main(String[] args) throws Exception {
        Random random = new Random();
        Path crashesDir = Paths.get("crashes");
        Files.createDirectories(crashesDir);

        for (int i = 0; i < ITERATIONS; i++) {
            byte[] input = randomInput(random);

            int exitCode = runTarget(input);

            if (exitCode != 0) {
                saveCrash(crashesDir, input);
                System.out.printf("Iteration %d: CRASH found (exit=%d), input=%s%n",
                        i, exitCode, bytesToDisplay(input));
            }
        }

        System.out.println("Done fuzzing.");
    }

    private static byte[] randomInput(Random random) {
        int len = random.nextInt(MAX_LEN + 1);
        byte[] data = new byte[len];

        if (random.nextBoolean()) {
            // Bias towards key=value shaped input, since that's what the target expects.
            String key = randomAscii(random, random.nextInt(8));
            String value = randomAscii(random, random.nextInt(8));
            String combined = key + "=" + value;
            data = combined.getBytes();
            if (data.length > MAX_LEN) {
                byte[] truncated = new byte[MAX_LEN];
                System.arraycopy(data, 0, truncated, 0, MAX_LEN);
                data = truncated;
            }
        } else {
            // Fully random bytes.
            random.nextBytes(data);
        }

        return data;
    }

    private static String randomAscii(Random random, int len) {
        StringBuilder sb = new StringBuilder(len);
        for (int i = 0; i < len; i++) {
            sb.append((char) (32 + random.nextInt(95))); // printable ASCII range
        }
        return sb.toString();
    }

    private static int runTarget(byte[] input) throws IOException, InterruptedException {
        ProcessBuilder pb = new ProcessBuilder("python3.11", "target.py");
        pb.redirectErrorStream(true);
        pb.redirectOutput(ProcessBuilder.Redirect.DISCARD);
        Process process = pb.start();

        try (OutputStream stdin = process.getOutputStream()) {
            stdin.write(input);
        } catch (IOException e) {
            // Target may close stdin early; ignore broken pipe.
        }

        return process.waitFor();
    }

    private static void saveCrash(Path crashesDir, byte[] input) throws Exception {
        String hash = sha1Hex(input);
        Path file = crashesDir.resolve("crash-" + hash + ".bin");
        Files.write(file, input);
    }

    private static String sha1Hex(byte[] data) throws Exception {
        MessageDigest digest = MessageDigest.getInstance("SHA-1");
        byte[] hash = digest.digest(data);
        StringBuilder sb = new StringBuilder();
        for (byte b : hash) {
            sb.append(String.format("%02x", b));
        }
        return sb.toString();
    }

    private static String bytesToDisplay(byte[] data) {
        StringBuilder sb = new StringBuilder();
        for (byte b : data) {
            int c = b & 0xFF;
            if (c >= 32 && c < 127) {
                sb.append((char) c);
            } else {
                sb.append(String.format("\\x%02x", c));
            }
        }
        return sb.toString();
    }
}
