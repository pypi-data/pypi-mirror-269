<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple Search Engine</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            flex-direction: column;
        }
        h1 {
            margin-bottom: 20px;
            color: #333;
        }
        form {
            display: flex;
            align-items: center;
        }
        input[type="text"] {
            padding: 10px;
            font-size: 16px;
            border: 2px solid #ccc;
            border-radius: 5px;
            margin-right: 10px;
            width: 300px;
        }
        button[type="submit"] {
            padding: 10px 20px;
            font-size: 16px;
            background-color: #4caf50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        button[type="submit"]:hover {
            background-color: #45a049;
        }
        h2 {
            margin-top: 20px;
            color: #333;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        li {
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <h1>Simple Search Engine</h1>
    <form action="/search" method="post">
        <input type="text" name="query" placeholder="Enter your search query">
        <button type="submit">Search</button>
    </form>
    {% if results %}
        <h2>Search Results</h2>
        <ul>
            {% for result in results %}
                <li>Title: {{ result[1] }}</li>
                <li>Content: {{ result[2] }}</li>
            {% endfor %}
        </ul>
    {% endif %}
</body>
</html>

