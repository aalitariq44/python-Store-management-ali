# -*- coding: utf-8 -*-
import os
import datetime
import requests
import json

class BackupController:
    def __init__(self):
        self.supabase_url = "https://xxqwhvjejjuvlnzanlha.supabase.co"
        self.supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh4cXdodmplamp1dmxuemFubGhhIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MjY2NTEzMywiZXhwIjoyMDY4MjQxMTMzfQ.gk0braqHP-EDIp1_fyV1OmgA10vOCz_dPBO8cVTcSko"
        self.bucket_name = "kadhem"
        self.db_path = "store_management.db"
        self.headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}"
        }

    def backup_database(self):
        try:
            folder_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_name = os.path.basename(self.db_path)
            remote_path = f"{folder_name}/{file_name}"
            
            url = f"{self.supabase_url}/storage/v1/object/{self.bucket_name}/{remote_path}"
            
            with open(self.db_path, "rb") as f:
                response = requests.post(url, headers=self.headers, data=f)
            
            if response.status_code == 200:
                return True, f"تم عمل نسخة احتياطية بنجاح في: {remote_path}"
            else:
                return False, f"حدث خطأ أثناء عمل نسخة احتياطية: {response.text}"
        except Exception as e:
            return False, f"حدث خطأ أثناء عمل نسخة احتياطية: {e}"

    def list_backups(self):
        try:
            url = f"{self.supabase_url}/storage/v1/object/list/{self.bucket_name}"
            response = requests.post(url, headers=self.headers, json={"prefix": "", "limit": 100})
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error listing backups: {response.text}")
                return []
        except Exception as e:
            print(f"Error listing backups: {e}")
            return []
