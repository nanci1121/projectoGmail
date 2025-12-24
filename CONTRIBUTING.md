# Gmail Attachment Downloader - Guía de Contribución

¡Gracias por tu interés en contribuir! Este documento te guiará en el proceso.

## 🚀 Cómo Contribuir

### 1. Fork y Clone

```bash
# Haz fork del repositorio en GitHub
# Luego clona tu fork
git clone https://github.com/TU-USUARIO/projectoGmail.git
cd projectoGmail
```

### 2. Crea una Rama

```bash
git checkout -b feature/mi-nueva-funcionalidad
```

### 3. Configura el Entorno

```bash
python -m venv venv
source venv/bin/activate  # En Windows: .\venv\Scripts\activate
pip install -r backend/requirements.txt
```

### 4. Realiza tus Cambios

- Escribe código limpio y bien documentado
- Sigue los principios de Clean Architecture
- Añade pruebas unitarias para nuevas funcionalidades

### 5. Ejecuta las Pruebas

```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/backend
./venv/bin/pytest backend/tests/ -v
```

### 6. Commit y Push

```bash
git add .
git commit -m "feat: descripción clara de tu cambio"
git push origin feature/mi-nueva-funcionalidad
```

### 7. Crea un Pull Request

- Ve a GitHub y crea un Pull Request
- Describe claramente qué cambia y por qué
- Espera la revisión del código

## 📋 Estándares de Código

### Python
- Usa nombres descriptivos en español para variables y funciones
- Máximo 100 caracteres por línea
- Docstrings para funciones públicas
- Type hints cuando sea posible

### Commits
Usamos [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` Nueva funcionalidad
- `fix:` Corrección de bug
- `docs:` Cambios en documentación
- `test:` Añadir o modificar tests
- `refactor:` Refactorización de código
- `style:` Cambios de formato (no afectan lógica)

### Testing
- Toda nueva funcionalidad debe tener tests
- Mantén la cobertura de tests > 80%
- Usa mocks para APIs externas

## 🔒 Seguridad

- NUNCA subas credenciales reales
- Revisa que `.gitignore` esté actualizado
- Reporta vulnerabilidades de forma privada

## ❓ Preguntas

Si tienes dudas, abre un [Issue](https://github.com/tu-usuario/projectoGmail/issues) con la etiqueta `question`.

¡Gracias por contribuir! 🎉
