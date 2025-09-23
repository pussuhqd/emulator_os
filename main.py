import shlex

def parse_command(line):
    try:
        return shlex.split(line)
    except ValueError as e:
        print(f"Ошибка парсинга: {e}")
        return []

def main():
    vfs_name = "my_vfs"

    while True:

        try:
            line = input(f"{vfs_name}$ ").strip()
            if not line:
                continue

            args = parse_command(line)
            if not args:
                continue

            cmd = args[0]
            if cmd == "exit":
                print("Выход из эмулятора.")
                break
            elif cmd == "ls":
                print(f"[Заглушка] ls: {args[1:]}")
            elif cmd == "cd":
                print(f"[Заглушка] cd: {args[1:]}")
            else:
                print(f"Неизвестная команда: {cmd}")
        except KeyboardInterrupt:
            print("\nВыход...")
            break

if __name__ == "__main__":
    main()