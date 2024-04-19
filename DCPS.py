import sqlite3
from datetime import datetime


def initialize_db():
  """Initialize the database and create the certificate table if it doesn't exist."""
  conn = sqlite3.connect('dsa_certificates.db')
  c = conn.cursor()
  c.execute('''
        CREATE TABLE IF NOT EXISTS certificates (
            id INTEGER PRIMARY KEY,
            student_name TEXT NOT NULL,
            course TEXT NOT NULL,
            date_issued DATE NOT NULL,
            is_duplicate BOOLEAN DEFAULT FALSE
        )
    ''')
  conn.commit()
  conn.close()


def add_certificate(student_name, course, date_issued):
  """Add a new certificate to the database."""
  try:
    datetime.strptime(date_issued, '%Y-%m-%d')  # Validates date format
    conn = sqlite3.connect('dsa_certificates.db')
    c = conn.cursor()
    c.execute(
        'INSERT INTO certificates (student_name, course, date_issued) VALUES (?, ?, ?)',
        (student_name, course, date_issued))
    conn.commit()
    print("Certificate added successfully!")
  except ValueError:
    print("Error: Date must be in YYYY-MM-DD format.")
  except sqlite3.Error as e:
    print("An error occurred:", e)
  finally:
    conn.close()


def search_certificate(search_query):
  """Search for certificates that match the query."""
  conn = sqlite3.connect('dsa_certificates.db')
  c = conn.cursor()
  query = f"%{search_query}%"
  c.execute(
      'SELECT * FROM certificates WHERE student_name LIKE ? OR course LIKE ?',
      (query, query))
  results = c.fetchall()
  conn.close()
  if results:
    for row in results:
      print(row)
  else:
    print("No matching certificates found.")


def update_certificate(certificate_id, student_name=None, course=None):
  """Update details of an existing certificate."""
  try:
    conn = sqlite3.connect('dsa_certificates.db')
    c = conn.cursor()
    updates = []
    params = []
    if student_name:
      updates.append('student_name = ?')
      params.append(student_name)
    if course:
      updates.append('course = ?')
      params.append(course)
    params.append(certificate_id)
    if updates:
      c.execute(f'UPDATE certificates SET {", ".join(updates)} WHERE id = ?',
                params)
      if c.rowcount == 0:
        print("No such certificate found.")
      else:
        conn.commit()
        print("Certificate updated successfully!")
    else:
      print("No updates provided.")
  except sqlite3.Error as e:
    print("An error occurred:", e)
  finally:
    conn.close()


def delete_certificate(certificate_id):
  """Delete a certificate from the database."""
  conn = sqlite3.connect('dsa_certificates.db')
  c = conn.cursor()
  c.execute('DELETE FROM certificates WHERE id = ?', (certificate_id, ))
  if c.rowcount == 0:
    print("No such certificate found.")
  else:
    conn.commit()
    print("Certificate deleted successfully!")
  conn.close()


def main_menu():
  """Display the main menu and handle user input."""
  actions = {
      '1': ("Add a new certificate", add_certificate),
      '2': ("Search for a certificate", search_certificate),
      '3': ("Update a certificate", update_certificate),
      '4': ("Delete a certificate", delete_certificate),
      '5': ("Exit", exit)
  }

  while True:
    print("\nAvailable actions:")
    for key, (description, _) in actions.items():
      print(f"{key}. {description}")
    choice = input("Select an action: ")
    action = actions.get(choice)

    if action:
      _, func = action
      if func is exit:
        print("Exiting the system.")
        break
      elif func in [add_certificate, update_certificate]:
        student_name = input(
            "Enter student name: ") if 'student' in func.__doc__ else None
        course = input("Enter course: ") if 'course' in func.__doc__ else None
        date_issued = input("Enter date issued (YYYY-MM-DD): "
                            ) if 'date' in func.__doc__ else None
        if func is add_certificate:
          func(student_name, course, date_issued)
        else:
          certificate_id = int(input("Enter certificate ID: "))
          func(certificate_id, student_name, course)
      else:
        query = input("Enter search query or certificate ID: ")
        if query.isdigit():
          func(int(query))
        else:
          func(query)
    else:
      print("Invalid choice. Please try again.")


if __name__ == "__main__":
  initialize_db()
  main_menu()
