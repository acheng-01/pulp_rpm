# Generated by Django 3.2.15 on 2022-08-29 16:33

from django.db import migrations, models, transaction

import ast
import logging
import yaml


logger = logging.getLogger(__name__)


def populate_new_fields(apps, schema_editor):
    """Populate new fields of modulemd."""
    Modulemd = apps.get_model("rpm", "Modulemd")
    ModulemdDefaults = apps.get_model("rpm", "ModulemdDefaults")
    modules_to_update = []

    # Fix issue #2786 if already tried to update to 3.18.1
    modulemds_to_update = []
    for modulemd in Modulemd.objects.filter(snippet__startswith="b\'---"):
        modulemd.snippet = ast.literal_eval(modulemd.snippet).decode("utf8")
        modulemds_to_update.append(modulemd)
    Modulemd.objects.bulk_update(modulemds_to_update, ["snippet"])

    # Same issue (#2786) has happened to modulemd defaults
    modulemd_defaults_to_update = []
    for default in ModulemdDefaults.objects.filter(snippet__startswith="b\'---"):
        default.snippet = ast.literal_eval(default.snippet).decode("utf8")
        modulemd_defaults_to_update.append(default)
    ModulemdDefaults.objects.bulk_update(modulemd_defaults_to_update, ["snippet"])

    for modulemd in Modulemd.objects.filter(profiles={}):
        try:
            modulemd_dict = yaml.safe_load(modulemd.snippet)
            modulemd.profiles = modulemd_dict["data"]["profiles"]
            modulemd.description = modulemd_dict["data"]["description"]
            modules_to_update.append(modulemd)
        except ValueError as err:
            # Due to issue #2735 it could happen that snippet will be empty
            # https://github.com/pulp/pulp_rpm/issues/2735
            logger.warning(
                "Modulemd {}-{}-{} cannot populate new fields."
                "So it will miss the info about profiles and its description.".format(
                    modulemd.name, modulemd.stream, modulemd.version
                )
            )

    Modulemd.objects.bulk_update(modules_to_update, ["profiles", "description"])


class Migration(migrations.Migration):

    dependencies = [
        ("rpm", "0044_noartifact_modules"),
    ]

    operations = [
        migrations.AddField(
            model_name="modulemd",
            name="description",
            field=models.TextField(default="Description"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="modulemd",
            name="profiles",
            field=models.JSONField(default=dict),
        ),
        migrations.RunPython(populate_new_fields),
    ]