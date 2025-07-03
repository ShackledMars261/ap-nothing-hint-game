from pymem import Pymem, process
import sys

class WindowsHelper: # Can add additional Operating Systems as new classes if needed
    def __init__(self, exe_name: str = "Nothing.exe") -> None:
        try:
            self.pm: Pymem = Pymem(exe_name)
        except Exception as e:
            if f'Could not find process: {exe_name}' == str(e):
                print(f'Please launch Nothing.exe')
                sys.exit(1)
            else:
                print(f'Unknown error: {str(e)}')
                sys.exit(1)

        self.memory_address = self.get_memory_address()

    def read_current_timer(self) -> float:
        return self.pm.read_float(self.memory_address)
    
    def get_memory_address(self, module_name: str = 'mono-2.0-bdwgc.dll'):
        module = process.module_from_name(self.pm.process_handle, module_name)
        address = module.lpBaseOfDll + 0x0072AC60
        address = self.pm.read_ulonglong(address) + 0x70
        address = self.pm.read_ulonglong(address) + 0x68
        address = self.pm.read_ulonglong(address) + 0x96C
        return address
        
class NothingHintGame:
    def __init__(self, milestone: int = 300) -> None:
        self.os: str = sys.platform
        self.milestone: int = milestone

        self.hints_to_give: int = 0

        if 'win32' == self.os:
            self.helper = WindowsHelper()
        else:
            print(f'OS \'{self.os}\' is not supported currently.')
            sys.exit(1)

        self.last_value: int = -1
        self.curr_value: int = -1

        self.next_milestone: int = milestone
        self.milestone_count: int = 0

        self.at_start: bool = True

    def tick(self) -> None:
        self.curr_value = round(self.helper.read_current_timer())

        if self.curr_value == 0:
            self.at_start = False
        
        if self.last_value == -1:
            self.last_value = self.curr_value

        if self.curr_value < self.last_value:
            self.last_value = -1
            self.curr_value = -1
            self.next_milestone = self.milestone
        
        if self.curr_value > self.next_milestone:
            self.milestone_count += 1
            self.next_milestone += self.milestone
            if not self.at_start:
                self.give_hint()

        self.last_value = self.curr_value

    def give_hint(self) -> None:
        print(f'You earned a hint for doing nothing! Giving now..')
        self.hints_to_give += 1

if __name__ == "__main__":
    milestone: int = 300
    hint_game: NothingHintGame = NothingHintGame(milestone)