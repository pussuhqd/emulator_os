@echo off
echo test minimal vfs:
python main.py --vfs-path vfs_min.json --script scripts/start_3.txt

echo.
echo 2.run not exist vfs (error):
python main.py --vfs-path nonexistent.json --script scripts/start_3.txt

