import os
import datetime
import subprocess
import boto3
from django.conf import settings

class BackupManager:
    def __init__(self):
        self.backup_dir = "/backups"
        os.makedirs(self.backup_dir, exist_ok=True)
        
        # Configuração AWS S3 (opcional)
        self.s3_bucket = "backups-loja-caixa"
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
    
    def criar_backup_local(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(self.backup_dir, f"backup_{timestamp}.sql")
        
        # Comando para dump do PostgreSQL
        cmd = [
            'pg_dump',
            '-h', settings.DATABASES['default']['HOST'],
            '-U', settings.DATABASES['default']['USER'],
            '-d', settings.DATABASES['default']['NAME'],
            '-f', backup_file
        ]
        
        # Executar comando
        env = os.environ.copy()
        env['PGPASSWORD'] = settings.DATABASES['default']['PASSWORD']
        subprocess.run(cmd, env=env, check=True)
        
        return backup_file
    
    def enviar_backup_s3(self, file_path):
        file_name = os.path.basename(file_path)
        self.s3_client.upload_file(file_path, self.s3_bucket, file_name)
        return f"s3://{self.s3_bucket}/{file_name}"
    
    def rotacionar_backups(self, max_local=5, max_s3=30):
        # Rotacionar backups locais
        backups = sorted([
            os.path.join(self.backup_dir, f)
            for f in os.listdir(self.backup_dir)
            if f.startswith('backup_') and f.endswith('.sql')
        ], key=os.path.getmtime)
        
        while len(backups) > max_local:
            os.remove(backups.pop(0))
        
        # Rotacionar backups no S3 (implementação similar)
        # ...
    
    def executar_backup_completo(self):
        try:
            backup_file = self.criar_backup_local()
            s3_path = self.enviar_backup_s3(backup_file)
            self.rotacionar_backups()
            return True, s3_path
        except Exception as e:
            return False, str(e)

# Agendamento com Celery (opcional)
from celery import shared_task

@shared_task
def tarefa_backup_diario():
    manager = BackupManager()
    return manager.executar_backup_completo()
