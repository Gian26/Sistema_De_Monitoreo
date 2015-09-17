# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Modulo_De_Monitoreo', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='datosdenodo',
            old_name='orp_sensor',
            new_name='orp_senso',
        ),
    ]
