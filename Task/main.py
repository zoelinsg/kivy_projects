from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox
from datetime import datetime
from database import Database

db = Database()

class DialogContent(MDBoxLayout):
    """開啟對話框以獲取使用者的任務"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.date_text.text = datetime.now().strftime('%A %d %B %Y')

    def show_date_picker(self):
        """開啟日期選擇器"""
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        date = value.strftime('%A %d %B %Y')
        self.ids.date_text.text = date

class ListItemWithCheckbox(TwoLineAvatarIconListItem):
    """自訂列表項目"""
    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        self.pk = pk

    def mark(self, check, the_list_item):
        """標記任務為完成或未完成"""
        if check.active:
            the_list_item.text = '[s]' + the_list_item.text + '[/s]'
            db.mark_task_as_complete(self.pk)
        else:
            the_list_item.text = db.mark_task_as_incomplete(self.pk)

    def delete_item(self, the_list_item):
        """刪除任務"""
        self.parent.remove_widget(the_list_item)
        db.delete_task(self.pk)

class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    """自訂左側容器"""

class MainApp(MDApp):
    task_list_dialog = None

    def build(self):
        self.theme_cls.primary_palette = "Orange"

    def show_task_dialog(self):
        if not self.task_list_dialog:
            self.task_list_dialog = MDDialog(
                title="Create Task",
                type="custom",
                content_cls=DialogContent(),
            )
        self.task_list_dialog.open()

    def on_start(self):
        """應用程式啟動時載入已保存的任務並添加到 MDList 小部件"""
        try:
            incomplete_tasks, complete_tasks = db.get_tasks()
            for task in incomplete_tasks:
                self.root.ids.container.add_widget(ListItemWithCheckbox(pk=task[0], text=task[1], secondary_text=task[2]))
            for task in complete_tasks:
                item = ListItemWithCheckbox(pk=task[0], text='[s]' + task[1] + '[/s]', secondary_text=task[2])
                item.ids.check.active = True
                self.root.ids.container.add_widget(item)
        except Exception as e:
            print(e)

    def close_dialog(self, *args):
        self.task_list_dialog.dismiss()

    def add_task(self, task, task_date):
        """添加任務到任務列表"""
        created_task = db.create_task(task.text, task_date)
        self.root.ids.container.add_widget(ListItemWithCheckbox(pk=created_task[0], text='[b]' + created_task[1] + '[/b]', secondary_text=created_task[2]))
        task.text = ''

if __name__ == '__main__':
    app = MainApp()
    app.run()