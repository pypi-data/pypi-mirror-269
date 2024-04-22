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
