import json, time

class Colors:
    def __init__(self):
        self.end = '\033[0m'
        self.bold = '\033[1m'
        self.blink = '\033[5m'
        self.urgent = f'{self.bold}{self.blink}'

        self.fg_black = '\033[37;30m'
        self.fg_red = '\033[37;31m'
        self.fg_green = '\033[37;32m'
        self.fg_yellow = '\033[37;33m'
        self.fg_blue = '\033[37;34m'
        self.fg_magenta = '\033[37;35m'
        self.fg_cyan = '\033[37;36m'
        self.fg_white = '\033[37;37m'
        self.fg_gray = '\033[37;90m'
        self.fg_bRed = '\033[37;91m'
        self.fg_bGreen = '\033[37;92m'
        self.fg_bYellow = '\033[37;93m'
        self.fg_bBlue = '\033[37;94m'
        self.fg_bMagenta = '\033[37;95m'
        self.fg_bCyan = '\033[37;96m'
        self.fg_bWhite = '\033[37;97m'

        self.bg_black = '\033[47;40m'
        self.bg_red = '\033[47;41m'
        self.bg_green = '\033[47;42m'
        self.bg_yellow = '\033[47;43m'
        self.bg_blue = '\033[47;44m'
        self.bg_magenta = '\033[47;45m'
        self.bg_cyan = '\033[47;46m'
        self.bg_white = '\033[47;47m'
        self.bg_gray = '\033[47;100m'
        self.bg_bRed = '\033[47;101m'
        self.bg_bGreen = '\033[47;102m'
        self.bg_bYellow = '\033[47;103m'
        self.bg_bBlue = '\033[47;104m'
        self.bg_bMagenta = '\033[47;105m'
        self.bg_bCyan = '\033[47;106m'
        self.bg_bWhite = '\033[47;107m'


class Todo(object):
    def __init__(self):
        with open('./todolist.json', 'r') as f:
            self.todo_list = json.load(f)
        self.done_tasks = 0
        self.clrs = Colors()

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
        print(f'{self.clrs.bold}{self.clrs.fg_red}\ue0b6{self.clrs.end}{self.clrs.bold}{self.clrs.bg_bRed}Important{self.clrs.end}{self.clrs.fg_red}{self.clrs.bold}\ue0b4{self.clrs.end}')
        for x in self.todo_list['urgent']:
            print(f'\u200b      \ue285 {self.clrs.urgent}{self.clrs.bg_magenta}{self.clrs.fg_white} {x.ljust(20)} {self.clrs.end}')
        print('\n')
        print(f'{self.clrs.bold}{self.clrs.fg_bBlue}\ue0b6{self.clrs.end}{self.clrs.bold}{self.clrs.bg_bBlue}Unimportant{self.clrs.end}{self.clrs.fg_bBlue}{self.clrs.bold}\ue0b4{self.clrs.end}')
        for x in self.todo_list['nonurgent']:
            print(f'\u200b      \ue285 {self.clrs.bold}{self.clrs.bg_magenta}{self.clrs.fg_white} {x.ljust(20)} {self.clrs.end}')

    def run(self):
        self.main()
            
    def main(self):
        while True:
            print('\n'*20)
            self.show_all_tasks()
            print('\n'*3)
            command = input(f'{self.clrs.bold}{self.clrs.bg_yellow}\u200b  \uf061{self.clrs.end}{self.clrs.fg_yellow}\ue0b0{self.clrs.end} ')
            command = str(command)

            if command == '?' or command.lower() == 'help':
                input("""
Commands:
    insert <urgent/unimpt> <task>     - Inserts an urgent/unimpt task.
    remove <urgent/unimpt> <task#>    - Removes an urgent/unimpt task.
    clear <urgent/unimpt>             - Clears all urgent/unimpt task.
    end                             - Ends the session, saves the list of tasks.
    help(?)                         - Shows this message.
                
Press enter to continue..""")

            elif command.lower() == 'end':
                self.save_list()
                break

            elif command.lower().startswith('insert'):
                if 'urgent' not in command and 'unimpt' not in command:
                    print('Unrecognized command, please try again.')
                    time.sleep(3)
                    return

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
                    time.sleep(3)
                    return

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
