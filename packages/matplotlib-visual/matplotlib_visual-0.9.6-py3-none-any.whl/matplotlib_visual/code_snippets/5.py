# app.py
from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


# Function to create a SQLite database and table for indexing
def create_index_db():
  conn = sqlite3.connect('search_index.db')
  c = conn.cursor()
  c.execute('''CREATE TABLE IF NOT EXISTS documents
                 (id INTEGER PRIMARY KEY, title TEXT, content TEXT)''')
  conn.commit()
  conn.close()


# Function to index a document
def index_document(title, content):
  conn = sqlite3.connect('search_index.db')
  c = conn.cursor()
  c.execute("INSERT INTO documents (title, content) VALUES (?, ?)",
            (title, content))
  conn.commit()
  conn.close()


# Function to search indexed documents
def search(query):
  conn = sqlite3.connect('search_index.db')
  c = conn.cursor()
  c.execute("SELECT * FROM documents WHERE content LIKE ? OR title LIKE ?",
            ('%' + query + '%', '%' + query + '%'))
  results = c.fetchall()
  conn.close()
  return results


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/search', methods=['POST'])
def do_search():
  query = request.form.get('query')
  results = search(query)
  return render_template('index.html', results=results)


if __name__ == '__main__':
  create_index_db()
  app.run(debug=True)

#db.py
import sqlite3


def create_index_db():
  conn = sqlite3.connect('search_index.db')
  c = conn.cursor()
  c.execute('''CREATE TABLE IF NOT EXISTS documents
(id INTEGER PRIMARY KEY, title TEXT, content TEXT)''')
  conn.commit()
  conn.close()


def index_document(title, content):
  conn = sqlite3.connect('search_index.db')
  c = conn.cursor()
  c.execute("INSERT INTO documents (title, content) VALUES (?, ?)",
            (title, content))
  conn.commit()
  conn.close()


def search(query):
  conn = sqlite3.connect('search_index.db')
  c = conn.cursor()
  c.execute("SELECT * FROM documents WHERE content LIKE ? OR title LIKE ?",
            ('%' + query + '%', '%' + query + '%'))
  results = c.fetchall()
  conn.close()
  return results


def display_results(results):
  if not results:
    print("No results found.")
  else:
    for result in results:
      print("Title:", result[1])
      print("Content:", result[2])
      print()


def main():
  create_index_db()
  index_document("Document 1", "This is the content of document 1.")
  index_document("Document 2", "This is the content of document 2.")
  index_document("Document 3", "Content of document 3.")
  index_document("Document 4", "Content of document 4.")


def index_document(title, content):
  try:
    conn = sqlite3.connect('search_index.db')
    c = conn.cursor()
    c.execute("INSERT INTO documents (title, content) VALUES (?, ?)",
              (title, content))
    conn.commit()
    conn.close()
    print("Document indexed successfully!")
  except Exception as e:
    print("Error indexing document:", e)


if __name__ == "__main__":
  main()

#html
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

