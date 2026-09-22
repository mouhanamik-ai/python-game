import os
import time

# ألوان ANSI للواجهة النصية
COLOR_RESET = "\033[0m"
COLOR_TITLE = "\033[1;36m"
COLOR_CYAN = "\033[0;36m"
COLOR_YELLOW = "\033[1;33m"
COLOR_GREEN = "\033[1;32m"
COLOR_RED = "\033[1;31m"
COLOR_GRAY = "\033[1;30m"

DISK_COLORS = [
    "\033[1;31m", "\033[1;33m", "\033[1;32m", 
    "\033[1;36m", "\033[1;34m", "\033[1;35m", 
    "\033[1;91m", "\033[1;93m"
]

class TowerOfHanoi:
    def __init__(self, disks=3, mode="free", time_limit=0, move_limit=0):
        self.disks = disks
        self.mode = mode
        self.time_limit = time_limit
        self.move_limit = move_limit
        self.towers = {'A': list(range(disks, 0, -1)), 'B': [], 'C': []}
        self.moves = 0
        self.history = []
        self.start_time = None

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def draw(self, status_msg=""):
        self.clear_screen()
        print(f"{COLOR_TITLE}============================================={COLOR_RESET}")
        print(f"{COLOR_TITLE}           TOWER OF HANOI - PRO             {COLOR_RESET}")
        print(f"{COLOR_TITLE}============================================={COLOR_RESET}")
        
        min_moves = (2 ** self.disks) - 1
        elapsed = int(time.time() - self.start_time) if self.start_time else 0
        
        print(f" Mode: {self.mode.upper()} | Minimum Moves: {min_moves}")
        print(f" Moves Done: {self.moves}", end="")
        if self.move_limit > 0:
            print(f" / Max: {self.move_limit}", end="")
        
        print(f" | Time: {elapsed}s", end="")
        if self.time_limit > 0:
            remaining = max(0, self.time_limit - elapsed)
            print(f" / Left: {remaining}s", end="")
        print("\n")

        max_w = self.disks * 2 + 1
        height = self.disks

        for lvl in range(height - 1, -1, -1):
            line = ""
            for t in ['A', 'B', 'C']:
                if lvl < len(self.towers[t]):
                    d_size = self.towers[t][lvl]
                    color = DISK_COLORS[(d_size - 1) % len(DISK_COLORS)]
                    disk_str = f"{color}" + "█" * (d_size * 2 - 1) + f"{COLOR_RESET}"
                    
                    padding = (max_w - (d_size * 2 - 1)) // 2
                    line += " " * padding + disk_str + " " * padding + "  "
                else:
                    line += f"{COLOR_GRAY}|{COLOR_RESET}".center(max_w) + "  "
            print(line)

        print(COLOR_GRAY + "-" * (max_w * 3 + 6) + COLOR_RESET)
        print("A".center(max_w) + "  " + "B".center(max_w) + "  " + "C".center(max_w) + "\n")

        if status_msg:
            print(status_msg)

    def move_disk(self, src, dst, record_history=True):
        src, dst = src.upper(), dst.upper()
        if src not in self.towers or dst not in self.towers:
            return False, f"{COLOR_RED}[!] Invalid tower name.{COLOR_RESET}"
        if not self.towers[src]:
            return False, f"{COLOR_RED}[!] Source tower is empty.{COLOR_RESET}"
        if self.towers[dst] and self.towers[src][-1] > self.towers[dst][-1]:
            return False, f"{COLOR_RED}[!] Cannot place larger disk on smaller disk.{COLOR_RESET}"

        disk = self.towers[src].pop()
        self.towers[dst].append(disk)
        self.moves += 1
        
        if record_history:
            self.history.append((src, dst))
            
        return True, f"{COLOR_GREEN}[+] Disk moved successfully.{COLOR_RESET}"

    def undo(self):
        if not self.history:
            return False, f"{COLOR_YELLOW}[!] No moves to undo.{COLOR_RESET}"
        
        src, dst = self.history.pop()
        disk = self.towers[dst].pop()
        self.towers[src].append(disk)
        self.moves -= 1
        return True, f"{COLOR_GREEN}[+] Undo successful.{COLOR_RESET}"

    def get_next_best_move(self):
        def solve_steps(n, source, target, auxiliary, steps):
            if n > 0:
                solve_steps(n - 1, source, auxiliary, target, steps)
                steps.append((source, target))
                solve_steps(n - 1, auxiliary, target, source, steps)

        optimal_steps = []
        solve_steps(self.disks, 'A', 'C', 'B', optimal_steps)
        
        if self.moves < len(optimal_steps):
            next_move = optimal_steps[self.moves]
            return f"{COLOR_YELLOW}[Hint] Move disk from {next_move[0]} to {next_move[1]}{COLOR_RESET}"
        return f"{COLOR_YELLOW}[Hint] Follow optimal path to destination.{COLOR_RESET}"

    def is_won(self):
        return len(self.towers['C']) == self.disks or len(self.towers['B']) == self.disks

    def is_failed(self):
        if self.move_limit > 0 and self.moves >= self.move_limit and not self.is_won():
            return True, "Reached maximum move limit!"
        if self.time_limit > 0 and self.start_time:
            if time.time() - self.start_time > self.time_limit and not self.is_won():
                return True, "Time limit expired!"
        return False, ""

    def auto_solve(self, n, src, dst, aux):
        if n == 1:
            self.move_disk(src, dst, record_history=False)
            self.draw(f"{COLOR_CYAN}[Auto-Solving] Moving {src} -> {dst}{COLOR_RESET}")
            time.sleep(0.3)
            return
        self.auto_solve(n - 1, src, aux, dst)
        self.move_disk(src, dst, record_history=False)
        self.draw(f"{COLOR_CYAN}[Auto-Solving] Moving {src} -> {dst}{COLOR_RESET}")
        time.sleep(0.3)
        self.auto_solve(n - 1, aux, dst, src)

def main():
    stats = {"played": 0, "won": 0}
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{COLOR_TITLE}=== TOWER OF HANOI: SYSTEM MENU ==={COLOR_RESET}")
        print("1. Free Play Mode")
        print("2. Time Attack Mode")
        print("3. Strict Move Limit Mode")
        print("4. View Session Statistics")
        print("5. Exit")
        
        choice = input("\nSelect Mode (1-5): ").strip()
        
        if choice == '5':
            print("Exiting application...")
            break
        elif choice == '4':
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"{COLOR_TITLE}=== SESSION STATISTICS ==={COLOR_RESET}")
            print(f"Games Played: {stats['played']}")
            print(f"Games Won   : {stats['won']}")
            input("\nPress Enter to return...")
            continue
        elif choice not in ['1', '2', '3']:
            continue

        disks = 3
        try:
            disks = int(input("Number of Disks (3-8): "))
            if disks < 3 or disks > 8:
                disks = 3
        except ValueError:
            disks = 3

        mode = "free"
        time_limit = 0
        move_limit = 0
        min_moves = (2 ** disks) - 1

        if choice == '2':
            mode = "time attack"
            time_limit = disks * 15
        elif choice == '3':
            mode = "move limit"
            move_limit = min_moves + 2

        game = TowerOfHanoi(disks, mode, time_limit, move_limit)
        game.start_time = time.time()
        stats["played"] += 1
        msg = ""

        while True:
            game.draw(msg)
            msg = ""

            failed, reason = game.is_failed()
            if failed:
                print(f"{COLOR_RED}[GAME OVER] {reason}{COLOR_RESET}")
                input("\nPress Enter to continue...")
                break

            if game.is_won():
                elapsed = int(time.time() - game.start_time)
                stats["won"] += 1
                print(f"{COLOR_GREEN}[VICTORY] Completed in {game.moves} moves and {elapsed}s!{COLOR_RESET}")
                input("\nPress Enter to continue...")
                break

            print("Commands: [AB = Move A to B] | [u = Undo] | [h = Hint] | [auto = Solve] | [q = Quit]")
            cmd = input("Command > ").strip().lower()

            if cmd == 'q':
                break
            elif cmd == 'u':
                _, msg = game.undo()
            elif cmd == 'h':
                msg = game.get_next_best_move()
            elif cmd == 'auto':
                game.towers = {'A': list(range(disks, 0, -1)), 'B': [], 'C': []}
                game.moves = 0
                game.auto_solve(disks, 'A', 'C', 'B')
                stats["won"] += 1
                input("\n[Auto-Solve Completed] Press Enter to continue...")
                break
            elif len(cmd) == 2:
                _, msg = game.move_disk(cmd[0], cmd[1])

if __name__ == "__main__":
    main()
                  
