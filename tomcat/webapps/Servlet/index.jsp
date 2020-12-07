<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>Image Recognition</title>
    <script src="https://ajax.aspnetcdn.com/ajax/jQuery/jquery-3.5.1.min.js"></script>
</head>

<style>
    img {
        max-width: 500px;
        height: auto;
    }

    div.polaroid {
        width: 500px;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
        text-align: center;
    }

    div.container {
        padding: 10px;
    }

    .p-a p{ margin-top:30px; margin-bottom:30px}
    .p-b p{ margin-top:60px; margin-bottom:60px}

    input[type=submit] {
        border-radius: 8px;
        position: relative;
        background-color: #E87A90;
        border: none;
        font-size: 15px;
        color: #FFFFFF;
        padding: 10px;
        width: 100px;
        text-align: center;
        -webkit-transition-duration: 0.4s; /* Safari */
        transition-duration: 0.4s;
        text-decoration: none;
        overflow: hidden;
        cursor: pointer;
        animation:myfirst 30s;
        -webkit-animation:myfirst 30s; /* Safari and Chrome */
    }
    @keyframes myfirst
    {
        0%   {background:#E87A90;}
        20%  {background:#C18A26;}
        40%  {background:#89916B;}
        60% {background:#0089A7;}
        80% {background:#77428D;}
        100%   {background:#E87A90;}
    }

    @-webkit-keyframes myfirst /* Safari and Chrome */
    {
        0%   {background:#E87A90;}
        20%  {background:#C18A26;}
        40%  {background:#89916B;}
        60% {background:#0089A7;}
        80% {background:#77428D;}
        100%   {background:#E87A90;}
    }

</style>

<body>

    <div align="center" style="margin-top: 20px;">
        <h3>please select picture:</h3>
        <form action="servlet" method = "post"  enctype="multipart/form-data" >
            <input type="file"
                   id="image" name="image"><br>
            <p>
            </p>
            <input type="submit" value="Submit">
        </form>

        <p>
        </p>
        <div class="polaroid">
            <img src="" id="img0">
            <div class="container">
            </div>
        </div>


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
