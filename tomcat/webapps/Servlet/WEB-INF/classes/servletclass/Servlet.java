package servletclass;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import java.io.*;
import java.util.*;
import javax.servlet.ServletException;

import java.net.*;
import java.nio.ByteBuffer;
import java.nio.file.*;

import org.apache.commons.fileupload.FileItem;
import org.apache.commons.fileupload.disk.DiskFileItemFactory;
import org.apache.commons.fileupload.servlet.ServletFileUpload;


public class Servlet extends HttpServlet {

    private boolean isMultipart;
    private String filePath;
    private int maxFileSize = 50 * 1024 * 1024;
    private int maxMemSize = 4 * 1024;
    private File file;

    public void init( ){
        // Get the file location where it would be stored.
        filePath = new File(System.getProperty("user.dir")).getParent() + File.separator + "webapps" + File.separator + "Servlet" + File.separator + "resources";
    }

    @Override
    public void doGet(HttpServletRequest request,
                      HttpServletResponse response) throws IOException,
            ServletException {
        doPost(request, response);
    }

    @Override
    public void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException {
        isMultipart = ServletFileUpload.isMultipartContent(request);
        response.setContentType("text/html");
        PrintWriter out = response.getWriter();

        if( !isMultipart ) {
            request.getRequestDispatcher("error.jsp").forward(request, response);
            return;
        }

        DiskFileItemFactory factory = new DiskFileItemFactory();

        // maximum size that will be stored in memory
        factory.setSizeThreshold(maxMemSize);

        // Location to save data that is larger than maxMemSize.
        factory.setRepository(new File(filePath));

        // Create a new file upload handler
        ServletFileUpload upload = new ServletFileUpload(factory);

        // maximum file size to be uploaded.
        upload.setSizeMax( maxFileSize );

        try {
            // Parse the request to get file items.
            List fileItems = upload.parseRequest(request);

            // Process the uploaded file items
            Iterator i = fileItems.iterator();

            while ( i.hasNext () ) {
                FileItem fi = (FileItem)i.next();
                if ( !fi.isFormField () ) {
                    // Get the uploaded file parameters
                    String fieldName = fi.getFieldName();
                    String fileName = fi.getName();
                    String contentType = fi.getContentType();
                    boolean isInMemory = fi.isInMemory();
                    long sizeInBytes = fi.getSize();

                    // Write the file
                    if( fileName.lastIndexOf("\\") >= 0 ) {
                        file = new File( filePath + File.separator + fileName.substring( fileName.lastIndexOf("\\"))) ;
                    } else {
                        file = new File( filePath + File.separator + fileName.substring(fileName.lastIndexOf("\\")+1)) ;
                    }
                    fi.write( file ) ;
                    byte[] fileContent = Files.readAllBytes(file.toPath());
                    String tag = handle(fileContent);
                    file.delete();
                    if(tag.equals("No result.")) {
                        request.setAttribute("tag", tag);
                        request.setAttribute("confidence", "N/A");
                    }
                    else {
                        String[] strList = tag.split(" ");
                        request.setAttribute("confidence", strList[strList.length - 1]);
                        StringBuilder sb = new StringBuilder();
                        for(int j = 0; j < strList.length - 1; j++) {
                            sb.append(strList[j]);
                            sb.append(" ");
                        }
                        request.setAttribute("tag", sb.toString());
                    }
                    request.getRequestDispatcher("result.jsp").forward(request, response);
                }
            }
        } catch(Exception ex) {
            System.out.println(ex);
        }

    }

    public static String handle(byte[] image) {
        ByteBuffer bb = ByteBuffer.allocate(4);
        bb.putInt(image.length);
        try (Socket s = new Socket("model", 8080)) {
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
}