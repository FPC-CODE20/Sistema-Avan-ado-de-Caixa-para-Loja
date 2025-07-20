# Django settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'loja_caixa',
        'USER': 'postgres',
        'PASSWORD': 'senha_segura',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Configurações de segurança
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
