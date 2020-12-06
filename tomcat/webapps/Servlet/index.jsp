<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>Image Recognition</title>
</head>
<body>

    <div align="center" style="margin-top: 50px;">

        <form action="servlet">
            Please enter your Username:  <input type="text" name="username" size="20px"> <br>
            Please enter your Password:  <input type="text" name="password" size="20px"> <br><br>
            <input type="file"
                   id="image" name="image"
                   accept="image/png, image/jpeg">
            <input type="submit" value="submit">
        </form>

    </div>

</body>
</html>
