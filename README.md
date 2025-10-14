# undar-examen plugin for [Tutor](https://docs.tutor.edly.io)

Plugin para integrar el entorno de **UNDAR** con **Open edX**, permitiendo desplegar, montar y gestionar los entornos **Authoring**, **Examen** y **Hono (Backend)** desde comandos personalizados de Tutor.

---

## 📦 Instalación

```bash
pip install git+https://github.com/oti-undar/plugin_openedx
```

---

## 🚀 Uso básico

```bash
tutor plugins enable undar-examen
```

Una vez habilitado, el plugin agrega el grupo de comandos:

```bash
tutor undar-examen [comando]
```

---

## 🧭 Manual de usuario

### 🔹 Comando principal

```bash
tutor undar-examen
```

Grupo de comandos personalizados para gestionar entornos de UNDAR (examen, authoring, hono, base de datos, etc).

---

### 🧩 1. Inicializar entorno de **Authoring**

```bash
tutor undar-examen init-authoring
```

**Opciones:**

- `--repo`: Repositorio a clonar (por defecto: `https://github.com/oti-undar/frontendAuth_openedx.git`)
- `--dir`: Carpeta destino (por defecto: `frontend-app-authoring`)

**Qué hace:**

1. Clona o actualiza el repositorio del authoring.
2. Monta el proyecto en Tutor.
3. Detiene los contenedores locales.
4. Reconstruye las imágenes `mfe`.
5. Levanta el entorno en background.

---

### 🧩 2. Inicializar entorno de **Examen**

```bash
tutor undar-examen init-examen
```

**Opciones:**

- `--repo`: Repositorio a clonar (por defecto: `https://github.com/oti-undar/frontend_openedx.git`)
- `--dir`: Carpeta destino (por defecto: `frontend-examen`)

**Qué hace:**

1. Clona o actualiza el repositorio del examen.
2. Monta el proyecto en Tutor.
3. Detiene los contenedores locales.
4. Reconstruye las imágenes `mfe` sin caché.
5. Levanta el entorno en background.

---

### 🧩 3. Inicializar entorno **Hono (Backend)**

```bash
tutor undar-examen init-hono
```

**Opciones:**

- `--repo`: Repositorio a clonar (por defecto: `https://github.com/oti-undar/backend_openedx.git`)
- `--dir`: Carpeta destino (por defecto: `hono-app`)

**Qué hace:**

1. Clona o actualiza el repositorio del backend.
2. Detiene los contenedores locales.
3. Construye la imagen `hono-app`.
4. Elimina contenedores previos (`hono-app-container`).
5. Arranca el contenedor con las variables de entorno correctas.
6. Verifica que el contenedor esté corriendo correctamente.

---

### 🧩 4. Inicializar base de datos

```bash
tutor undar-examen init-db
```

**Qué hace:**

1. Crea la base de datos `undar_plugin_examen`.
2. Crea el usuario `undar_user` con permisos completos.
3. Aplica privilegios.
4. Verifica que MySQL esté disponible antes de ejecutar los comandos.

---

### 🧩 5. Reiniciar base de datos

```bash
tutor undar-examen reiniciar-db
```

**Qué hace:**
Ejecuta `npm run migrate:fresh:linux` dentro del contenedor `hono-app-container`, aplicando migraciones limpias y seeders.

---

### 🧩 6. Migrar base de datos

```bash
tutor undar-examen migrar-db
```

**Qué hace:**
Ejecuta un comando `npx prisma migrate dev` dentro del contenedor `hono-app-container` con un nombre de migración aleatorio.

---

### 🧩 7. Ejecutar seeders

```bash
tutor undar-examen seed-db
```

**Qué hace:**
Corre el comando `npm run seed` dentro del contenedor `hono-app-container`.

---

### 🧩 8. Inicializar todo el plugin (entorno completo)

```bash
tutor undar-examen inicializar-plugin-undar
```

**Qué hace:**
Ejecuta en orden los siguientes comandos:

1. `init-examen`
2. `init-authoring`
3. `init-db`
4. `init-hono`
5. `reiniciar-db`

🔁 Resultado: el entorno UNDAR (frontend, authoring, backend y base de datos) queda completamente listo.

---

### 🧩 9. Remover usuario de base de datos

```bash
tutor undar-examen remove-user
```

**Qué hace:**
Elimina el usuario `undar_user` de MySQL y limpia los privilegios.

---

### 🧩 10. Desinstalar plugin

```bash
tutor undar-examen uninstall
```

**Qué hace:**

1. Elimina el montaje `./frontend-app-authoring`.
2. Ejecuta `remove-user` para eliminar el usuario de MySQL.

---

## ⚙️ Requisitos

- [Tutor](https://docs.tutor.edly.io) instalado y configurado.
- Docker y Docker Compose funcionando.
- Git disponible en el sistema.
- Acceso a los repositorios de UNDAR.

---

## 🧑‍💻 Consejos

- Puedes ejecutar los comandos con `-h` para ver las opciones disponibles:
  ```bash
  tutor undar-examen -h
  ```

---

## 🪪 Licencia

Este software está licenciado bajo los términos de **AGPLv3**.
