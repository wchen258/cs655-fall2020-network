<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>Image Recognition</title>
</head>
<body>

    <div align="center" style="margin-top: 50px;">

        <form action="servlet" method = "post"  enctype="multipart/form-data">
            <input type="file"
                   id="image" name="image">
            <input type="submit" value="submit">
        </form>

    </div>

</body>
</html>
