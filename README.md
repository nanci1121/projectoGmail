# 📧 Gmail Attachment Downloader

Una aplicación web moderna y segura para descargar adjuntos de Gmail de forma visual e intuitiva. Olvídate de la consola, gestiona tus descargas desde el navegador con una interfaz premium.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.127.0-green.svg)

## ✨ Características

- 🎨 **Interfaz Web Premium**: Diseño moderno con efectos glassmorphism y modo oscuro
- 🔐 **Autenticación OAuth2**: Conexión segura con tu cuenta de Gmail
- 📁 **Selector de Carpetas**: Descarga adjuntos de etiquetas específicas o de todos los correos
- ⏸️ **Control Total**: Botones para iniciar, detener y cambiar de cuenta
- 📊 **Progreso en Tiempo Real**: Barra de progreso y lista de archivos descargados
- 👥 **Multi-usuario**: Cambia fácilmente entre diferentes cuentas de Gmail
- 🧪 **Testing**: Suite de pruebas unitarias con pytest
- 🚀 **CI/CD**: Integración continua con GitHub Actions

## 📁 Estructura del Proyecto

```
projectoGmail/
├── backend/              # Lógica del servidor
│   ├── app.py            # Servidor FastAPI
│   ├── web_logic.py      # Gestión de Gmail y descargas
│   ├── descargar_adjuntos.py  # Script CLI original
│   ├── tests/            # Pruebas unitarias
│   └── requirements.txt  # Dependencias Python
├── frontend/             # Interfaz web
│   ├── static/           # CSS y JavaScript
│   └── templates/        # Plantillas HTML
├── downloads/            # Archivos descargados (gitignored)
└── .github/
    └── workflows/        # GitHub Actions CI
```

## 🚀 Instalación

### 1. Requisitos Previos

- Python 3.11 o superior
- Una cuenta de Google
- Git (para clonar el repositorio)

### 2. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/projectoGmail.git
cd projectoGmail
```

### 3. Crear Entorno Virtual

```bash
python -m venv venv

# En Linux/Mac
source venv/bin/activate

# En Windows
.\venv\Scripts\activate
```

### 4. Instalar Dependencias

```bash
pip install -r backend/requirements.txt
```

### 5. Configurar Credenciales de Google

Este es el paso más importante. Necesitas crear credenciales OAuth2 en Google Cloud:

#### Pasos Detallados:

1. **Accede a Google Cloud Console**:
   - Ve a [https://console.cloud.google.com/apis/credentials](https://console.cloud.google.com/apis/credentials)

2. **Crea un Proyecto Nuevo** (o selecciona uno existente)

3. **Habilita la API de Gmail**:
   - Ve a "Biblioteca de APIs"
   - Busca "Gmail API"
   - Haz clic en "Habilitar"

4. **Configura la Pantalla de Consentimiento**:
   - Ve a "Pantalla de consentimiento de OAuth"
   - Selecciona **"Externo"**
   - Rellena:
     - Nombre de la aplicación: `Gmail Downloader`
     - Correo de asistencia: tu email
     - Dominio de la aplicación: (puedes dejarlo vacío)
   - En **"Usuarios de prueba"**, añade tu dirección de Gmail
   - Guarda y continúa

5. **Crea las Credenciales**:
   - Ve a "Credenciales" → "+ CREAR CREDENCIALES"
   - Selecciona **"ID de cliente de OAuth"**
   - Tipo de aplicación: **"Aplicación de escritorio"**
   - Nombre: `Gmail Downloader Desktop`
   - Haz clic en "Crear"

6. **Descarga el Archivo**:
   - Haz clic en el botón de descarga (icono ⬇️)
   - Guarda el archivo como `credentials.json` en la carpeta `backend/`

### 6. Configurar Variables de Entorno (Opcional)

Crea un archivo `.env` en la carpeta `backend/` si quieres personalizar la configuración:

```env
GMAIL_SCOPES=https://www.googleapis.com/auth/gmail.readonly
GMAIL_CREDENTIALS_FILE=credentials.json
GMAIL_TOKEN_FILE=token.json
DOWNLOAD_DIR=../downloads
```

## 🎯 Uso

### Modo Web (Recomendado)

1. **Inicia el servidor**:
   ```bash
   ./venv/bin/python backend/app.py
   ```

2. **Abre tu navegador**:
   - Ve a [http://localhost:8000](http://localhost:8000)

3. **Primera vez**:
   - Se abrirá automáticamente una ventana del navegador pidiendo permisos
   - Inicia sesión con tu cuenta de Gmail
   - Acepta los permisos solicitados
   - ¡Listo! Ya puedes descargar adjuntos

4. **Cambiar de cuenta**:
   - Haz clic en "Cambiar de cuenta" en la barra lateral
   - Confirma la acción
   - Inicia sesión con otra cuenta de Gmail

### Modo Consola (Script Original)

Si prefieres usar la línea de comandos:

```bash
cd backend
python descargar_adjuntos.py
```

## 🧪 Pruebas

### Ejecutar Pruebas Unitarias

```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/backend
./venv/bin/pytest backend/tests/ -v
```

### Cobertura de Pruebas

```bash
./venv/bin/pytest backend/tests/ --cov=backend --cov-report=html
```

## 🔒 Seguridad

- ✅ **OAuth2**: Autenticación segura con Google
- ✅ **Tokens Locales**: Las credenciales se almacenan solo en tu máquina
- ✅ **`.gitignore`**: Configurado para nunca subir credenciales a GitHub
- ✅ **HTTPS**: Comunicación cifrada con la API de Gmail
- ✅ **Sin Contraseñas**: No se almacenan contraseñas en ningún momento

### ⚠️ Archivos Sensibles (NUNCA subir a GitHub)

- `backend/credentials.json` - Credenciales de OAuth2
- `backend/token.json` - Token de acceso del usuario
- `backend/.env` - Variables de entorno

Estos archivos ya están en `.gitignore` para protegerte.

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. Haz un fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Haz commit de tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Estándares de Código

- Seguimos los principios de **Clean Architecture**
- Código simple y fácil de entender
- Pruebas unitarias para nuevas funcionalidades
- Desarrollo seguro siguiendo OWASP

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🙏 Agradecimientos

- [FastAPI](https://fastapi.tiangolo.com/) - Framework web moderno
- [Google Gmail API](https://developers.google.com/gmail/api) - API de Gmail
- Inspirado en la necesidad de hacer la tecnología más accesible para todos

## 📞 Soporte

Si tienes problemas:

1. Revisa la sección de [Issues](https://github.com/tu-usuario/projectoGmail/issues)
2. Crea un nuevo issue describiendo el problema
3. Incluye logs y capturas de pantalla si es posible

---

**Desarrollado con ❤️ siguiendo los principios de desarrollo seguro especificados en `GEMINI.md`**
