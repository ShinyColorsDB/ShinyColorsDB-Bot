from peewee import *
from playhouse.pool import PooledMySQLDatabase
from playhouse.shortcuts import ThreadSafeDatabaseMetadata
from multiprocessing import cpu_count as cpuCount

import os

db = PooledMySQLDatabase(os.environ.get('DATABASE'), max_connections=3*cpuCount(), **{
    'charset': 'utf8', 'sql_mode': 'PIPES_AS_CONCAT', 'use_unicode': True, 'host': os.environ.get('SERVER'), 'user': os.environ.get('USERNAME'), 'password': os.environ.get('PASSWORD')})

class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = db
        model_metadata_class = ThreadSafeDatabaseMetadata
        print("Database connected")


class ScdbAssetVersion(BaseModel):
    asset_encrypted_path = TextField(column_name='AssetEncryptedPath')
    asset_exist = IntegerField(column_name='AssetExist')
    asset_index = AutoField(column_name='AssetIndex')
    asset_path = TextField(column_name='AssetPath')
    asset_chunk = IntegerField(column_name='AssetChunk')
    asset_version = IntegerField(column_name='AssetVersion')

    class Meta:
        table_name = 'SCDB_AssetVersion'


class ScdbUnits(BaseModel):
    color1 = TextField(column_name='Color1')
    color2 = TextField(column_name='Color2')
    unit_hiragana = TextField(column_name='UnitHiragana')
    unit_id = AutoField(column_name='UnitID')
    unit_name = TextField(column_name='UnitName')
    unit_pv = TextField(column_name='UnitPV')

    class Meta:
        table_name = 'SCDB_Units'


class ScdbIdols(BaseModel):
    age = IntegerField(column_name='Age')
    birth_place = TextField(column_name='BirthPlace')
    birthday = TextField(column_name='Birthday')
    blood_type = TextField(column_name='BloodType')
    cv = TextField(column_name='CV')
    color1 = TextField(column_name='Color1')
    color2 = TextField(column_name='Color2')
    height = IntegerField(column_name='Height')
    hiragana = TextField(column_name='Hiragana')
    hirameki = TextField(column_name='Hirameki')
    idol_hash = TextField(column_name='IdolHash')
    idol_id = AutoField(column_name='IdolID')
    idol_name = CharField(column_name='IdolName', index=True)
    interest = TextField(column_name='Interest')
    nick_name = TextField(column_name='NickName')
    pre_cv = TextField(column_name='PreCV', null=True)
    special_skill = TextField(column_name='SpecialSkill')
    star_sign = TextField(column_name='StarSign')
    three_size = TextField(column_name='ThreeSize')
    unit = ForeignKeyField(column_name='UnitID',
                           field='unit_id', model=ScdbUnits)
    used_hand = TextField(column_name='UsedHand')
    weight = IntegerField(column_name='Weight')

    class Meta:
        table_name = 'SCDB_Idols'


class ScdbCardList(BaseModel):
    big_pic1 = TextField(column_name='BigPic1', null=True)
    big_pic2 = TextField(column_name='BigPic2', null=True)
    card_hash = TextField(column_name='CardHash', null=True)
    card_index = AutoField(column_name='CardIndex')
    card_name = TextField(column_name='CardName')
    card_type = TextField(column_name='CardType')
    card_uuid = TextField(column_name='CardUUID')
    enza_id = BigIntegerField(column_name='EnzaID', index=True)
    get_method = TextField(column_name='GetMethod', null=True)
    idea_mark = TextField(column_name='IdeaMark', null=True)
    idol = ForeignKeyField(column_name='IdolID',
                           field='idol_id', model=ScdbIdols)
    release_date = DateField(column_name='ReleaseDate', null=True)
    sml_pic = TextField(column_name='SmlPic', null=True)

    class Meta:
        table_name = 'SCDB_CardList'
