# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Modulo_De_Monitoreo', '0002_auto_20150122_0009'),
    ]

    operations = [
        migrations.RenameField(
            model_name='datosdenodo',
            old_name='orp_senso',
            new_name='orp',
        ),
    ]
