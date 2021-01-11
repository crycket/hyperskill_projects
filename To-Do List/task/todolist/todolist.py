from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime, timedelta

Base = declarative_base()


class TaskTable(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


class Interface:
    def __init__(self):
        self.engine = create_engine('sqlite:///todo.db?check_same_thread=False')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self._start_session()
        self.today = datetime.today().date()

    def _start_session(self) -> Session:
        return self.Session()

    @staticmethod
    def menu():
        return "1) Today's tasks\n" \
               "2) Week's tasks\n" \
               "3) All tasks\n" \
               "4) Missed tasks\n" \
               "5) Add task\n" \
               "6) Delete task\n" \
               "0) Exit\n"

    def today_tasks(self):
        print(f'Today {self.today.strftime("%d %b")}:')
        tasks = self.session.query(TaskTable).filter(TaskTable.deadline == self.today).all()
        if not tasks:
            print('Nothing to do!')
            return
        for i, task in enumerate(tasks, start=1):
            print(f'{i}. {task}')

    def week_tasks(self):
        week_later = self.today + timedelta(days=7)
        tasks = self.session.query(TaskTable).\
            filter((TaskTable.deadline >= self.today) & (TaskTable.deadline < week_later)).\
            order_by(TaskTable.deadline).all()
        for day in range(7):
            index = 1
            date = self.today + timedelta(days=day)
            print(f'{date.strftime("%A %d %b")}:')
            for task in tasks:
                if task.deadline == date:
                    print(f'{index}. {task}\n')
                    index += 1
            if index == 1:
                print('Nothing to do!\n')

    def all_tasks(self):
        print('All tasks:')
        rows = self.session.query(TaskTable).order_by(TaskTable.deadline).all()
        for i, row in enumerate(rows, start=1):
            print(f'{i}. {row}. {row.deadline.day} {row.deadline.strftime("%b")}')

    def missed_tasks(self):
        rows = self.session.query(TaskTable).\
            filter(TaskTable.deadline < self.today).\
            order_by(TaskTable.deadline).all()
        print('Missed tasks:')
        for i, row in enumerate(rows):
            print(f'{i}. {row}. {row.deadline.day} {row.deadline.strftime("%b")}')

    def add_task(self):
        task = input('Enter task\n')
        deadline = input('Enter deadline\n')
        new_task = TaskTable(task=task, deadline=datetime.strptime(deadline, '%Y-%m-%d').date())
        self.session.add(new_task)
        self.session.commit()
        print('The task has been added!')

    def delete_task(self):
        print('Choose the number of the task you want to delete:')
        rows = self.session.query(TaskTable).order_by(TaskTable.deadline).all()
        for i, row in enumerate(rows, start=1):
            print(f'{i}. {row}. {row.deadline.day} {row.deadline.strftime("%b")}')
        _user_input = int(input()) - 1
        self.session.delete(rows[_user_input])
        self.session.commit()
        print('The task has been deleted!')


user_interface = Interface()
while True:
    user_input = input(Interface.menu())
    if user_input == '1':
        user_interface.today_tasks()
    elif user_input == '2':
        user_interface.week_tasks()
    elif user_input == '3':
        user_interface.all_tasks()
    elif user_input == '4':
        user_interface.missed_tasks()
    elif user_input == '5':
        user_interface.add_task()
    elif user_input == '6':
        user_interface.delete_task()
    elif user_input == '0':
        print('Bye!')
        break
    print()
