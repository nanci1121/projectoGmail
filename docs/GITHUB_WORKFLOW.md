# 📘 Guía: GitHub Actions y Pull Requests

## 🤖 ¿Qué son GitHub Actions?

GitHub Actions es un sistema de **CI/CD** (Integración Continua / Despliegue Continuo) que automatiza tareas cuando ocurren eventos en tu repositorio.

### ¿Qué acabamos de configurar?

En `.github/workflows/ci.yml` tenemos un flujo que:

1. **Se activa** cuando:
   - Haces `push` a `main`
   - Alguien crea un Pull Request

2. **Ejecuta** estos pasos:
   - ✅ Instala Python 3.11
   - ✅ Instala las dependencias del proyecto
   - ✅ Ejecuta todas las pruebas con pytest
   - ✅ Si todo pasa → ✅ Marca verde
   - ❌ Si algo falla → ❌ Marca roja (bloquea el merge)

### Ventajas

- 🛡️ **Protección**: No se puede fusionar código roto
- 🚀 **Automatización**: No tienes que acordarte de ejecutar tests
- 📊 **Visibilidad**: Todos ven si los tests pasan
- 🔄 **Consistencia**: Mismo entorno para todos

---

## 🔄 ¿Qué son los Pull Requests?

Un **Pull Request (PR)** es una solicitud para fusionar cambios de una rama a otra.

### Flujo de Trabajo Típico

```
1. Crear rama nueva
   git checkout -b feature/nueva-funcionalidad

2. Hacer cambios y commits
   git add .
   git commit -m "feat: nueva funcionalidad"

3. Subir la rama
   git push -u origin feature/nueva-funcionalidad

4. Crear Pull Request en GitHub
   - GitHub te da un enlace directo
   - O ve a la pestaña "Pull Requests"

5. Revisión
   - Otros revisan el código
   - GitHub Actions ejecuta tests
   - Se discuten cambios

6. Aprobar y Fusionar
   - Si todo está bien → Merge
   - Los cambios pasan a main
```

### Componentes de un PR

1. **Título y Descripción**: Explica qué cambia y por qué
2. **Commits**: Lista de cambios incluidos
3. **Archivos Cambiados**: Diff visual de las modificaciones
4. **Checks**: Resultados de GitHub Actions
5. **Revisiones**: Comentarios y aprobaciones
6. **Conversación**: Discusión sobre el código

---

## 🎯 Ejemplo Práctico: Tu Primer PR

### Acabamos de crear uno juntos:

**Rama**: `feature/add-user-info`
**Cambios**:
- ✅ Nuevo endpoint `/api/user-info`
- ✅ Tests para el endpoint
- ✅ Documentación en el commit

**Próximos pasos**:

1. **Ve a GitHub**: https://github.com/nanci1121/projectoGmail/pull/new/feature/add-user-info

2. **Crea el PR**:
   - Título: "feat: Add user info endpoint"
   - Descripción:
     ```
     ## Cambios
     - Añadido endpoint `/api/user-info` para obtener el email del usuario autenticado
     - Añadidos tests unitarios
     
     ## Motivación
     Útil para mostrar en la interfaz qué cuenta de Gmail está actualmente autenticada.
     
     ## Tests
     - ✅ Todas las pruebas pasan localmente
     - ✅ GitHub Actions verificará automáticamente
     ```

3. **Observa GitHub Actions**:
   - Verás un check amarillo ⏳ (ejecutando)
   - Luego verde ✅ (pasó) o rojo ❌ (falló)

4. **Fusionar**:
   - Click en "Merge pull request"
   - Confirma
   - ¡Listo! Los cambios están en `main`

---

## 🔒 Protecciones de Rama (Branch Protection)

Puedes configurar reglas para proteger `main`:

### Cómo Activarlas

1. Ve a: **Settings** → **Branches** → **Add rule**
2. Branch name pattern: `main`
3. Activa:
   - ✅ **Require pull request before merging**
   - ✅ **Require status checks to pass** (GitHub Actions)
   - ✅ **Require branches to be up to date**

### Resultado

- ❌ No se puede hacer `push` directo a `main`
- ✅ Solo se puede fusionar vía Pull Request
- ✅ Solo si los tests pasan
- 🛡️ Código siempre estable en `main`

---

## 📊 Badges en el README

Puedes añadir badges que muestren el estado de CI:

```markdown
![CI](https://github.com/nanci1121/projectoGmail/workflows/Python%20CI/badge.svg)
```

Esto muestra si el último build pasó o falló.

---

## 🎓 Mejores Prácticas

### Para Pull Requests

1. **Tamaño**: PRs pequeños son más fáciles de revisar
2. **Descripción**: Explica el "por qué", no solo el "qué"
3. **Tests**: Siempre incluye tests para código nuevo
4. **Un objetivo**: Un PR = Una funcionalidad/fix
5. **Commits limpios**: Mensajes descriptivos

### Para GitHub Actions

1. **Rápido**: Tests deben ejecutarse en < 5 minutos
2. **Confiable**: Si falla, debe ser por un problema real
3. **Informativo**: Logs claros cuando algo falla
4. **Seguro**: No expongas secretos en los logs

---

## 🚀 Próximos Pasos

Ahora que entiendes el flujo:

1. **Crea tu primer PR** con los cambios que hicimos
2. **Observa GitHub Actions** ejecutarse
3. **Fusiona el PR** cuando pase
4. **Experimenta**: Crea más ramas y PRs

### Ideas para Practicar

- Añadir un nuevo endpoint
- Mejorar el diseño CSS
- Añadir más tests
- Actualizar documentación

Cada cambio → Nueva rama → PR → Review → Merge

---

**¡Felicidades! Ahora dominas el flujo profesional de desarrollo con Git y GitHub.** 🎉
