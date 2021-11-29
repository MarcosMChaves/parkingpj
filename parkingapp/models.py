# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from datetime import datetime, timedelta
import time
import random

from .config import LETRAS, DÍGITOS

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Estacionamento(models.Model):
    id_estacionamento = models.AutoField(primary_key=True)
    razão_social_estacionamento = models.CharField(max_length=100)
    nome_fantasia_estacionamento = models.CharField(unique=True, max_length=25)
    cnpj_estacionamento = models.CharField(unique=True, max_length=15)
    gratuidade_estacionamento = models.TimeField()
    fração_estacionamento = models.TimeField()

    class Meta:
        managed = False
        db_table = 'estacionamento'

    def __str__(self):
        return self.nome_fantasia_estacionamento

class Estadia(models.Model):
    id_estadia = models.AutoField(primary_key=True)
    fk_vaga = models.ForeignKey('Vaga', models.DO_NOTHING, db_column='fk_vaga')
    fk_veículo = models.ForeignKey('Veículo', models.DO_NOTHING, db_column='fk_veículo')
    data_hora_entrada = models.DateTimeField()
    data_hora_saída = models.DateTimeField()
    valor_estadia = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'estadia'

    def __str__(self):
        return self.fk_vaga.fk_área.nome_área + '-' + self.fk_vaga.nome_vaga

class Fabricante(models.Model):
    id_fabricante = models.AutoField(primary_key=True)
    nome_fantasia_fabricante = models.CharField(unique=True, max_length=25)

    class Meta:
        managed = False
        db_table = 'fabricante'

    def __str__(self):
        return self.nome_fantasia_fabricante.upper()

class Modelo(models.Model):
    id_modelo = models.AutoField(primary_key=True)
    nome_modelo = models.CharField(unique=True, max_length=25)
    fk_fabricante = models.ForeignKey(Fabricante, models.DO_NOTHING, db_column='fk_fabricante')
    fk_porte = models.ForeignKey('Porte', models.DO_NOTHING, db_column='fk_porte')

    class Meta:
        ordering = ['nome_modelo']
        managed = False
        db_table = 'modelo'

    def __str__(self):
        return self.fk_fabricante.nome_fantasia_fabricante.upper() + " " + self.nome_modelo

class Porte(models.Model):
    id_porte = models.AutoField(primary_key=True)
    nome_porte = models.CharField(unique=True, max_length=15)
    sigla_porte = models.CharField(unique=True, max_length=2)
    valor_hora = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'porte'

    def __str__(self):
        return self.nome_porte

#OVERRIDE save METHOD TO ENFORCE UPPERCASE TO sigla_porte
    def save(self, *args, **kwargs):
        self.sigla_porte = self.sigla_porte.upper()
        return super(Porte, self).save(*args, **kwargs)

class Vaga(models.Model):
    id_vaga = models.AutoField(primary_key=True)
    nome_vaga = models.CharField(unique=True, max_length=10)
    fk_área = models.ForeignKey('área', models.DO_NOTHING, db_column='fk_área')

    class Meta:
        managed = False
        db_table = 'vaga'

    def __str__(self):
        return self.fk_área.nome_área + '-' + self.nome_vaga

class Veículo(models.Model):
    id_veículo = models.AutoField(primary_key=True)
    chapa_veículo = models.CharField(unique=True, max_length=7)
    fk_modelo = models.ForeignKey(Modelo, models.DO_NOTHING, db_column='fk_modelo')

    class Meta:
        managed = False
        db_table = 'veículo'

#OVERRIDE save METHOD TO ENFORCE UPPERCASE TO chapa_veículo
    def save(self, *args, **kwargs):
        self.chapa_veículo = self.chapa_veículo.upper()
        return super(Veículo, self).save(*args, **kwargs)

    def __str__(self):
        return self.chapa_veículo

class Área(models.Model):
    id_área = models.AutoField(primary_key=True)
    nome_área = models.CharField(unique=True, max_length=10)
    fk_estacionamento = models.ForeignKey(Estacionamento, models.DO_NOTHING, db_column='fk_estacionamento')

    class Meta:
        managed = False
        db_table = 'área'

    def __str__(self):
        return self.nome_área

class Ocupação(models.Model):
    id = models.BigIntegerField(primary_key=True)
    id_vaga = models.IntegerField('id_vaga')
    nome_vaga = models.CharField('nome_vaga', max_length=10)
    nome_área = models.CharField('nome_área', max_length=10)
    chapa_veículo = models.CharField('chapa_veículo', max_length=7)
    sigla_porte = models.CharField('sigla_porte', max_length=2)
    id_estadia = models.IntegerField('id_estadia')
    gratuidade = models.TimeField()
    fração = models.TimeField()
    data_hora_entrada = models.DateTimeField()
    data_hora_saída = models.DateTimeField()
    duração_estimada = models.BigIntegerField('ocupação_estimada')

    class Meta:
        managed = False
        db_table = 'ocupação'

    def estadia_gratuita(self):
        (h, m, s) = f"{self.gratuidade}".split(':')
        gratuidade = int(h) * 3600 + int(m) * 60 + int(s)
        return self.duração_estimada <= gratuidade

    def __str__(self):
        return self.nome_área + '-' + self.nome_vaga

class Ocupada(models.Model):
    id_estadia = models.BigIntegerField(primary_key=True)
    fk_vaga = models.IntegerField('fk_vaga')
    fk_veículo = models.IntegerField('fk_veículo')
    sigla_porte = models.CharField('sigla_porte', max_length=2)
    data_hora_entrada = models.DateTimeField()
    data_hora_saída = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ocupada'

class VeículoDisponível(models.Model):
    id = models.BigIntegerField(primary_key=True)
    id_veículo = models.BigIntegerField()
    chapa_veículo = models.CharField(unique=True, max_length=7)

    class Meta:
        managed = False
        db_table = 'veículodisponível'

class Cliente(models.Model):
    def gerar_cliente(self, veículos, modelos):
        cliente = random.choice([False, True])
        placa = modelo = ''

        if cliente :    #GERAR CLIENTE
            antigo = random.choice([False, True])
            if antigo:  #SELECIONA DE veículo
                veículo = random.choice(veículos)
                placa = veículo.chapa_veículo
            else:       #GERAR PLACA + MODELO
                placa_nova = random.choice([False, True])
                if placa_nova:
                    letra1 = random.choice(LETRAS)
                    letra2 = random.choice(LETRAS)
                    letra3 = random.choice(LETRAS)
                    dígito1 = random.choice(DÍGITOS)
                    letra4 = random.choice(LETRAS)
                    dígito2 = random.choice(DÍGITOS)
                    dígito3 = random.choice(DÍGITOS)
                    placa = letra1 + letra2 + letra3 + dígito1 + letra4 + dígito2 + dígito3 
                else:
                    letra1 = random.choice(LETRAS)
                    letra2 = random.choice(LETRAS)
                    letra3 = random.choice(LETRAS)
                    dígito1 = random.choice(DÍGITOS)
                    dígito2 = random.choice(DÍGITOS)
                    dígito3 = random.choice(DÍGITOS)
                    dígito4 = random.choice(DÍGITOS)
                    placa = letra1 + letra2 + letra3 + dígito1 + dígito2 + dígito3 + dígito4

                modelo_escolhido = random.choice(modelos)
                modelo = modelo_escolhido.nome_modelo

        return placa, modelo