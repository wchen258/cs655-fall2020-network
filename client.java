import java.net.*;
import java.nio.ByteBuffer;
import java.nio.file.*;
import java.io.*;

public class client {
    public static String handle(byte[] image) {
        ByteBuffer bb = ByteBuffer.allocate(4);
        bb.putInt(image.length);
        try (Socket s = new Socket("localhost", 8080)) {
            OutputStream os = s.getOutputStream();
            os.write(bb.array());
            os.write(image);
            os.flush();
            InputStream is = s.getInputStream();
            bb = ByteBuffer.wrap(is.readNBytes(4));
            int length = bb.getInt();
            return new String(is.readNBytes(length));
        } catch (Exception e) {
            e.printStackTrace();
        }
        return "No result.";
    }

    public static void main(String[] args) throws IOException {
        Path path = Paths.get("dog.jpg");
        byte[] data = Files.readAllBytes(path);
        System.out.println(handle(data));
    }
}
