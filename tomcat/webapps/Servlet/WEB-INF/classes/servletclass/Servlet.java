package servletclass;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;

public class Servlet extends HttpServlet {
    public void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException {
        response.setContentType("text/html");

        PrintWriter writer = response.getWriter();

        writer.println("<!DOCTYPE> <html><head><title> Welcome Servlet</title></head>");
        writer.println("<body><h3>Welcome to the world of Servlet! </h3></body>");
    }
}