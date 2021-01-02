import json, time, os, subprocess
from colors import *

class Todo(object):
    def __init__(self):
        os.chdir('./todo-cli')
        with open('./todolist.json', 'r') as f:
            self.todo_list = json.load(f)
        self.done_tasks = 0

    def save_list(self):
        with open('./todolist.json', 'w') as f:
            json.dump(self.todo_list, f, indent=4)

    def remove_impt_task(self, index:int):
        if index < 0:
            raise Exception('It should be within the range of your todo list count')
        
        index -= 1

        finished_task = self.todo_list['urgent'].pop(index)
        self.done_tasks += 1
        return finished_task

    def remove_task(self, index:int):
        if index < 0:
            raise Exception('It should be within the range of your todo list count')

        index -= 1

        finished_task = self.todo_list['nonurgent'].pop(index)
        self.done_tasks += 1
        return finished_task

    def add_new_impt_task(self, task:str):
        self.todo_list['urgent'].append(task)
        return task

    def add_new_task(self, task:str):
        self.todo_list['nonurgent'].append(task)
        return task

    def show_all_tasks(self):
        impt = f'{c_bold}{fg_red}\ue0b6{c_end}{c_bold}{bg_bRed}Important{c_end}{fg_red}{c_bold}\ue0b4{c_end}\n'
        for x in self.todo_list['urgent']:
            impt += f'\u200b       \ue285 {c_urgent}{bg_magenta}{fg_white} {x.ljust(20)} {c_end}\n'

        unimpt = f'{c_bold}{fg_bBlue}\ue0b6{c_end}{c_bold}{bg_bBlue}Unimportant{c_end}{fg_bBlue}{c_bold}\ue0b4{c_end}\n'
        for x in self.todo_list['nonurgent']:
            unimpt += f'\u200b       \ue285 {c_bold}{bg_magenta}{fg_white} {x.ljust(20)} {c_end}\n'

        print(f'{impt}\n{unimpt}')

    def send_help(self):
        subprocess.run('clear')
        input("""
Commands:
    insert <urgent/unimpt> <task>     - Inserts an urgent/unimpt task.
    remove <urgent/unimpt> <task#>    - Removes an urgent/unimpt task.
    clear <urgent/unimpt>             - Clears all urgent/unimpt task.
    end                             - Ends the session, saves the list of tasks.
    help(?)                         - Shows this message.
                
Press enter to continue..""")

    def send_finished_tasks(self):
        subprocess.run('clear')
        op = 'You have finished/removed {self.done_tasks} this session! Have a good day.' if self.done_tasks >= 1 else 'You haven\'t finished/removed any task this session. Have a good day.'
        print(op)
        time.sleep(3)

    def run(self):
        self.main()
            
    def main(self):
        while True:
            subprocess.run('clear')
            self.show_all_tasks()
            print('\n'*3)
            command = input(f'{c_bold}{bg_yellow}\u200b  \uf061{c_end}{fg_yellow}\ue0b0{c_end} ')
            command = str(command)

            if command == '?' or command.lower() == 'help':
                self.send_help()

            elif command.lower() == 'end':
                self.save_list()
                self.send_finished_tasks()
                break

            elif command.lower().startswith('insert'):
                if 'urgent' not in command and 'unimpt' not in command:
                    print('Unrecognized command, please try again.')
                    return time.sleep(3)

                if 'urgent' in command:
                    task = command.replace('insert urgent ', '')
                    self.add_new_impt_task(task)
                    print(f'Successfully added "{task}"!')
                    time.sleep(3)
                    continue

                task = command.replace('insert unimpt ', '')
                self.add_new_task(task)
                print(f'Successfully added "{task}"!')
                time.sleep(3)
            
            elif command.lower().startswith('remove'):
                if 'urgent' not in command and 'unimpt' not in command:
                    print('Unrecognized command, please try again.')
                    return time.sleep(3)

                if 'urgent' in command:
                    task = command.replace('remove urgent ', '')
                    removed = self.remove_impt_task(int(task))
                    print(f'Successfully removed "{removed}"!')
                    time.sleep(3)
                    continue

                task = command.replace('remove unimpt ', '')
                removed = self.remove_task(int(task))
                print(f'Successfully removed "{removed}"!')
                time.sleep(3)

            elif command.lower().startswith('clear'):
                if 'urgent' in command:
                    self.todo_list['urgent'] = []
                    self.save_list()
                    print('Successfully cleared urgent todo-list!')
                    time.sleep(3)
                    continue

                self.todo_list['nonurgent'] = []
                self.save_list()
                print('Successfully cleared unimportant todo-list!')
                time.sleep(3)

            else:
                print('Unrecognized command, please try again..')
                time.sleep(3)

if __name__ == '__main__':
    todo = Todo()
    todo.run()
