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
        return self.current_dir
