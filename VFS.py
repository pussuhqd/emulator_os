import base64
import json


class VirtualFileSystem:
    def __init__(self,vfs_path):
        self.vfs_path = vfs_path
        self.current_dir = "/"
        self.data = self._load_vfs()
        self.show_motd()

    def _load_vfs(self):
        with open(self.vfs_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def show_motd(self):
        if 'motd' in self.data:
            print(self.data['motd'])

    def _get_node(self, path):
        if not path.startswith('/'):
            if self.current_dir == "/":
                path = f"/{path}"
            else:
                path = f"{self.current_dir}/{path}"

        if path == "/":
            return self.data

        parts = [p for p in path.split('/') if p]
        current = self.data

        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None

        return current

    def list_directory(self, path=""):
        if path == "":
            path = self.current_dir

        node = self._get_node(path)
        if node is None:
            return []

        if not isinstance(node, dict):
            return []

        items = []
        for name, content in node.items():
            if name == 'motd':
                continue
            if isinstance(content, dict) and content.get('type') == 'file':
                items.append(name)
            else:
                items.append(f"{name}/")

        return sorted(items)

    def change_directory(self, path):
        if path == "..":
            if self.current_dir == "/":
                return True

            parts = [p for p in self.current_dir.split('/') if p]
            if len(parts) > 1:
                new_path = "/" + "/".join(parts[:-1])
            else:
                new_path = "/"

            node = self._get_node(new_path)
            if node is not None and isinstance(node, dict):
                self.current_dir = new_path
                return True
            else:
                return False

        if path.startswith('/'):
            target_path = path
        else:
            if self.current_dir == "/":
                target_path = f"/{path}"
            else:
                target_path = f"{self.current_dir}/{path}"

        node = self._get_node(target_path)
        if node is not None and isinstance(node, dict):
            self.current_dir = target_path
            return True
        else:
            return False

    def get_file_content(self, path):
        node = self._get_node(path)
        if node and isinstance(node, dict) and node.get('type') == 'file':
            data = node.get('data', '')
            try:
                return base64.b64decode(data).decode('utf-8')
            except:
                return data
        return None

    def get_current_path(self):
        return self.current_dir.rstrip('/')

    def show_tree(self, path=""):
        if path == "":
            path = self.current_dir

        node = self._get_node(path)
        if node is None or not isinstance(node, dict):
            print(f"tree: '{path}': Нет такого файла или каталога")
            return

        print(path if path != "/" else "/")
        self._show_tree_recursive(node, "", path)

    def _show_tree_recursive(self, node, prefix, current_path):
        if not isinstance(node, dict):
            return

        items = sorted(node.items())

        for i, (name, content) in enumerate(items):
            is_last = i == len(items) - 1
            connector = "└── " if is_last else "├── "

            if isinstance(content, dict) and content.get('type') == 'file':
                print(f"{prefix}{connector}{name}")
            else:
                print(f"{prefix}{connector}{name}/")
                if isinstance(content, dict) and content.get('type') != 'file':
                    next_prefix = prefix + ("    " if is_last else "│   ")
                    self._show_tree_recursive(content, next_prefix, f"{current_path}/{name}")

    def copy_file(self, source, dest):
        """Копирует файл из source в dest"""
        # Получаем абсолютные пути
        if not source.startswith('/'):
            if self.current_dir == "/":
                source = f"/{source}"
            else:
                source = f"{self.current_dir}/{source}"

        if not dest.startswith('/'):
            if self.current_dir == "/":
                dest = f"/{dest}"
            else:
                dest = f"{self.current_dir}/{dest}"

        # Находим исходный файл
        source_node = self._get_node(source)
        if not source_node or not isinstance(source_node, dict) or source_node.get('type') != 'file':
            return False

        # Разбиваем путь назначения
        import os
        dest_parts = [p for p in dest.split('/') if p]
        if not dest_parts:
            return False

        dest_file_name = dest_parts[-1]
        dest_folder_path = "/" + "/".join(dest_parts[:-1]) if len(dest_parts) > 1 else "/"

        dest_folder_node = self._get_node(dest_folder_path)
        if not dest_folder_node or not isinstance(dest_folder_node, dict):
            return False

        # Копируем
        dest_folder_node[dest_file_name] = source_node.copy()
        return True

    def remove_item(self, path, recursive=False):
        """Удаляет файл или папку"""
        # Делаем путь абсолютным
        if not path.startswith('/'):
            if self.current_dir == "/":
                path = f"/{path}"
            else:
                path = f"{self.current_dir}/{path}"

        import os
        path = os.path.normpath(path).replace('\\', '/')

        parts = [p for p in path.split('/') if p]
        if not parts:
            return False

        item_name = parts[-1]
        parent_path = "/" + "/".join(parts[:-1]) if len(parts) > 1 else "/"

        parent_node = self._get_node(parent_path)
        if not parent_node or not isinstance(parent_node, dict):
            return False

        if item_name not in parent_node:
            return False

        item_node = parent_node[item_name]

        # Это файл
        if isinstance(item_node, dict) and item_node.get('type') == 'file':
            del parent_node[item_name]
            return True

        # Это папка
        if isinstance(item_node, dict):
            if not recursive:
                return False
            del parent_node[item_name]
            return True

        return False