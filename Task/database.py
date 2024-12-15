import sqlite3

class Database:
    def __init__(self):
        self.con = sqlite3.connect('todo.db')
        self.cursor = self.con.cursor()
        self.create_task_table()

    # 建立 Tasks 表格
    def create_task_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task VARCHAR(50) NOT NULL,
                due_date VARCHAR(50),
                completed BOOLEAN NOT NULL CHECK (completed IN (0, 1))
            )
        """)

    # 建立任務
    def create_task(self, task, due_date=None):
        self.cursor.execute("INSERT INTO tasks(task, due_date, completed) VALUES(?, ?, ?)", (task, due_date, 0))
        self.con.commit()
        created_task = self.cursor.execute("SELECT id, task, due_date FROM tasks WHERE task = ? AND completed = 0", (task,)).fetchone()
        return created_task

    # 取得任務
    def get_tasks(self):
        complete_tasks = self.cursor.execute("SELECT id, task, due_date FROM tasks WHERE completed = 1").fetchall()
        incomplete_tasks = self.cursor.execute("SELECT id, task, due_date FROM tasks WHERE completed = 0").fetchall()
        return incomplete_tasks, complete_tasks

    # 更新任務狀態為完成
    def mark_task_as_complete(self, taskid):
        self.cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (taskid,))
        self.con.commit()

    # 更新任務狀態為未完成
    def mark_task_as_incomplete(self, taskid):
        self.cursor.execute("UPDATE tasks SET completed = 0 WHERE id = ?", (taskid,))
        self.con.commit()
        task_text = self.cursor.execute("SELECT task FROM tasks WHERE id = ?", (taskid,)).fetchone()
        return task_text[0]

    # 刪除任務
    def delete_task(self, taskid):
        self.cursor.execute("DELETE FROM tasks WHERE id = ?", (taskid,))
        self.con.commit()

    # 關閉資料庫連線
    def close_db_connection(self):
        self.con.close()