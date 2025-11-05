undar-examen plugin for `Tutor <https://docs.tutor.edly.io>`_
=============================================================

Plugin Open Edx para Evaluación por Competencias en Educación Musical y Artes, personalizado para el entorno de la **UNDAR**, permitiendo desplegar, montar y gestionar los entornos **Authoring**, **Examen** y **Hono (Backend)** desde comandos personalizados de Tutor.

Equipo de Investigadores Docentes de la UNDAR:

Aland Bravo Vecorena
ORCID: 0000-0002-1802-8402

Jorge Gadi Marcellini Morales
ORCID: 0000-0003-1952-6988

Fabio Rodríguez Meléndez
ORCID: 0000-0003-4533-5595

---

📦 Instalación
---------------

.. code-block:: bash

    pip install git+https://github.com/oti-undar/plugin_openedx

---

🚀 Uso básico
--------------

.. code-block:: bash

    tutor plugins enable undar-examen

Una vez habilitado, el plugin agrega el grupo de comandos:

.. code-block:: bash

    tutor undar-examen [comando]

---

🧭 Manual de usuario
---------------------

🔹 Comando principal
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    tutor undar-examen


📋 Orden de ejecución
-----------------------

Primero debe inicializar el plugin UNDAR:

.. code-block:: bash

    tutor undar-examen inicializar-plugin-undar

Luego debe dar permiso de escritura para subir los archivos de los examenes para que puedan persistir en caso se realicen actualizaciones en el backend:

.. code-block:: bash

    sudo chown -R 1001:1001 "$(tutor config printroot)/env/plugins/undar-examen/build/examenes"

---

Grupo de comandos personalizados para gestionar entornos de UNDAR (examen, authoring, hono, base de datos, etc).

---

🧩 1. Inicializar entorno de **Authoring**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    tutor undar-examen init-authoring

**Opciones:**

- ``--repo``: Repositorio a clonar (por defecto: ``https://github.com/oti-undar/frontendAuth_openedx.git``)
- ``--dir``: Carpeta destino (por defecto: ``frontend-app-authoring``)

**Qué hace:**

1. Clona o actualiza el repositorio del authoring.
2. Monta el proyecto en Tutor.
3. Detiene los contenedores locales.
4. Reconstruye las imágenes ``mfe``.
5. Levanta el entorno en background.

---

🧩 2. Inicializar entorno de **Examen**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    tutor undar-examen init-examen

**Opciones:**

- ``--repo``: Repositorio a clonar (por defecto: ``https://github.com/oti-undar/frontend_openedx.git``)
- ``--dir``: Carpeta destino (por defecto: ``frontend-examen``)

**Qué hace:**

1. Clona o actualiza el repositorio del examen.
2. Monta el proyecto en Tutor.
3. Detiene los contenedores locales.
4. Reconstruye las imágenes ``mfe`` sin caché.
5. Levanta el entorno en background.

---

🧩 3. Inicializar entorno **Hono (Backend)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    tutor undar-examen init-hono

**Opciones:**

- ``--repo``: Repositorio a clonar (por defecto: ``https://github.com/oti-undar/backend_openedx.git``)
- ``--dir``: Carpeta destino (por defecto: ``hono-app``)

**Qué hace:**

1. Clona o actualiza el repositorio del backend.
2. Detiene los contenedores locales.
3. Construye la imagen ``hono-app``.
4. Elimina contenedores previos (``hono-app-container``).
5. Arranca el contenedor con las variables de entorno correctas.
6. Verifica que el contenedor esté corriendo correctamente.

---

🧩 4. Inicializar base de datos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    tutor undar-examen init-db

**Qué hace:**

1. Crea la base de datos ``undar_plugin_examen``.
2. Crea el usuario ``undar_user`` con permisos completos.
3. Aplica privilegios.
4. Verifica que MySQL esté disponible antes de ejecutar los comandos.

---

🧩 5. Truncar base de datos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    tutor undar-examen truncar-db

**Qué hace:**
1. Elimina la base de datos ``undar_plugin_examen``.
2. Recrea la base de datos ``undar_plugin_examen``.

---

🧩 6. Migrar base de datos
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    tutor undar-examen migrar-db

**Qué hace:**
Ejecuta un comando ``npx prisma migrate deploy`` dentro del contenedor ``hono-app-container``.

---

🧩 7. Ejecutar seeders
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    tutor undar-examen seed-db

**Qué hace:**
Corre el comando ``npm run seed`` dentro del contenedor ``hono-app-container``.

---

🧩 8. Inicializar todo el plugin (entorno completo)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    tutor undar-examen inicializar-plugin-undar

**Qué hace:**
Ejecuta en orden los siguientes comandos:

1. ``init-examen``
2. ``init-authoring``
3. ``init-db``
4. ``init-hono``
5. ``truncar-db``
6. ``migrar-db``
7. ``seed-db``

🔁 **Resultado:** el entorno UNDAR (frontend, authoring, backend y base de datos) queda completamente listo.

---

🧩 9. Remover usuario de base de datos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    tutor undar-examen remove-user

**Qué hace:**
Elimina el usuario ``undar_user`` de MySQL y limpia los privilegios.

---

🧩 10. Desinstalar plugin
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    tutor undar-examen uninstall

**Qué hace:**

1. Elimina el montaje ``./frontend-app-authoring``.
2. Ejecuta ``remove-user`` para eliminar el usuario de MySQL.

---

⚙️ Requisitos
--------------

- `Tutor <https://docs.tutor.edly.io>`_ instalado y configurado.
- Docker y Docker Compose funcionando.
- Git disponible en el sistema.
- Acceso a los repositorios de UNDAR.

---

🧑‍💻 Consejos
--------------

Puedes ejecutar los comandos con ``-h`` para ver las opciones disponibles:

.. code-block:: bash

    tutor undar-examen -h

---

🪪 Licencia
-----------

Este software está licenciado bajo los términos de **AGPLv3**.
