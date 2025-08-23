import os
import subprocess
from glob import glob
import shutil
import click
import importlib_resources
from tutor import hooks
import stat
import time

from .__about__ import __version__

from tutormfe.hooks import MFE_APPS
@MFE_APPS.add()
def _add_exams_mfe(mfes):
    mfes["examen"] = {
        "repository": "https://github.com/DaveARG/frontend-app-undar-examen.git",
        "port": 3100,
        "version": "main",  # opcional: rama o tag
    }
    mfes["authoring"] = {
        "repository": "https://github.com/DaveARG/frontend-app-authoring.git",
        "port": 2001,
        "version": "open-release/sumac.2",  # opcional: rama o tag
    }
    return mfes

########################################
# CONFIGURATION
########################################

hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        # Add your new settings that have default values here.
        # Each new setting is a pair: (setting_name, default_value).
        # Prefix your setting names with 'UNDAR_EXAMEN_'.
        ("UNDAR_EXAMEN_VERSION", __version__),
    ]
)

hooks.Filters.CONFIG_UNIQUE.add_items(
    [
        # Add settings that don't have a reasonable default for all users here.
        # For instance: passwords, secret keys, etc.
        # Each new setting is a pair: (setting_name, unique_generated_value).
        # Prefix your setting names with 'UNDAR_EXAMEN_'.
        # For example:
        ### ("UNDAR_EXAMEN_SECRET_KEY", "{{ 24|random_string }}"),
    ]
)

hooks.Filters.CONFIG_OVERRIDES.add_items(
    [
        # Danger zone!
        # Add values to override settings from Tutor core or other plugins here.
        # Each override is a pair: (setting_name, new_value). For example:
        ### ("PLATFORM_NAME", "My platform"),
    ]
)


########################################
# INITIALIZATION TASKS
########################################

# To add a custom initialization task, create a bash script template under:
# tutorundar_examen/templates/undar-examen/tasks/
# and then add it to the MY_INIT_TASKS list. Each task is in the format:
# ("<service>", ("<path>", "<to>", "<script>", "<template>"))
MY_INIT_TASKS: list[tuple[str, tuple[str, ...]]] = [
    # For example, to add LMS initialization steps, you could add the script template at:
    # tutorundar_examen/templates/undar-examen/tasks/lms/init.sh
    # And then add the line:
    ### ("lms", ("undar-examen", "tasks", "lms", "init.sh")),
]


# For each task added to MY_INIT_TASKS, we load the task template
# and add it to the CLI_DO_INIT_TASKS filter, which tells Tutor to
# run it as part of the `init` job.
for service, template_path in MY_INIT_TASKS:
    full_path: str = str(
        importlib_resources.files("tutorundar_examen")
        / os.path.join("templates", *template_path)
    )
    with open(full_path, encoding="utf-8") as init_task_file:
        init_task: str = init_task_file.read()
    hooks.Filters.CLI_DO_INIT_TASKS.add_item((service, init_task))


########################################
# DOCKER IMAGE MANAGEMENT
########################################


# Images to be built by `tutor images build`.
# Each item is a quadruple in the form:
#     ("<tutor_image_name>", ("path", "to", "build", "dir"), "<docker_image_tag>", "<build_args>")
hooks.Filters.IMAGES_BUILD.add_items(
    [
        # To build `myimage` with `tutor images build myimage`,
        # you would add a Dockerfile to templates/undar-examen/build/myimage,
        # and then write:
        ### (
        ###     "myimage",
        ###     ("plugins", "undar-examen", "build", "myimage"),
        ###     "docker.io/myimage:{{ UNDAR_EXAMEN_VERSION }}",
        ###     (),
        ### ),
        (
            "hono-app",
            ("plugins", "undar-examen", "build", "hono-app"),  # Ruta relativa dentro del directorio del plugin
            "hono-app:{{ UNDAR_EXAMEN_VERSION }}",
            [],
        ),
    ]
)


# Images to be pulled as part of `tutor images pull`.
# Each item is a pair in the form:
#     ("<tutor_image_name>", "<docker_image_tag>")
hooks.Filters.IMAGES_PULL.add_items(
    [
        # To pull `myimage` with `tutor images pull myimage`, you would write:
        ### (
        ###     "myimage",
        ###     "docker.io/myimage:{{ UNDAR_EXAMEN_VERSION }}",
        ### ),
    ]
)


# Images to be pushed as part of `tutor images push`.
# Each item is a pair in the form:
#     ("<tutor_image_name>", "<docker_image_tag>")
hooks.Filters.IMAGES_PUSH.add_items(
    [
        # To push `myimage` with `tutor images push myimage`, you would write:
        ### (
        ###     "myimage",
        ###     "docker.io/myimage:{{ UNDAR_EXAMEN_VERSION }}",
        ### ),
    ]
)


########################################
# TEMPLATE RENDERING
# (It is safe & recommended to leave
#  this section as-is :)
########################################

hooks.Filters.ENV_TEMPLATE_ROOTS.add_items(
    # Root paths for template files, relative to the project root.
    [
        str(importlib_resources.files("tutorundar_examen") / "templates"),
    ]
)

hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    # For each pair (source_path, destination_path):
    # templates at ``source_path`` (relative to your ENV_TEMPLATE_ROOTS) will be
    # rendered to ``source_path/destination_path`` (relative to your Tutor environment).
    # For example, ``tutorundar_examen/templates/undar-examen/build``
    # will be rendered to ``$(tutor config printroot)/env/plugins/undar-examen/build``.
    [
        ("undar-examen/build", "plugins"),
        ("undar-examen/apps", "plugins"),
    ],
)


########################################
# PATCH LOADING
# (It is safe & recommended to leave
#  this section as-is :)
########################################

# For each file in tutorundar_examen/patches,
# apply a patch based on the file's name and contents.
for path in glob(str(importlib_resources.files("tutorundar_examen") / "patches" / "*")):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))


########################################
# CUSTOM JOBS (a.k.a. "do-commands")
########################################

# A job is a set of tasks, each of which run inside a certain container.
# Jobs are invoked using the `do` command, for example: `tutor local do importdemocourse`.
# A few jobs are built in to Tutor, such as `init` and `createuser`.
# You can also add your own custom jobs:


# To add a custom job, define a Click command that returns a list of tasks,
# where each task is a pair in the form ("<service>", "<shell_command>").
# For example:
### @click.command()
### @click.option("-n", "--name", default="plugin developer")
### def say_hi(name: str) -> list[tuple[str, str]]:
###     """
###     An example job that just prints 'hello' from within both LMS and CMS.
###     """
###     return [
###         ("lms", f"echo 'Hello from LMS, {name}!'"),
###         ("cms", f"echo 'Hello from CMS, {name}!'"),
###     ]


# Then, add the command function to CLI_DO_COMMANDS:
## hooks.Filters.CLI_DO_COMMANDS.add_item(say_hi)

# Now, you can run your job like this:
#   $ tutor local do say-hi --name="Arturo Rodas"


#######################################
# CUSTOM CLI COMMANDS
#######################################

@click.group(name="undar-examen")
def undar_examen():
    """Comandos para UNDAR_EXAMEN."""
    pass

@undar_examen.command(name="init-authoring")
@click.option(
    "--repo",
    default="https://github.com/DaveARG/frontend-app-authoring.git",
    help="URL del repositorio a clonar",
)
@click.option(
    "--dir",
    default="frontend-app-authoring",
    help="Carpeta destino para el clone",
)
def init_authoring(repo: str, dir: str):
    """Clona, monta y arranca el entorno de authoring."""
    # 1. Clonar
    if not os.path.isdir(dir):
        # Si la carpeta no existe, clona el repositorio y luego hace checkout de la etiqueta
        subprocess.check_call(["git", "clone", "--branch", "open-release/sumac.2", repo, dir])
        click.echo("✅ Repo Authoring Clonado y Rama/Tag open-release/sumac.2 seleccionada")
    else:
        # Si la carpeta existe, hace un pull para actualizar y luego hace checkout de la etiqueta
        subprocess.check_call(["git", "-C", dir, "fetch", "--all"])
        subprocess.check_call(["git", "-C", dir, "checkout", "open-release/sumac.2"])
        subprocess.check_call(["git", "-C", dir, "pull"])
        click.echo("✅ Repo Authoring Actualizado y Rama/Tag open-release/sumac.2 seleccionada")
    # 2. Mount
    subprocess.check_call(["tutor", "mounts", "add", f"./{dir}"])
    # 3. Stop
    subprocess.check_call(["tutor", "local", "stop"])
    # 4. Build
    subprocess.check_call(["tutor", "images", "build", "mfe"])
    # 5. Start en background
    subprocess.check_call(["tutor", "local", "start", "-d"])
    click.echo("Entorno de authoring levantado ✅")

@undar_examen.command(name="init-examen")
def init_examen():
    """Clona, monta y arranca el entorno de examen."""
    # 3. Stop
    subprocess.check_call(["tutor", "local", "stop"])
    # 4. Build
    subprocess.check_call(["tutor", "images", "build", "mfe", "--no-cache"])
    # 5. Start en background
    subprocess.check_call(["tutor", "local", "start", "-d"])
    click.echo("Entorno de examen levantado ✅")

def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)
@undar_examen.command(name="init-hono")
@click.option(
    "--repo",
    default="https://github.com/DaveARG/hono-app.git",
    help="URL del repositorio a clonar",
)
@click.option(
    "--dir",
    default="hono-app",
    help="Carpeta destino para el clone",
)
def init_hono(repo: str, dir: str):
    """Clona, monta y arranca el entorno de hono-app."""
    # 1. Clonar
    if not os.path.isdir(dir):
        # Si la carpeta no existe, clona el repositorio y luego hace checkout de la etiqueta
        subprocess.check_call(["git", "clone", "--branch", "master", repo, dir])
        click.echo("✅ Repo hono-app Clonado y Rama/Tag master seleccionada")
    else:
        # Si la carpeta existe, hace un pull para actualizar y luego hace checkout de la etiqueta
        subprocess.check_call(["git", "-C", dir, "fetch", "--all"])
        subprocess.check_call(["git", "-C", dir, "checkout", "master"])
        subprocess.check_call(["git", "-C", dir, "pull"])
        click.echo("✅ Repo hono-app Actualizado y Rama/Tag master seleccionada")
    
    # 2. Obtener la ruta del entorno de Tutor
    result = subprocess.run(
        ["tutor", "config", "printroot"],
        stdout=subprocess.PIPE,
        check=True,
    )
    tutor_root = result.stdout.decode("utf-8").strip()
    
    # 2.5. Copiar código al contexto de build
    plugin_build_path = os.path.join(tutor_root, "env", "plugins", "undar-examen", "build", "hono-app")
    if os.path.exists(plugin_build_path):
        shutil.rmtree(plugin_build_path, onerror=remove_readonly)
    
    # Asegurarnos de que copiamos todo el contenido del repo
    shutil.copytree(dir, plugin_build_path)
    click.echo(f"📦 Código copiado desde {dir} al contexto de build: {plugin_build_path}")
    
    # 3. Stop
    subprocess.check_call(["tutor", "local", "stop"])
    # 4. Build
    subprocess.check_call(["tutor", "images", "build", "hono-app"])
    click.echo("✅ Build de hono-app completado")
    # 4.1. Eliminar contenedor hono-app-container si existe
    subprocess.check_call(["docker", "rm", "-f", "hono-app-container"])
    click.echo("✅ Contenedor hono-app-container eliminado")
    # 4.2. Arrancar el contenedor
    subprocess.check_call([
        "docker", "run", "-d", "--name", "hono-app-container",
        "-p", "3000:3000",
        "-e", "DATABASE_URL=mysql://mi_usuario:mi_contraseña@tutor_local-mysql-1:3306/mi_nueva_bd",
        "hono-app:19.0.3"
    ])
    click.echo("✅ Contenedor hono-app-container arrancado")
    # 4.3. Conectar el contenedor al network tutor_default
    subprocess.check_call(["docker", "network", "connect", "tutor_local_default", "hono-app-container"])
    click.echo("✅ Contenedor hono-app-container conectado al network tutor_default")
    # 5. Start en background
    subprocess.check_call(["tutor", "local", "start", "-d"])
    click.echo("✅ Entorno de hono-app levantado")
    
    # Esperar a que MySQL esté disponible
    click.echo("Esperando a que MySQL esté disponible...")
    max_retries = 20
    retry_interval = 3  # segundos
    for i in range(max_retries):
        try:
            # Prueba la conexión al contenedor MySQL
            result = subprocess.run(
                ["docker", "exec", "tutor_local-mysql-1", "mysqladmin", "ping", "-h", "localhost", "-u", "root", "--silent"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False
            )
            if result.returncode == 0:
                click.echo("✅ MySQL está disponible")
                break
        except Exception as e:
            pass
        click.echo(f"Esperando a MySQL... intento {i+1}/{max_retries}")
        time.sleep(retry_interval)
        if i == max_retries - 1:
            click.echo("❌ No se pudo establecer conexión con MySQL después de varios intentos")
            return

    # 6. Ejecutar migraciones y seed dentro del contenedor
    subprocess.check_call([
        "docker", "exec", "hono-app-container",
        "sh", "-c",
        "npm run migrate:fresh:linux"
    ])
    click.echo("✅ Migraciones y seeders ejecutados dentro del contenedor")

@undar_examen.command(name="initdb")
def initdb():
    """Inicializa la base de datos con el usuario y contraseña del entorno."""
    import json

    # Obtener la contraseña root de MySQL desde la configuración de Tutor
    result = subprocess.run(
        ["tutor", "config", "printvalue", "MYSQL_ROOT_PASSWORD"],
        stdout=subprocess.PIPE,
        check=True,
    )
    mysql_root_password = result.stdout.decode("utf-8").strip()

    comandos = [
        "CREATE DATABASE IF NOT EXISTS mi_nueva_bd;",
        "CREATE USER IF NOT EXISTS 'mi_usuario'@'%' IDENTIFIED BY 'mi_contraseña';",
        "GRANT ALL PRIVILEGES ON *.* TO 'mi_usuario'@'%';",
        "FLUSH PRIVILEGES;"
    ]

    for comando in comandos:
        subprocess.run([
            "tutor", "local", "exec", "mysql", "--",
            "mysql", "-u", "root", f"-p{mysql_root_password}", "-e", comando
        ], check=True)

    click.echo("Base de datos inicializada ✅")

@undar_examen.command(name="uninstall")
def uninstall():
    """Elimina el montaje al desinstalar o deshabilitar el plugin."""
    # Asegúrate de quitar el montaje
    subprocess.check_call(["tutor", "mounts", "remove", "./frontend-app-authoring"])
    click.echo("Montaje removido ✅")

# Llama a la función remove_mount si se deshabilita o desinstala el plugin
hooks.Filters.CLI_COMMANDS.add_item(undar_examen)