<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>Image Recognition</title>
    <script src="https://ajax.aspnetcdn.com/ajax/jQuery/jquery-3.5.1.min.js"></script>
</head>
<body>

    <div align="center" style="margin-top: 50px;">
        <h3>please select picture:</h3>
        <img src="" id="img0" style="width: 20rem;height: 15rem;">
        <form action="servlet" method = "post"  enctype="multipart/form-data" >
            <input type="file"
                   id="image" name="image"><br>
            <input type="submit" value="Submit">
        </form>

        <script type="text/javascript">
            $("#image").change(function(){
                var objUrl = getObjectURL(this.files[0]) ; // get file information
                console.log("objUrl = "+objUrl);
                if (objUrl) {
                    $("#img0").attr("src", objUrl);
                }
            });

            function getObjectURL(file) {
                var url = null;
                if(window.createObjectURL!=undefined) {
                    url = window.createObjectURL(file) ;
                }else if (window.URL!=undefined) { // mozilla(firefox)
                    url = window.URL.createObjectURL(file) ;
                }else if (window.webkitURL!=undefined) { // webkit or chrome
                    url = window.webkitURL.createObjectURL(file) ;
                }
                return url ;
            }
        </script>

    </div>

</body>
</html>
