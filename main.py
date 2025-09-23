def main():
    vfs_name = "my_vfs"

    while True:
        try:
            command = input(f"{vfs_name}$ ").strip()
            if not command:
                continue
            print(f"[DEBUG] Вы ввели: {command}")


        except KeyboardInterrupt:
            print("\nВыход...")
            break

if __name__ == "__main__":
    main()