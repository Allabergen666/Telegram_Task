import sqlite3 

class Task:
    def __init__(self, title, description, status):
        self.title = title
        self.description = description
        self.status = status

    def save(self):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO tasks (title, description, status) VALUES (?, ?, ?)",
                  (self.title, self.description, self.status))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM tasks")
        rows = c.fetchall()
        conn.close()

        tasks = []
        for row in rows:
            task = Task(row[1], row[2], row[3])
            tasks.append(task)

        return tasks

    @staticmethod
    def mark_as_done(task_id):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("UPDATE tasks SET status='выполнена' WHERE id=?", (task_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(task_id):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
        conn.close()