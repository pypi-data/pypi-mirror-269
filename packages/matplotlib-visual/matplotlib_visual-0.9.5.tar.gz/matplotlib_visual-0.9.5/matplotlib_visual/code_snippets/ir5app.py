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
