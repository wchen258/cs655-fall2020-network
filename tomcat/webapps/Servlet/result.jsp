<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>Image Recognition</title>
</head>
<style>

    .button {
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
    <p>tag: ${tag}</p>
    <p>confidence: ${confidence}</p>
    <a href="/Servlet">
        <button class="button">Retrun</button>
    </a>
</div>
</body>
</html>