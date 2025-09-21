import json
from datetime import datetime

class JSONFileDB:
    """Class สำหรับจัดการข้อมูลในไฟล์ JSON."""
    def __init__(self, filename):
        self.filepath = f'data/{filename}.json'
        self.data = self._load_data()

    def _load_data(self):
        """โหลดข้อมูลจากไฟล์ JSON."""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def _save_data(self):
        """บันทึกข้อมูลลงในไฟล์ JSON."""
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def get_all(self):
        """ดึงข้อมูลทั้งหมด."""
        return self.data

    def find_one(self, key, value):
        """ค้นหาข้อมูลชิ้นเดียวจาก key/value."""
        for item in self.data:
            if item.get(key) == value:
                return item
        return None

    def find_many(self, key, value):
        """ค้นหาข้อมูลหลายชิ้นจาก key/value."""
        return [item for item in self.data if item.get(key) == value]
    
    def add(self, new_item):
        """เพิ่มข้อมูลใหม่และบันทึก."""
        self.data.append(new_item)
        self._save_data()

candidates_db = JSONFileDB('candidates')
jobs_db = JSONFileDB('jobs')
companies_db = JSONFileDB('companies')
applications_db = JSONFileDB('applications')