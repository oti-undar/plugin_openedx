import os
import subprocess
from glob import glob

import click
import importlib_resources
from tutor import hooks

from .__about__ import __version__

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

@undar_examen.command(name="start-authoring")
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
def start_authoring(repo: str, dir: str):
    """Clona, monta y arranca el entorno de authoring."""
    # 1. Clonar
    if not os.path.isdir(dir):
        # Si la carpeta no existe, clona el repositorio y luego hace checkout de la etiqueta
        subprocess.check_call(["git", "clone", "--branch", "open-release/sumac.2", repo, dir])
        click.echo("✅ Repo Clonado y Rama/Tag open-release/sumac.2 seleccionada")
    else:
        # Si la carpeta existe, hace un pull para actualizar y luego hace checkout de la etiqueta
        subprocess.check_call(["git", "-C", dir, "fetch", "--all"])
        subprocess.check_call(["git", "-C", dir, "checkout", "open-release/sumac.2"])
        subprocess.check_call(["git", "-C", dir, "pull"])
        click.echo("✅ Repo Actualizado y Rama/Tag open-release/sumac.2 seleccionada")
    # 2. Mount
    subprocess.check_call(["tutor", "mounts", "add", f"./{dir}"])
    # 3. Stop
    subprocess.check_call(["tutor", "local", "stop"])
    # 4. Build
    subprocess.check_call(["tutor", "images", "build", "mfe"])
    # 5. Start en background
    subprocess.check_call(["tutor", "local", "start", "-d"])
    click.echo("Entorno de authoring levantado ✅")

@undar_examen.command(name="remove-mount")
def remove_mount():
    """Elimina el montaje al desinstalar o deshabilitar el plugin."""
    # Asegúrate de quitar el montaje
    subprocess.check_call(["tutor", "mounts", "remove", "./frontend-app-authoring"])
    click.echo("Montaje removido ✅")

# Llama a la función remove_mount si se deshabilita o desinstala el plugin
hooks.Filters.CLI_COMMANDS.add_item(undar_examen)