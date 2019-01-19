import re
import sys
import random
import asyncio
import os

from datetime import datetime
from itertools import cycle


try:
    from discord.ext import commands
    from discord.ext.commands import Bot
    from discord.voice_client import VoiceClient
    from discord import ChannelType
    import discord
except ImportError:
    print("Discord.py がインストールされていません。\nDiscord.pyをインストールしてください。")
    sys.exit(1)

client = Bot(command_prefix=';', pm_help=True)
status=['このBOTはTAOと連動しています！', '::stか::statusしてね！', '役職更新頑張って！']
version=discord.__version__
RE_STATUS = re.compile(r"<@(\d+)>のステータス\nLv: (\d+)", re.MULTILINE)
prefix = '&'

#-------------------------------------------------------------------------------------------------------------------
ROLESSSS = (
    (lambda x: 1 <= x < 100,'TAO level 1'),
    (lambda x: 100 <= x < 1000, 'TAO level 100'),
    (lambda x: 1000 <= x , 'TAO level 1000')
)

#MMO特化型特訓場
ROLE = (
    (lambda x: 1 <= x < 10,'RPG初心者(Lv1以上)'),
    (lambda x: 10 <= x < 25, 'RPG初心者卒業(Lv10以上)'),
    (lambda x: 25 <= x < 50, 'RPG新人(Lv25以上)'),
    (lambda x: 50 <= x < 75,'RPG新人卒業(Lv50以上)'),
    (lambda x: 75 <= x < 100,'RPG下級者・・・？(Lv75以上)'),
    (lambda x: 100 <= x < 125,'RPG下級者(Lv100以上)'),
    (lambda x: 125 <= x < 150,'RPG下級者卒業(Lv125以上)'),
    (lambda x: 150 <= x < 175, 'RPG中級者・・・？(Lv150以上)'),
    (lambda x: 175 <= x < 200, 'RPG中級者(Lv175以上)'),
    (lambda x: 200 <= x < 300, 'RPG中級者卒業(Lv200以上)'),
    (lambda x: 300 <= x < 500, 'RPG上級者・・・？(Lv300以上)'),
    (lambda x: 500 <= x < 750, 'RPG上級者(Lv500以上)'),
    (lambda x: 750 <= x < 1000, 'RPG上級者中間(Lv750以上)'),
    (lambda x: 1000 <= x < 1250, 'RPG上級者卒業(Lv1000以上)'),
    (lambda x: 1250 <= x < 1500, 'RPGチュートリアルスタート(Lv1250以上)'),
    (lambda x: 1500 <= x < 1750, 'RPG廃人計画始動(Lv1500以上)'),
    (lambda x: 1750 <= x < 2000, 'RPGチュートリアル中盤(Lv1750以上)'),
    (lambda x: 2000 <= x < 2250, 'RPG(Lv2000以上)'),
    (lambda x: 2250 <= x < 2500, 'RPGチュートリアル完了(Lv2250以上)'),
    (lambda x: 2500 <= x < 2750,'RPGエンジョイ勢(Lv2500以上)'),
    (lambda x: 2750 <= x < 3000, 'RPG終盤(Lv2750以上)'),
    (lambda x: 3000 <= x < 3250, 'RPG廃人の仲間入り(Lv3000以上)'),
    (lambda x: 3250 <= x < 3500,'RPGガチ勢(Lv3250以上)'),
    (lambda x: 3500 <= x < 3750,'RPG=End(Lv3500以上)'),
    (lambda x: 3750 <= x < 4000,'RPG第二章開幕(Lv3750以上)'),
    (lambda x: 4000 <= x < 4250,'RPG強くてニューゲーム(Lv4000以上)'),
    (lambda x: 4250 <= x ,'RPG最初のレベル上げ(Lv4250以上)'),
)

#のんきなMMO&miner&tao&uuuレベル上げ場
ROLE_MAP = (
    (lambda x: 1 <= x < 5, 'Lv1　RPGをよく知らない人'),
    (lambda x: 5 <= x < 10, 'Lv5　初心者'),
    (lambda x: 10 <= x < 50, 'Lv10　レベ上げ中の人'),
    (lambda x: 50 <= x < 75, 'Lv50　初心者卒業者？'),
    (lambda x: 75 <= x < 100, 'Lv75　初心者卒業者'),
    (lambda x: 100 <= x < 200,'Lv100　中級者'),
    (lambda x: 200 <= x < 300, 'lv200　中上級者'),
    (lambda x: 300 <= x < 500, 'Lv300　上級者'),
    (lambda x: 500 <= x < 750, 'Lv500　バウンティハンター'),
    (lambda x: 750 <= x < 1000, 'Lv750　魔界ヲ統ベル者'),
    (lambda x: 1000 <= x < 1250, 'Lv1000　神罰の地上代行者'),
    (lambda x: 1250 <= x < 1500, 'Lv1250　魔界の頂点に立つ者'),
    (lambda x: 1500 <= x < 1750, 'Lv1500　魔界の界王'),
    (lambda x: 1750 <= x < 2000, 'Lv1750　破壊神'),
    (lambda x: 2000 <= x < 2250, 'Lv2000　創造神'),
    (lambda x: 2250 <= x < 2500, 'Lv2250　次元を超えし者'),
    (lambda x: 2500 <= x < 2750,'Lv2500　覇者'),
    (lambda x: 2750 <= x < 3000, 'Lv2750　覇者の中でもトップクラス'),
    (lambda x: 3000 <= x < 3250, 'Lv3000　覇者の中でも一番強き者'),
    (lambda x: 3250 <= x < 3500, 'Lv3250　夢からの刺客'),
    (lambda x: 3500 <= x < 3750, 'Lv3500　夢見の王'),
    (lambda x: 3750 <= x < 4000,'Lv3750　闇を切り裂く勇者'),
    (lambda x: 4000 <= x < 4250,'Lv4000　限界突破'),
    (lambda x: 4250 <= x < 4500,'Lv4250　MMOくんの友達'),
    (lambda x: 4500 <= x < 4750,'Lv4500 　MMOくんの親友'),
    (lambda x: 4750 <= x < 5000,'Lv4750　 MMOくんの相棒'),
    (lambda x: 5000 <= x < 5250,'Lv5000　冥界意志 The_will_of_Hades'),
    (lambda x: 5250 <= x < 5500,'Lv5250　断罪者'),
    (lambda x: 5500 <= x < 5750,'Lv5500 青き地獄'),
    (lambda x: 5750 <= x < 6000,'Lv5750　血の空'),
    (lambda x: 6000 <= x < 6250,'Lv6000 神を超越した者'),
    (lambda x: 6250 <= x < 6500,'Lv6250 第一形態'),
    (lambda x: 6500 <= x < 6750,'Lv6500 第二形態'),
    (lambda x: 6750 <= x < 7000,'Lv6750 第三形態'),
    (lambda x: 7000 <= x < 7250,'Lv7000 虚数形態'),
    (lambda x: 7250 <= x < 7500,'Lv7250　次元を壊し者'),
    (lambda x: 7500 <= x < 7750,'Lv7500 飽きてきた人'),
    (lambda x: 7750 <= x < 8000,'Lv7750 作業厨'),
    (lambda x: 8000 <= x < 8250,'Lv8000 お遊びはおしまいだ'),
    (lambda x: 8250 <= x < 8500,'Lv8250 銀河を喰らいし者'),
    (lambda x: 8500 <= x < 8750,'Lv8500 伝説の勇者'),
    (lambda x: 8750 <= x < 9000,'Lv8750 永遠とmmoをやり続ける者'),
    (lambda x: 9000 <= x < 9250,'Lv9000 古代勇者　-Ancient-'),
    (lambda x: 9250 <= x < 9500,'Lv9250 英雄'),
    (lambda x: 9500 <= x < 9750,'Lv9500 地獄のサバイバー'),
    (lambda x: 9750 <= x < 10000,'Lv9750 バグ使っただろ^^'),
    (lambda x: 10000 <= x < 30000,'Lv10000　夢を帯し者'),
    (lambda x: 30000 <= x < 50000,'Lv30000　真・超上位破壊神の領域'),
    (lambda x: 50000 <= x < 100000,'Lv50000 無限の可能性'),
    (lambda x: 100000 <= x < 200000,'Lv100000　一閃の稲妻'),
    (lambda x: 200000 <= x < 300000,'Lv200000 騎虎の元帥'),
    (lambda x: 300000 <= x < 400000,'Lv300000　†「怪竜」・八岐大蛇　†'),
    (lambda x: 400000 <= x < 500000,'Lv400000　憎悪と絶望の堕天使'),
    (lambda x: 500000 <= x ,'Lv500000　危険な香り'),
)
#のんきなMMO&miner&tao&uuuレベル上げ場
ROLES = (
    (lambda x: 1 <= x < 30,'Lv1 [tao]taoをよく知らない人'),
    (lambda x: 30 <= x < 50, 'Lv30 [tao]初心者卒業！'),
    (lambda x: 50 <= x < 75,'Lv50 [tao]中級者！'),
    (lambda x: 75 <= x < 100,'Lv75　初心者卒業者'),
    (lambda x: 100 <= x < 200,'Lv100 [tao]中級者卒業！'),
    (lambda x: 200 <= x < 300, 'Lv200 [tao]上級者！'),
    (lambda x: 300 <= x < 400, 'Lv300 [tao]上級者卒業！'),
    (lambda x: 400 <= x < 500,'Lv400 [tao]モンスターハンター！'),
    (lambda x: 500 <= x < 750, 'Lv500 [tao]チュートリアル卒業！'),
    (lambda x: 750 <= x < 1000, 'Lv750 [tao]　アイ♡TAO!'),
    (lambda x: 1000 <= x < 1250, 'Lv1000[tao] taoマスターへの道！'),
    (lambda x: 1250 <= x < 1500, 'Lv1250 [tao]マスターへの道～第一関門～'),
    (lambda x: 1500 <= x < 1750, 'Lv1500 [tao]マスターへの道 ～第二関門～'),
    (lambda x: 1750 <= x < 2000, 'Lv1750 [tao]マスター！'),
    (lambda x: 2000 <= x < 2250, 'Lv2000[tao] 大台突破'),
    (lambda x: 2250 <= x < 2500, 'Lv2250[tao] ドハマリ。'),
    (lambda x: 2500 <= x < 2750,'Lv2500[tao] taoを極めし者'),
    (lambda x: 2750 <= x < 3000, 'Lv2750[tao]ヒーロー'),
    (lambda x: 3000 <= x < 3250, 'Lv3000 [tao]ヒーロー卒業！'),
    (lambda x: 3250 <= x < 3500,'Lv3250 [tao]スーパーヒーローへの道！'),
    (lambda x: 3500 <= x < 3750,'Lv3500 [tao]暇人'),
    (lambda x: 3750 <= x < 4000,'Lv3750 [tao]魔王の配下'),
    (lambda x: 4000 <= x < 4250,'Lv4000 [tao]魔王'),
    (lambda x: 4250 <= x < 4500,'Lv4250 [tao]～勇者TAO～'),
    (lambda x: 4500 <= x < 4750,'Lv4500 [tao]四天王最弱'),
    (lambda x: 4750 <= x < 5000,'Lv4750 [tao]四天王の中で３番目に強き者'),
    (lambda x: 5000 <= x < 5250,'Lv5000 [tao]四天王の中で２番目に強き者'),
    (lambda x: 5250 <= x < 5500,'Lv5250 [tao]四天王最強'),
    (lambda x: 5500 <= x < 5750,'lv5500 [tao]殿堂入りした勇者'),
    (lambda x: 5750 <= x < 6000,'Lv5750 [tao]MMO神道・極'),
    (lambda x: 6000 <= x,'Lv6000 [tao]MMO神道・覇')
)

#L会議-TAO部門
ROLESS = (
    (lambda x: 100 <= x < 200,'100↑'),
    (lambda x: 200 <= x < 300, '200↑'),
    (lambda x: 300 <= x < 400,'300↑'),
    (lambda x: 400 <= x < 500,'400↑'),
    (lambda x: 500 <= x < 600,'500↑'),
    (lambda x: 600 <= x < 700, '600↑'),
    (lambda x: 700 <= x < 800, '700↑'),
    (lambda x: 800 <= x < 900,'800↑'),
    (lambda x: 900 <= x < 1000, '900↑'),
    (lambda x: 1000 <= x < 1500, '1000↑'),
    (lambda x: 1500 <= x < 2000, '1500↑'),
    (lambda x: 2000 <= x < 3000, '2000↑'),
    (lambda x: 3000 <= x < 4000, '3000↑'),
    (lambda x: 4000 <= x < 5000,'4000↑'),
    (lambda x: 5000 <= x,'5000↑')
)

ROLESSS = (
    (lambda x: 1 <= x < 5,'[TAOLv1]ラピス初心者'),
    (lambda x: 5 <= x < 10,'[TAOLv5]ラピス中級者'),
    (lambda x: 10 <= x < 20,'[TAOLv10]ラピスキケロ'),
    (lambda x: 20 <= x < 50,'[TAOLv20]ラピス中級者+'),
    (lambda x: 50 <= x < 80,'[TAOLv50]ラピス上級者'),
    (lambda x: 80 <= x < 120,'[TAOLv80]ラピス上級者+'),
    (lambda x: 120 <= x < 180,'[TAOLv120]ラピスデュラハン'),
    (lambda x: 180 <= x < 250,'[TAOLv180]ラピス超級者'),
    (lambda x: 250 <= x < 300,'[TAOLv250]風雷ラピス'),
    (lambda x: 300 <= x < 500,'[TAOLv300]ラピス超級者+'),
    (lambda x: 500 <= x < 600,'[TAOLv500]ラピス卒業'),
    (lambda x: 600 <= x < 750,'[TAOLv600]ルビー初心者'),
    (lambda x: 750 <= x < 800,'[TAOLv750]ルビー中級者'),
    (lambda x: 800 <= x < 900,'[TAOLv800]ルビーデュラハン'),
    (lambda x: 900 <= x < 950,'[TAOLv900]風雷ルビー'),
    (lambda x: 950 <= x < 1000,'[TAOLv950]ルビーマスター'),
    (lambda x: 1000 <= x < 1100,'[TAOLv1000]ルビー卒業'),
    (lambda x: 1100 <= x < 1200,'[TAOLv1100]アクア初心者'),
    (lambda x: 1200 <= x < 1320,'[TAOLv1200]アクア中級者'),
    (lambda x: 1320 <= x < 1400,'[TAOLv1320]アクアデュラハン'),
    (lambda x: 1400 <= x < 1480,'[TAOLv1400]風雷アクア'),
    (lambda x: 1480 <= x < 1560,'[TAOLv1480]アクアマスター'),
    (lambda x: 1560 <= x < 1700,'[TAOLv1560]祟アクア'),
    (lambda x: 1700 <= x < 1800,'[TAOLv1700]アクア卒業'),
    (lambda x: 1800 <= x < 2000,'[TAOLv1800]アンドラ初心者'),
    (lambda x: 2000 <= x < 2200,'[TAOLv2000]アンドラデュラハン'),
    (lambda x: 2200 <= x < 2300,'[TAOLv2200]風雷アンドラ'),
    (lambda x: 2300 <= x < 2400,'[TAOLv2300]祟アンドラ'),
    (lambda x: 2500 <= x < 2600,'[TAOLv2500]アンドラ卒業'),
    (lambda x: 2600 <= x < 2750,'[TAOLv2600]セラフィ初心者'),
    (lambda x: 2750 <= x < 2900,'[TAOLv2750]風雷セラフィ'),
    (lambda x: 2900 <= x < 3000,'[TAOLv2900]銀河最強の戦士・SER'),
    (lambda x: 3000 <= x < 3150,'[TAOLv3000]セラフィ卒業'),
    (lambda x: 3300 <= x < 3500,'[TAOLv3300]ローズ初心者'),
    (lambda x: 3750 <= x < 3900,'[TAOLv3750]銀河最強の戦士・ROS'),
    (lambda x: 3900 <= x < 4000,'[TAOLv3900]真・銀河最強の戦士・ROS'),
    (lambda x: 4000 <= x ,'[TAOLv4000]ローズ卒業'),
)
#-------------------------------------------------------------------------------------------------------------------

#MMO特化型特訓場
ROLE_LEVEL = {
    "RPG初心者(Lv1以上)":1,
    "RPG初心者卒業(Lv10以上)":10,
    "RPG新人(Lv25以上)":25,
    "RPG新人卒業(Lv50以上)": 50,
    "RPG下級者・・・？(Lv75以上)":75,
    "RPG下級者(Lv100以上)": 100,
    "RPG下級者卒業(Lv125以上)": 125,
    "RPG中級者・・・？(Lv150以上)": 150,
    "RPG中級者(Lv175以上)": 175,
    "RPG中級者卒業(Lv200以上)": 200,
    "RPG上級者・・・？(Lv300以上)": 300,
    "RPG上級者(Lv500以上)": 500,
    "RPG上級者中間(Lv750以上)": 750,
    "RPG上級者卒業(Lv1000以上)": 1000,
    "RPGチュートリアルスタート(Lv1250以上)": 1250,
    "RPG廃人計画始動(Lv1500以上)": 1500,
    "RPGチュートリアル中盤(Lv1750以上)": 1750,
    "RPG(Lv2000以上)": 2000,
    "RPGチュートリアル完了(Lv2250以上)": 2250,
    "RPGエンジョイ勢(Lv2500以上)": 2500,
    "RPG終盤(Lv2750以上)": 2750,
    "RPG廃人の仲間入り(Lv3000以上)": 3000,
    "RPGガチ勢(Lv3250以上)": 3250,
    "RPG=End(Lv3500以上)": 3500,
    "RPG第二章開幕(Lv3750以上)": 3750,
    "RPG強くてニューゲーム(Lv4000以上)": 4000,
    "RPG最初のレベル上げ(Lv4250以上)": 4250,
}

#のんきなMMO&miner&tao&uuuレベル上げ場
ROLE_LEVELSS = {
    "Lv1　taoをよく知らない人": 1,
    "Lv30　[tao]初心者卒業！": 30,
    "Lv50　[tao]中級者！": 50,
    "Lv100　[tao]中級者卒業！": 100,
    "Lv200　[tao]上級者！": 200,
    "Lv300　[tao]上級者卒業！": 300,
    "Lv400　[tao]モンスターハンター！": 400,
    "Lv500　[tao]チュートリアル卒業！": 500,
    "Lv750　[tao]　アイ♡TAO!": 750,
    "Lv1000　[tao] taoマスターへの道！": 1000,
    "Lv1250　[tao]マスターへの道～第一関門～": 1250,
    "Lv1500　[tao]マスターへの道～第二関門～": 1500,
    "Lv1750　[tao] taoマスター！": 1750,
    "Lv2000　[tao] 大台突破": 2000,
    "Lv2250　[tao]　ドハマリ": 2250,
    "Lv2500　[tao] taoを極めし者": 2500,
    "Lv2750　[tao]ヒーロー": 2750,
    "Lv3000　[tao] ヒーロー卒業！": 3000,
    "Lv3250　[tao]スーパーヒーローへの道！": 3250,
    "Lv3500　[tao]暇人": 3500,
    "Lv3750　[tao]魔王の配下": 3750,
    "Lv4000　[tao]魔王": 4000,
    "Lv4250　[tao]～勇者TAO～": 4250,
    "Lv4500　[tao]四天王最弱": 4500,
    "Lv4750　[tao]四天王の中で3番目に強き者": 4750,
    "Lv5000　[tao]四天王の中で２番目に強き者": 5000,
    "Lv5250　[tao]四天王最強": 5250,
    "Lv5500　[tao]殿堂入りした勇者": 5500,
    "Lv5750　[tao]MMO神道・極": 5750,
    "Lv6000　[tao]MMO神道・覇": 6000,
}
#のんきなMMO&miner&tao&uuuレベル上げ場

ROLE_LEVELS = {
    "Lv1　RPGをよく知らない人":1,
    "Lv5　初心者":5,
    "Lv10　レベ上げ中の人":10,
    "Lv50　初心者卒業者？": 50,
    "Lv75　初心者卒業者":75,
    "Lv100　中級者": 100,
    "lv200　中上級者": 125,
    "Lv300　上級者": 300,
    "Lv500　バウンティハンター": 500,
    "Lv750　魔界ヲ統ベル者": 750,
    "Lv1000　神罰の地上代行者": 1000,
    "Lv1250　魔界の頂点に立つ者": 1250,
    "Lv1500　魔界の界王": 1500,
    "Lv1750　破壊神": 1750,
    "Lv2000　創造神": 2000,
    "Lv2250　次元を超えし者": 2250,
    "Lv2500　覇者": 2500,
    "Lv2750　覇者の中でもトップクラス": 2750,
    "Lv3000　覇者の中でも一番強き者": 3000,
    "Lv3250　夢からの刺客": 3250,
    "Lv3500　夢見の王": 1250,
    "Lv3750　闇を切り裂く勇者": 3750,
    "Lv4250　mmoくんの友達": 4250,
    "Lv4500　mmoくんの親友": 4500,
    "Lv4750　mmoくんの相棒": 4750,
    "Lv5000　冥界意思 The_will_of_Hades": 5000,
    "Lv5250　断罪者": 5250,
    "Lv5500　青き地獄": 5500,
    "Lv5750　血の空": 5750,
    "Lv6000　神を超越した者": 6000,
    "Lv6250　第一形態": 6250,
    "Lv6500　第二形態": 6500,
    "Lv6750　第三形態": 6750,
    "Lv7000　虚数形態": 7000,
    "Lv7250　次元を壊し者": 7250,
    "Lv7500　飽きてきた人": 7500,
    "Lv7750　作業厨": 7750,
    "Lv8000　お遊びはおしまいだ": 8000,
    "Lv8250　銀河を喰らいし者": 8250,
    "Lv8500　伝説の勇者": 8500,
    "Lv8750　永遠にmmoをやりつづける者": 8750,
    "Lv9000　Lv9000 古代勇者　-Ancient-": 9000,
    "Lv9250　英雄": 9250,
    "Lv9500　地獄のサバイバー": 9500,
    "Lv9750　バグ使っただろ^^": 9750,
    "Lv10000　夢を帯し者": 10000,
    "Lv30000　超・上位破壊神の領域": 30000,
    "Lv50000　無限の可能性": 50000,
    "Lv100000　一閃の稲妻": 100000,
    "Lv150000　叡智の戦士": 150000,
    "Lv200000　騎虎の元帥": 200000,
    "Lv300000　†「怪竜」・八岐大蛇　†": 300000,
    "Lv400000　憎悪と絶望の堕天使": 400000,
    "Lv500000　危険な香り": 500000,
}
ROLE_LEVELSSS = {
    "100↑": 100,
    "200↑": 200,
    "300↑": 300,
    "400↑": 400,
    "500↑": 500,
    "600↑": 300,
    "700↑": 700,
    "800↑": 800,
    "900↑": 900,
    "1000↑": 1000,
    "1500↑": 1500,
    "2000↑": 2000,
    "3000↑": 3000,
    "4000↑": 4000,
    "5000↑": 5000,
}

ROLE_LEVELSSSS = {
    "[TAOLv1]ラピス初心者": 1,
    "[TAOLv5]ラピス中級者": 5,
    "[TAOLv10]ラピスキケロ": 10,
    "[TAOLv20]ラピス中級者+": 20,
    "[TAOLv50]ラピス上級者": 50,
    "[TAOLv120]ラピスデュラハン": 80,
    "[TAOLv180]ラピス超級者": 180,
    "[TAOLv250]風雷ラピス": 250,
    "[TAOLv300]ラピス超級者+": 300,
    "[TAOLv500]ラピス卒業": 500,
    "[TAOLv600]ルビー初心者": 600,
    "[TAOLv750]ルビー中級者": 750,
    "[TAOLv800]ルビーデュラハン": 800,
    "[TAOLv900]風雷ルビー": 900,
    "[TAOLv950]ルビーマスター": 950,
    "[TAOLv1000]ルビー卒業": 1000,
    "[TAOLv1100]アクア初心者": 1100,
    "[TAOLv1200]アクア中級者": 1200,
    "[TAOLv1320]アクアデュラハン": 1320,
    "[TAOLv1400]風雷アクア": 1400,
    "[TAOLv1480]アクアマスター": 1480,
    "[TAOLv1560]祟りアクア": 1560,
    "[TAOLv1700]アクア卒業": 1700,
    "[TAOLv1800]アンドラ初心者": 1800,
    "[TAOLv2000]アンドラデュラハン": 2000,
    "[TAOLv2200]風雷アンドラ": 2200,
    "[TAOLv2300]祟アンドラ": 2300,
    "[TAOLv2500]アンドラ卒業": 2500,
    "[TAOLv2600]セラフィ初心者": 2600,
    "[TAOLv2700]風雷セラフィ": 2750,
    "[TAOLv2900]銀河最強の戦士・SER": 2900,
    "[TAOLv3000]セラフィ卒業": 3000,
    "[TAOLv3300]ローズ初心者": 3300,
    "[TAOLv3750]銀河最強の戦士・ROS": 3750,
    "[TAOLv3900]真・銀河最強の戦士・ROS": 3900,
    "[TAOLv4000]ローズ卒業": 4000,
}

ROLE_LEVELSSSSS = {
    "TAO level 1": 1,
    "TAO level 100": 100,
    "TAO level 1000": 1000,
}
#-------------------------------------------------------------------------------------------------------------------

@client.event
async def on_ready():
    up = discord.Color(random.randint(0,0xFFFFFF))
    embed = discord.Embed(
        title="起動しました！",
        description="",
        color=up
    )
    embed.set_author(
        name="役職自動付与BOT"
    )
    embed.set_footer(
        text="起動時刻:" + datetime.now().strftime(" %Y/%m/%d %H:%M:%S")
    )
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/avatars/{0.user.id}/{0.user.avatar}.png?size=1024".format(client)
    )
    embed.set_footer(
        text="現在時刻:" + datetime.now().strftime(" %Y/%m/%d %H:%M:%S")
    )
    embed.add_field(
        name="BOTが再起動しました。",
        value="役職を持っていない方は「役職付与」と打ってください。",
        inline=False
    )
    server = client.get_server('337524390155780107')
    await client.send_message(server.get_channel('535957520666066954'),embed=embed)
    print("起動完了じゃああああああああああああああああああああ")
    memberID = "304932786286886912"
    server = client.get_server('337524390155780107')
    person = discord.Server.get_member(server,memberID)
    up = discord.Color(random.randint(0,0xFFFFFF))
    embed = discord.Embed(
        title="起動しました！",
        description="このBOTはTAOと連動しています",
        color=up
    )
    embed.set_author(
        name="役職自動付与BOT"
    )
    embed.set_footer(
        text="起動時刻:" + datetime.now().strftime(" %Y/%m/%d %H:%M:%S")
    )
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/avatars/{0.user.id}/{0.user.avatar}.png?size=1024".format(client)
    )
    embed.set_footer(
        text="現在時刻:" + datetime.now().strftime(" %Y/%m/%d %H:%M:%S")
    )
    embed.add_field(
        name="このBOTの名前:",
        value=client.user.name,
        inline=False
    )
    embed.add_field(
        name="このBOTのID:",
        value=client.user.id,
        inline=False
    )
    embed.add_field(
        name="BOTが取得してるサーバーの数",
        value=(len(client.servers)),
        inline=False
    )
    embed.add_field(
        name="BOTが取得してるユーザー数",
        value=(len(set(client.get_all_members()))),
        inline=False
    )
    embed.add_field(
        name="BOTが取得してるチャンネル数",
        value=(len([c for c in client.get_all_channels()])),
        inline=False
    )
    embed.add_field(
        name="BOTの招待",
        value="[**ここからお願いします**](<https://discordapp.com/oauth2/authorize?client_id=529149531800076319&permissions=8&scope=bot>)",
        inline=False
    )
    embed.set_footer(
        text="このBOTの作成日: " + client.user.created_at.__format__(' %Y/%m/%d %H:%M:%S')
    )
    await client.send_message(person, embed=embed)
    server = client.get_server('337524390155780107')
    a = await client.send_message(server.get_channel('338151444731658240'),"起動完了じゃあああああああああああああああああああああああ")
    await asyncio.sleep(60)
    await client.delete_message(a)
    return

#-------------------------------------------------------------------------------------------------------------------
@client.event
async def on_server_remove(server):
    await client.send_message(server.owner, "```このBOTをいままでありがとう！\nこのBOTの事はThe.First.Step#3454に言ってね\nもしこのBOTを正常に動かしたいのであれば兄者にDMで言ってください！```")
    up = discord.Color(random.randint(0,0xFFFFFF))
    embed = discord.Embed(
        title=server.name+"鯖がこのBOTをKICKしま   した",
        description="このBOTはTAOと連動しています",
        color=up
    )
    embed.set_author(
        name="役職自動付与BOTをKICKした鯖情報:"
    )
    embed.set_thumbnail(
        url=server.icon_url
    )
    embed.set_footer(
        text="現在時刻:" + datetime.now().strftime(" %Y/%m/%d %H:%M:%S")
    )
    embed.add_field(
        name="鯖名:",
        value=server.name,
        inline=True
    )
    embed.add_field(
        name="サーバーID:",
        value=server.id,
        inline=True
    )
    embed.add_field(
        name="鯖のチャンネル数:",
        value=len(server.channels),
        inline=True
    )
    embed.add_field(
        name="鯖の人数:",
        value=len(server.members),
        inline=True
    )
    embed.add_field(
        name="役職数:",
        value=str(len(server.roles)),
        inline=True
    )
    embed.add_field(
        name="鯖の主の名前:",
        value=server.owner,
        inline=True
    )
    embed.set_footer(
        text="サーバー作成日: " + server.created_at.__format__(' %Y/%m/%d %H:%M:%S')
    )
    server = client.get_server('526274496177635338')
    await client.send_message(server.get_channel('529139075165192192'),embed=embed)


@client.event
async def on_server_join(server):
    await client.send_message(server.owner, "```このBOTを入れてくれてありがとう！\nこのBOTはThe.First.Step#3454が作りました。\nどうぞよろしくお願いします。\nもしこのBOTを正常に動かしたいのであれば兄者にDMで言ってください！```")
    up = discord.Color(random.randint(0,0xFFFFFF))
    embed = discord.Embed(
        title=server.name+"鯖にこのBOTが導入されました",
        description="このBOTはTAOと連動しています",
        color=up
    )
    embed.set_author(
        name="役職自動付与BOTを導入した鯖情報:"
    )
    embed.set_thumbnail(
        url=server.icon_url
    )
    embed.set_footer(
        text="現在時刻:" + datetime.now().strftime(" %Y/%m/%d %H:%M:%S")
    )
    embed.add_field(
        name="鯖名:",
        value=server.name,
        inline=True
    )
    embed.add_field(
        name="サーバーID:",
        value=server.id,
        inline=True
    )
    embed.add_field(
        name="鯖のチャンネル数:",
        value=len(server.channels),
        inline=True
    )
    embed.add_field(
        name="鯖の人数:",
        value=len(server.members),
        inline=True
    )
    embed.add_field(
        name="役職数:",
        value=str(len(server.roles)),
        inline=True
    )
    embed.add_field(
        name="鯖の主の名前:",
        value=server.owner,
        inline=True
    )
    embed.set_footer(
        text="サーバー作成日: " + server.created_at.__format__(' %Y/%m/%d %H:%M:%S')
    )
    server = client.get_server('526274496177635338')
    await client.send_message(server.get_channel('529139075165192192'),embed=embed)

@client.event
async def on_member_join(member):
    if not member.server.id == "337524390155780107":
        return
    if client.user == member:
        return
    await client.send_message(member,
                                    "```ようこそ！\n{}へ！\nこの鯖はMMOくんとTAOくん専門の鯖です！\n今後ともよろしくお願いします！```".format(member.server.name))
    channel = client.get_channel('337860614846283780')
    channels = client.get_channel('528113643330600971')
    channelss = client.get_channel('535079479576625152')
    channelsss = client.get_channel('535957520666066954')
    up = discord.Color(random.randint(0,0xFFFFFF))
    embed = discord.Embed(
        title="よろしくお願いします～",
        description="",
        color=up
    )
    embed.set_author(
        name=member.name + "さんがこの鯖に入りました！"
    )
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(member)
    )
    embed.add_field(
        name="現在の鯖の人数:\n",
        value="{}\n".format(len(member.server.members)),
        inline=False
    )
    embed.add_field(
        name="MMOのステータスを表示させる場合は:",
        value=channel.mention,
        inline=False
    )
    embed.add_field(
        name="TAOのステータスを表示させる場合は:",
        value="{}".format(channels.mention),
        inline=False
    )
    embed.add_field(
        name="ステータスの表示のさせ方",
        value="MMOの場合が!!status\nTAOの場合は::stか::statusです！\n\n{}でTAOのステータスを表示させると\n役職がもらえるよ！".format(channels.mention),
        inline=False
    )
    embed.add_field(
        name="自己紹介よろしくお願いします！",
        value="{}で自己紹介よろしくお願いします～\nテンプレはピン止めしています。".format(channelss.mention),
        inline=False
    )
    server = client.get_server('337524390155780107')
    await client.send_message(server.get_channel('338173860719362060'),embed=embed)
    embed = discord.Embed(
        title="もしこのBOTが起動してなく役職を付与されなかったら...",
        description="",
        color=up
    )
    embed.set_footer(
        text="加入時刻:" + datetime.now().strftime(" %Y/%m/%d %H:%M:%S")
    )
    embed.add_field(
        name="この鯖で発言権限を得るためには『暇人』役職が必要です。",
        value="もしこのBOTが起動していなく\n暇人役職が付与されていない場合は\n{}で『役職付与』と打ってください。".format(channelsss.mention),
        inline=False
    )
    embed.add_field(
        name="レベル役職を付与してほしい場合には...",
        value="{}でステータス表示させてね！\n\n※要注意:このBOTが起動してないと役職を付与してくれません。".format(channels.mention),
        inline=False
    )
    server = client.get_server('337524390155780107')
    await client.send_message(server.get_channel('338173860719362060'),embed=embed)
    role = discord.utils.get(member.server.roles,name="暇人")
    await client.add_roles(member,role)
    servers = client.get_server('337524390155780107')
    await client.send_message(servers.get_channel('338173860719362060'),"{}さんに役職を付与しました。".format(member.mention))


@client.event
async def on_member_remove(member):
    if not member.server.id == "337524390155780107":
        return
    up = discord.Color(random.randint(0,0xFFFFFF))
    embed = discord.Embed(
        title="ありがとうございました！",
        description="",
        color=up
    )
    embed.set_author(
        name=member.name + "さんがこの鯖から退出しました；；"
    )
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(member)
    )
    embed.set_footer(
        text="退出時刻:" + datetime.now().strftime(" %Y/%m/%d %H:%M:%S")
    )
    embed.add_field(
        name="現在の鯖の人数:",
        value=len(member.server.members),
        inline=False
    )
    server = client.get_server('337524390155780107')
    await client.send_message(server.get_channel('338173860719362060'),embed=embed)

async def change_status():
    await client.wait_until_ready()
    msgs=cycle(status)

    while not client.is_closed:
        current_status=next(msgs)
        await client.change_presence(game=discord.Game(name=current_status))
        await asyncio.sleep(30)

#-------------------------------------------------------------------------------------------------------------------

@client.event
async def on_message(message: discord.Message):
    if message.content.find("https://discord.gg/") != -1:
        if message.server.id == "337524390155780107":
            if not message.channel.id == "421954703509946368":
                channel = client.get_channel('421954703509946368')
                await client.delete_message(message)
                await client.send_message(message.channel,
                                          "<@{0}>さん\nもし鯖の宣伝をしたいなら{1}でやってください！\n出来れば時間制限無しの宣伝をお願いします！".format(
                                              message.author.id,channel.mention))
                return

    if message.channel.type == ChannelType.private:
        if not message.author.id == "529149531800076319":
            if not message.author.id == '304932786286886912':
                if not message.author.id == '247671415715790849':
                    await client.send_message(message.channel,"**コマンドはDMでは使うことができません...**")
                    return

    # ログは勝手に送ってくれるようにする
    # BOTのProfileを表示自分のメイン垢かドロキンさんの垢しか反応しない
    if message.content.startswith("役職付与"):
        role = discord.utils.get(message.server.roles,name="暇人")
        if role in message.author.roles:
            await client.send_message(message.channel,
                                      "{}\nあなたはもう既にこの役職を持っています！！".format(message.author.mention))
        else:
            await client.add_roles(message.author,role)
            await client.send_message(message.channel,"{0}さんに『{1}』役職を付与しました。".format(message.author.mention,role))

    if datetime.now().strftime("%H:%M:%S") == datetime.now().strftime("23:00:00"):
        memberID = "304932786286886912"
        server = client.get_server('337524390155780107')
        person = discord.Server.get_member(server,memberID)
        await client.send_message(person,"時間だよ")

    if message.content.startswith(prefix + 'shutdown'):
        if not message.author.id == "304932786286886912":
            await client.send_message(message.channel,"**これは全権限者しか使用できないコマンドです.**")
            return
        a = await client.send_message(message.channel,"シャットダウンします。少しお待ちください。")
        await asyncio.sleep(2)
        b = await client.edit_message(a,"シャットダウンまで残り80%...")
        await asyncio.sleep(2)
        c = await client.edit_message(b,"シャットダウンまで残り60%...")
        await asyncio.sleep(2)
        d = await client.edit_message(c,"シャットダウンまで残り40%...")
        await asyncio.sleep(2)
        e = await client.edit_message(d,"シャットダウンまで残り20%...")
        await asyncio.sleep(2)
        f = await client.edit_message(e,"シャットダウンまで残り0%...")
        await client.delete_message(f)
        await client.send_message(message.channel,'シャットダウンします！\nお疲れさまでした！')
        await client.logout()
        await client.close()

    if message.content.startswith(prefix + 'embed'):
        if not message.author.id == '304932786286886912':
            if not message.author.id == '247671415715790849':
                await client.send_message(message.channel,
                                          "{}さん\nこのコマンドは兄者かドロキンさんしか使えないよ！".format(message.author.mention))
                return
        user = message.author
        if not user.nick == None:  # ニックネーム存在確認
            user_name = user.nick
        else:
            user_name = user.name
        nick = message.server.me
        if not nick.nick == None:
            nick_name = nick.nick
        else:
            nick_name = nick.name
        sayd = message.content[6:]
        embed = discord.Embed(
            title="アナウンスの内容:",
            description="発言者:" + user_name + "#" + message.author.discriminator,
            color=discord.Color.dark_grey(),
            timestamp=message.timestamp
        )
        embed.add_field(
            name="**内容:**",
            value="**" + sayd.replace("sex","**").replace("fuck","****") + "**"
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(message.author)
        )
        embed.set_footer(
            text="発言時刻: "
        )
        embed.set_author(
            name=nick_name,
            icon_url=client.user.avatar_url
        )
        await client.delete_message(message)
        await client.send_message(message.channel,embed=embed)

    if message.content.startswith(prefix + 'profile') and message.content.endswith(prefix + 'profile'):
        if not message.author.id == '304932786286886912':
            if not message.author.id == '247671415715790849':
                await client.send_message(message.channel,"{}このコマンドは兄者かドロキンさんしか使えないよ！".format(message.author.mention))
                return
        up = discord.Color(random.randint(0,0xFFFFFF))
        embed = discord.Embed(
            title="『BOTの詳細』",
            description="このBOTはTAOと連動しています\nこのBOTは兄者(The.First.Step)が制作しています。",
            color=up
        )
        embed.set_author(
            name="役職自動付与BOT情報:"
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/328421178328875009/529157361525456906/1670560676-star-jRPy-1920x1080-MM-100.jpg"
        )
        embed.set_footer(
            text="現在時刻:" + datetime.now().strftime(" %Y/%m/%d %H:%M:%S")
        )
        embed.add_field(
            name="Pythonのバージョン:",
            value="[**3.6.5**](<https://www.python.org/>)",
            inline=False
        )
        embed.add_field(
            name="discord.pyのバージョン:",
            value="[**0.16.12**](<http://discordpy.readthedocs.io/en/latest/index.html>)",
            inline=False
        )
        embed.add_field(
            name="BOTが確認しているユーザー数:",
            value=len(set(client.get_all_members())),
            inline=False
        )
        embed.add_field(
            name="BOTが参加しているサーバー数:",
            value=len(client.servers),
            inline=False
        )
        await client.send_message(message.channel,embed=embed)

    if message.content.startswith('役職一覧') and message.content.endswith('役職一覧'):
        role = "\n".join([r.mention for r in message.author.roles if r.mentionable][::-1])
        up = discord.Color(random.randint(0,0xFFFFFF))
        embed = discord.Embed(
            title="",
            description="",
            color=up
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(message.author)
        )
        embed.add_field(
            name="**{}**に付与されてる役職一覧:".format(message.author),
            value=role,
            inline=False
        )
        await client.send_message(message.channel,embed=embed)
        # -------------------------------------------------------------------------------------------------------------------
    if not message.author.id == '330049154552430593':
        if not message.author.id == '526620171658330112':
            if not message.author.id == '531818623422038026':
                return
                # MMO特化型特訓場
        if len(message.embeds) != 0:
            if message.server.id == "337524390155780107":
                embed = message.embeds[0]
                if embed.get("author") and embed["author"].get("name"):
                    if embed["author"]["name"][-7:] != "のステータス:":
                        return
                    authos = embed["author"]["name"][:-7]
                    for f in embed["fields"]:
                        if f["name"] == "Lv":
                            level = int(f["value"])
                    for f in embed["fields"]:
                        if f["name"] == "プレイヤーランク":
                            levelss = int(f["value"][:-1])
                    channel = client.get_channel('529139075165192192')
                    member = discord.utils.get(message.server.members,display_name=authos)
                    role_name = next((role[1] for role in ROLE if role[0](level)))
                    role = discord.utils.get(message.server.roles,name=role_name)
                    delete_role_names = [role[1] for role in ROLE if not role[0](level)]
                    delete_roles = [discord.utils.get(message.server.roles,name=role_name) for role_name in
                                    delete_role_names]
                    for value in sorted(ROLE_LEVEL.values()):
                        if value > level:
                            next_level = value
                            break
                    else:
                        next_level = '4250'
                        for value in sorted(ROLE_LEVEL.values()):
                            if level > value:
                                await client.send_message(message.channel,
                                                          "```凄い！あなたは今鯖のレベル役職の付与範囲を超えてしまった！\nぜひ運営に役職を追加して貰ってください！\nこの鯖のTAOの最高レベル役職は『{}』です。```".format(
                                                              role_name))
                                return
                    if role in member.roles:
                        await client.send_message(message.channel,
                                                  "次のレベル役職を得るためには{}Lvが必要です！".format(int(next_level - level)))
                        await client.send_message(channel,
                                                  "```・TAO関連 \n発言鯖名:『{0}』 \n\nSTATUSを確認した人:『{1}』 \n現在のレベルは:{2}Lv \nこのひとに適切な役職は『{3}』です。\nこの人はTAOで{4}位です。\n次の役職まで後{5}Lvです！\n\nログ報告時刻:{6}```".format(
                                                      message.server,member,level,role_name,levelss,
                                                      int(next_level - level),
                                                      datetime.now().strftime(" %Y/%m/%d %H:%M:%S")))
                        print("----------------------------------")
                        print(
                            "TAO関連 \n発言鯖名:『{0}』 \nSTATUSを確認した人:『{1}』 \n現在のレベルは:{2}Lv \nこのひとに適切な役職は『{3}』です。\nこの人はTAOで{4}位です。\n次の役職まで後{5}Lvです！\nログ報告時刻:{6}".format(
                                message.server,member,level,role_name,levelss,int(next_level - level),
                                datetime.now().strftime(" %Y/%m/%d %H:%M:%S")))
                        print("----------------------------------")
                        return
                    else:
                        await client.add_roles(member,role)
                        await client.remove_roles(member,*delete_roles)
                        await client.send_message(message.channel,
                                                  "前の役職を削除しました。\n役職名:『{0}』を付与しました。\n次の役職まで後{1}Lvです！".format(
                                                      discord.utils.get(message.server.roles,name=role_name),
                                                      int(next_level - level)))
                        await client.send_message(channel,
                                                  "```・TAO関連 \n発言鯖名:『{0}』 \n\nSTATUSを確認した人:『{1}』 \n現在のレベルは:{2}Lv \nこのひとに適切な役職は『{3}』です。\nこの人はTAOで{4}位です。\n次の役職まで後{5}Lvです！\n\nログ報告時刻:{6}```".format(
                                                      message.server,member,level,role_name,levelss,
                                                      int(next_level - level),
                                                      datetime.now().strftime(" %Y/%m/%d %H:%M:%S")))
                        print("----------------------------------")
                        print(
                            "TAO関連 \n発言鯖名:『{0}』 \nSTATUSを確認した人:『{1}』 \n現在のレベルは:{2}Lv \nこのひとに適切な役職は『{3}』です。\nこの人はTAOで{4}位です。\n次の役職まで後{5}Lvです！\nログ報告時刻:{6}".format(
                                message.server,member,level,role_name,levelss,int(next_level - level),
                                datetime.now().strftime(" %Y/%m/%d %H:%M:%S")))
                        print("----------------------------------")
                        channel = client.get_channel('528458081139556372')
                        mem = str(member)
                        nick = message.server.me
                        if not nick.nick == None:
                            nick_name = nick.nick
                        else:
                            nick_name = nick.name
                        if message.content.find("役職を付与しました"):
                            embedee = discord.Embed(
                                title=mem + "さんにレベル役職を付けました！",
                                description="",
                                color=discord.Color(random.randint(0,0xFFFFFF)),
                                timestamp=message.timestamp
                            )
                            embedee.set_thumbnail(
                                url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(
                                    member)
                            )
                            embedee.add_field(
                                name="役職更新おめでとうです～",
                                value="役職名:『" + role_name + "』"
                            )
                            embedee.set_footer(
                                text="発言時刻 "
                            )
                            embedee.set_author(
                                name=nick_name,
                                icon_url="https://cdn.discordapp.com/attachments/514424761074581504/528492969322479629/1670560676-star-jRPy-1920x1080-MM-100.jpg"
                            )
                            await client.send_message(channel,embed=embedee)
                            return

                # -------------------------------------------------------------------------------------------------------------------
                # のんきなMMO&miner&tao&uuuレベル上げ場
        if len(message.embeds) != 0:
            if message.server.id == "415120414323245057":
                embed = message.embeds[0]

                if embed.get("author") and embed["author"].get("name"):
                    if embed["author"]["name"][-7:] != "のステータス:":
                        return
                    authos = embed["author"]["name"][:-7]
                    for f in embed["fields"]:
                        if f["name"] == "Lv":
                            level = int(f["value"])
                    for f in embed["fields"]:
                        if f["name"] == "プレイヤーランク":
                            levelss = int(f["value"][:-1])
                    channel = client.get_channel('529139075165192192')
                    member = discord.utils.get(message.server.members,display_name=authos)
                    role_name = next((role[1] for role in ROLES if role[0](level)))
                    role = discord.utils.get(message.server.roles,name=role_name)
                    delete_role_names = [role[1] for role in ROLES if not role[0](level)]
                    delete_roles = [discord.utils.get(message.server.roles,name=role_name) for role_name in
                                    delete_role_names]
                    for value in sorted(ROLE_LEVELSS.values()):
                        if value > level:
                            next_level = value
                            break
                    else:
                        next_level = '6000'
                        for value in sorted(ROLE_LEVELSS.values()):
                            if level > value:
                                await client.send_message(message.channel,
                                                          "```凄い！あなたは今鯖のレベル役職の付与範囲を超えてしまった！\nぜひ運営に役職を追加して貰ってください！\nこの鯖のTAOの最高レベル役職は『{}』です。```".format(
                                                              role_name))
                                return
                    if role in member.roles:
                        await client.send_message(message.channel,
                                                  "次のレベル役職を得るためには{}Lvが必要です！".format(int(next_level - level)))
                        await client.send_message(channel,
                                                  "```・TAO関連 \n発言鯖名:『{0}』 \n\nSTATUSを確認した人:『{1}』 \n現在のレベルは:{2}Lv \nこのひとに適切な役職は『{3}』です。\nこの人はTAOで{4}位です。\n次の役職まで後{5}Lvです！\n\nログ報告時刻:{6}```".format(
                                                      message.server,member,level,role_name,levelss,
                                                      int(next_level - level),
                                                      datetime.now().strftime(" %Y/%m/%d %H:%M:%S")))
                        print("----------------------------------")
                        print(
                            "TAO関連 \n発言鯖名:『{0}』 \nSTATUSを確認した人:『{1}』 \n現在のレベルは:{2}Lv \nこのひとに適切な役職は『{3}』です。\nこの人はTAOで{4}位です。\n次の役職まで後{5}Lvです！\nログ報告時刻:{6}".format(
                                message.server,member,level,role_name,levelss,int(next_level - level),
                                datetime.now().strftime(" %Y/%m/%d %H:%M:%S")))
                        print("----------------------------------")
                        return
                    else:
                        await client.add_roles(member,role)
                        await client.remove_roles(member,*delete_roles)
                        await client.send_message(message.channel,
                                                  "前の役職を削除しました。\n役職名:『{0}』を付与しました。\n次の役職まで後{1}Lvです！".format(
                                                      discord.utils.get(message.server.roles,name=role_name),
                                                      int(next_level - level)))
                        await client.send_message(channel,
                                                  "```・TAO関連 \n発言鯖名:『{0}』 \n\nSTATUSを確認した人:『{1}』 \n現在のレベルは:{2}Lv \nこのひとに適切な役職は『{3}』です。\nこの人はTAOで{4}位です。\n次の役職まで後{5}Lvです！\n\nログ報告時刻:{6}```".format(
                                                      message.server,member,level,role_name,levelss,
                                                      int(next_level - level),
                                                      datetime.now().strftime(" %Y/%m/%d %H:%M:%S")))
                        print("----------------------------------")
                        print(
                            "TAO関連 \n発言鯖名:『{0}』 \nSTATUSを確認した人:『{1}』 \n現在のレベルは:{2}Lv \nこのひとに適切な役職は『{3}』です。\nこの人はTAOで{4}位です。\n次の役職まで後{5}Lvです！\nログ報告時刻:{6}".format(
                                message.server,member,level,role_name,levelss,int(next_level - level),
                                datetime.now().strftime(" %Y/%m/%d %H:%M:%S")))
                        print("----------------------------------")
                        channel = client.get_channel('528940004181934120')
                        mem = str(member)
                        nick = message.server.me
                        if not nick.nick == None:
                            nick_name = nick.nick
                        else:
                            nick_name = nick.name
                        if message.content.find("役職を付与しました"):
                            embedee = discord.Embed(
                                title=mem + "さんにレベル役職を付けました！",
                                description="",
                                color=discord.Color(random.randint(0,0xFFFFFF)),
                                timestamp=message.timestamp
                            )
                            embedee.set_thumbnail(
                                url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(
                                    member)
                            )
                            embedee.add_field(
                                name="役職更新おめでとうです～",
                                value="役職名:『" + role_name + "』"
                            )
                            embedee.set_footer(
                                text="発言時刻 "
                            )
                            embedee.set_author(
                                name=nick_name,
                                icon_url="https://cdn.discordapp.com/attachments/514424761074581504/528492969322479629/1670560676-star-jRPy-1920x1080-MM-100.jpg"
                            )
                            await client.send_message(channel,embed=embedee)
                            return
                # -------------------------------------------------------------------------------------------------------------------
                # L会議-TAO部門
        if len(message.embeds) != 0:
            if message.server.id == "526957203479986176":
                embed = message.embeds[0]
                if embed.get("author") and embed["author"].get("name"):
                    if embed["author"]["name"][-7:] != "のステータス:":
                        return
                    authos = embed["author"]["name"][:-7]
                    for f in embed["fields"]:
                        if f["name"] == "Lv":
                            level = int(f["value"])
                    for f in embed["fields"]:
                        if f["name"] == "プレイヤーランク":
                            plevel = int(f["value"][:-1])

                    channel = client.get_channel('529139075165192192')
                    member = discord.utils.get(message.server.members,display_name=authos)
                    role_name = next((role[1] for role in ROLESS if role[0](level)))
                    role = discord.utils.get(message.server.roles,name=role_name)
                    delete_role_names = [role[1] for role in ROLESS if not role[0](level)]
                    delete_roles = [discord.utils.get(message.server.roles,name=role_name) for role_name in
                                    delete_role_names]
                    for value in sorted(ROLE_LEVELSSS.values()):
                        if value > level:
                            next_level = value
                            break
                    else:
                        next_level = '5000'
                        for value in sorted(ROLE_LEVELSSS.values()):
                            if level > value:
                                await client.send_message(message.channel,
                                                          "```凄い！あなたは今鯖のレベル役職の付与範囲を超えてしまった！\nぜひ運営に役職を追加して貰ってください！\nこの鯖のTAOの最高レベル役職は『{}』です。```".format(
                                                              role_name))
                                return
                    if role in member.roles:
                        await client.send_message(message.channel,
                                              "次のレベル役職を得るためには{}Lvが必要です！".format(int(next_level - level)))
                        await client.send_message(channel,
                                              "```・TAO関連 \n発言鯖名:『{0}』 \n\nSTATUSを確認した人:『{1}』 \n現在のレベルは:{2}Lv \nこのひとに適切な役職は『{3}』です。\nこの人はTAOで{4}位です。\n次の役職まで後{5}Lvです！\n\nログ報告時刻:{6}```".format(
                                                  message.server,member,level,role_name,plevel,
                                                  int(next_level - level),
                                                  datetime.now().strftime(" %Y/%m/%d %H:%M:%S")))
                        print("----------------------------------")
                        print(
                            "TAO関連 \n発言鯖名:『{0}』 \nSTATUSを確認した人:『{1}』 \n現在のレベルは:{2}Lv \nこのひとに適切な役職は『{3}』です。\nこの人はTAOで{4}位です。\n次の役職まで後{5}Lvです！\nログ報告時刻:{6}".format(
                                message.server,member,level,role_name,plevel,int(next_level - level),
                                datetime.now().strftime(" %Y/%m/%d %H:%M:%S")))
                        print("----------------------------------")
                        return
                    else:
                        await client.add_roles(member,role)
                        await client.remove_roles(member,*delete_roles)
                        await client.send_message(message.channel,
                                                  "前の役職を削除しました。\n役職名:『{0}』を付与しました。\n次の役職まで後{1}Lvです！".format(
                                                      discord.utils.get(message.server.roles,name=role_name),
                                                      int(next_level - level)))
                        await client.send_message(channel,
                                                  "```・TAO関連 \n発言鯖名:『{0}』 \n\nSTATUSを確認した人:『{1}』 \n現在のレベルは:{2}Lv \nこのひとに適切な役職は『{3}』です。\nこの人はTAOで{4}位です。\n次の役職まで後{5}Lvです！\n\nログ報告時刻:{6}```".format(
                                                      message.server,member,level,role_name,plevel,
                                                      int(next_level - level),
                                                      datetime.now().strftime(" %Y/%m/%d %H:%M:%S")))
                        print("----------------------------------")
                        print(
                            "TAO関連 \n発言鯖名:『{0}』 \nSTATUSを確認した人:『{1}』 \n現在のレベルは:{2}Lv \nこのひとに適切な役職は『{3}』です。\nこの人はTAOで{4}位です。\n次の役職まで後{5}Lvです！\nログ報告時刻:{6}".format(
                                message.server,member,level,role_name,plevel,int(next_level - level),
                                datetime.now().strftime(" %Y/%m/%d %H:%M:%S")))
                        print("----------------------------------")
                        channel = client.get_channel('529191465222406146')
                        mem = str(member)
                        nick = message.server.me
                        if not nick.nick == None:
                            nick_name = nick.nick
                        else:
                            nick_name = nick.name
                        if message.content.find("役職を付与しました"):
                            embedee = discord.Embed(
                                title=mem + "さんにレベル役職を付けました！",
                                description="",
                                color=discord.Color(random.randint(0,0xFFFFFF)),
                                timestamp=message.timestamp
                            )
                            embedee.set_thumbnail(
                                url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(
                                    member)
                            )
                            embedee.add_field(
                                name="役職更新おめでとうです～",
                                value="役職名:『" + role_name + "』"
                            )
                            embedee.set_footer(
                                text="発言時刻 "
                            )
                            embedee.set_author(
                                name=nick_name,
                                icon_url="https://cdn.discordapp.com/attachments/514424761074581504/528492969322479629/1670560676-star-jRPy-1920x1080-MM-100.jpg"
                            )
                            await client.send_message(channel,embed=embedee)
                            return

                # -------------------------------------------------------------------------------------------------------------------

        if len(message.embeds) != 0:
            if message.server.id == "479848615326515201":
                embed = message.embeds[0]
                if embed.get("author") and embed["author"].get("name"):
                    if embed["author"]["name"][-7:] != "のステータス:":
                        return
                    authos = embed["author"]["name"][:-7]
                    for f in embed["fields"]:
                        if f["name"] == "Lv":
                            level = int(f["value"])
                    for f in embed["fields"]:
                        if f["name"] == "プレイヤーランク":
                            plevel = int(f["value"][:-1])
                    channel = client.get_channel('529139075165192192')
                    member = discord.utils.get(message.server.members,display_name=authos)
                    role_name = next((role[1] for role in ROLESSS if role[0](level)))
                    role = discord.utils.get(message.server.roles,name=role_name)
                    delete_role_names = [role[1] for role in ROLESSS if not role[0](level)]
                    delete_roles = [discord.utils.get(message.server.roles,name=role_name) for role_name in
                                    delete_role_names]
                    for value in sorted(ROLE_LEVELSSSS.values()):
                        if value > level:
                            next_level = value
                            break
                    else:
                        next_level = '4000'
                        for value in sorted(ROLE_LEVELSSSS.values()):
                            if level > value:
                                await client.send_message(message.channel,
                                                          "```凄い！あなたは今鯖のレベル役職の付与範囲を超えてしまった！\nぜひ運営に役職を追加して貰ってください！\nこの鯖のTAOの最高レベル役職は『{}』です。```".format(
                                                              role_name))
                                return
                    if role in member.roles:
                        await client.send_message(message.channel,
                                                  "次のレベル役職を得るためには{}Lvが必要です！".format(int(next_level - level)))
                        await client.send_message(channel,
                                                  "```・TAO関連 \n発言鯖名:『{0}』 \n\nSTATUSを確認した人:『{1}』 \n現在のレベルは:{2}Lv \nこのひとに適切な役職は『{3}』です。\nこの人はTAOで{4}位です。\n次の役職まで後{5}Lvです！\n\nログ報告時刻:{6}```".format(
                                                      message.server,member,level,role_name,plevel,
                                                      int(next_level - level),
                                                      datetime.now().strftime(" %Y/%m/%d %H:%M:%S")))
                        print("----------------------------------")
                        print(
                            "TAO関連 \n発言鯖名:『{0}』 \nSTATUSを確認した人:『{1}』 \n現在のレベルは:{2}Lv \nこのひとに適切な役職は『{3}』です。\nこの人はTAOで{4}位です。\n次の役職まで後{5}Lvです！\nログ報告時刻:{6}".format(
                                message.server,member,level,role_name,plevel,int(next_level - level),
                                datetime.now().strftime(" %Y/%m/%d %H:%M:%S")))
                        print("----------------------------------")
                        return
                    else:
                        await client.add_roles(member,role)
                        await client.remove_roles(member,*delete_roles)
                        await client.send_message(message.channel,
                                                  "前の役職を削除しました。\n役職名:『{0}』を付与しました。\n次の役職まで後{1}Lvです！".format(
                                                      discord.utils.get(message.server.roles,name=role_name),
                                                      int(next_level - level)))
                        await client.send_message(channel,
                                                  "```・TAO関連 \n発言鯖名:『{0}』 \n\nSTATUSを確認した人:『{1}』 \n現在のレベルは:{2}Lv \nこのひとに適切な役職は『{3}』です。\nこの人はTAOで{4}位です。\n次の役職まで後{5}Lvです！\n\nログ報告時刻:{6}```".format(
                                                      message.server,member,level,role_name,levelss,
                                                      int(next_level - level),
                                                      datetime.now().strftime(" %Y/%m/%d %H:%M:%S")))
                        print("----------------------------------")
                        print(
                            "TAO関連 \n発言鯖名:『{0}』 \nSTATUSを確認した人:『{1}』 \n現在のレベルは:{2}Lv \nこのひとに適切な役職は『{3}』です。\nこの人はTAOで{4}位です。\n次の役職まで後{5}Lvです！\nログ報告時刻:{6}".format(
                                message.server,member,level,role_name,plevel,int(next_level - level),
                                datetime.now().strftime(" %Y/%m/%d %H:%M:%S")))
                        print("----------------------------------")
                        channel = client.get_channel('532133404624289802')
                        mem = str(member)
                        nick = message.server.me
                        if not nick.nick == None:
                            nick_name = nick.nick
                        else:
                            nick_name = nick.name
                        if message.content.find("役職を付与しました"):
                            embedee = discord.Embed(
                                title=mem + "さんにレベル役職を付けました！",
                                description="",
                                color=discord.Color(random.randint(0,0xFFFFFF)),
                                timestamp=message.timestamp
                            )
                            embedee.set_thumbnail(
                                url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(
                                    member)
                            )
                            embedee.add_field(
                                name="役職更新おめでとうです～",
                                value="役職名:『" + role_name + "』"
                            )
                            embedee.set_footer(
                                text="発言時刻 "
                            )
                            embedee.set_author(
                                name=nick_name,
                                icon_url="https://cdn.discordapp.com/attachments/514424761074581504/528492969322479629/1670560676-star-jRPy-1920x1080-MM-100.jpg"
                            )
                            await client.send_message(channel,embed=embedee)
                            return

        if len(message.embeds) != 0:
            if message.server.id == "533235864164368384":
                embed = message.embeds[0]
                if embed.get("author") and embed["author"].get("name"):
                    if embed["author"]["name"][-9:] != "'s status":
                        return
                    authos = embed["author"]["name"][:-9]
                    for f in embed["fields"]:
                        if f["name"] == "Lv":
                            level = int(f["value"])
                    for f in embed["fields"]:
                        if f["name"] == "Global Player rank":
                            plevel = int(f["value"][3:])

                    channel = client.get_channel('529139075165192192')
                    member = discord.utils.get(message.server.members,display_name=authos)
                    role_name = next((role[1] for role in ROLESSSS if role[0](level)))
                    role = discord.utils.get(message.server.roles,name=role_name)
                    delete_role_names = [role[1] for role in ROLESSSS if not role[0](level)]
                    delete_roles = [discord.utils.get(message.server.roles,name=role_name) for role_name in
                                    delete_role_names]
                    for value in sorted(ROLE_LEVELSSSSS.values()):
                        if value > level:
                            next_level = value
                            break
                    else:
                        next_level = '1000'
                        for value in sorted(ROLE_LEVELSSSSS.values()):
                            if level > value:
                                await client.send_message(message.channel,
                                                          "```WOW!!\nYou has exceeded the range of server role levels!!```")
                                return
                    if role in member.roles:
                        await client.send_message(message.channel,
                                                  "You need {} level to get next role!!".format(
                                                      int(next_level - level)))
                        await client.send_message(channel,
                                                  "```・TAO関連 \n発言鯖名:『{0}』 \n\nSTATUSを確認した人:『{1}』 \n現在のレベルは:{2}Lv \nこのひとに適切な役職は『{3}』です。\nこの人はTAOで{4}位です。\n次の役職まで後{5}Lvです！\n\nログ報告時刻:{6}```".format(
                                                      message.server,member,level,role_name,plevel,
                                                        int(next_level - level),
                                                      datetime.now().strftime(" %Y/%m/%d %H:%M:%S")))
                        print("----------------------------------")
                        print(
                            "TAO関連 \n発言鯖名:『{0}』 \nSTATUSを確認した人:『{1}』 \n現在のレベルは:{2}Lv \nこのひとに適切な役職は『{3}』です。\nこの人はTAOで{4}位です。\n次の役職まで後{5}Lvです！\nログ報告時刻:{6}".format(
                                message.server,member,level,role_name,plevel,int(next_level - level),
                                datetime.now().strftime(" %Y/%m/%d %H:%M:%S")))
                        print("----------------------------------")
                        return
                    else:
                        await client.add_roles(member,role)
                        await client.remove_roles(member,*delete_roles)
                        await client.send_message(message.channel,
                                                  "Previous role was removed!!\nRole name:『{0}』was added to you!!\nYou need {1} level to get next role!!".format(
                                                      discord.utils.get(message.server.roles,name=role_name),                                                          int(next_level - level)))
                        await client.send_message(channel,
                                                  "```・TAO関連 \n発言鯖名:『{0}』 \n\nSTATUSを確認した人:『{1}』 \n現在のレベルは:{2}Lv \nこのひとに適切な役職は『{3}』です。\nこの人はTAOで{4}位です。\n次の役職まで後{5}Lvです！\n\nログ報告時刻:{6}```".format(
                                                      message.server,member,level,role_name,plevel,
                                                      int(next_level - level),
                                                      datetime.now().strftime(" %Y/%m/%d %H:%M:%S")))
                        print("----------------------------------")
                        print(
                            "TAO関連 \n発言鯖名:『{0}』 \nSTATUSを確認した人:『{1}』 \n現在のレベルは:{2}Lv \nこのひとに適切な役職は『{3}』です。\nこの人はTAOで{4}位です。\n次の役職まで後{5}Lvです！\nログ報告時刻:{6}".format(
                                message.server,member,level,role_name,plevel,int(next_level - level),
                                datetime.now().strftime(" %Y/%m/%d %H:%M:%S")))
                        print("----------------------------------")
                        channel = client.get_channel('533275521597964309')
                        mem = str(member)
                        nick = message.server.me
                        if not nick.nick == None:
                            nick_name = nick.nick
                        else:
                            nick_name = nick.name

                        if message.content.find("Previous role was removed!!"):
                            embedee = discord.Embed(
                                title=mem + "has get a new role!！",
                                description="",
                                color=discord.Color(random.randint(0,0xFFFFFF)),
                                timestamp=message.timestamp
                            )
                            embedee.set_thumbnail(
                                url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(
                                    member)
                            )
                            embedee.add_field(
                                name="Congratulations on your level role update!!",
                                value="Role Name:『" + role_name + "』"
                            )
                            embedee.set_footer(
                                text="Time "
                            )
                            embedee.set_author(
                                name=nick_name,
                                icon_url="https://cdn.discordapp.com/attachments/514424761074581504/528492969322479629/1670560676-star-jRPy-1920x1080-MM-100.jpg"
                            )
                            await client.send_message(channel,embed=embedee)
                            return


            # -------------------------------------------------------------------------------------------------------------------
            # のんきなMMO&miner&tao&uuuレベル上げ場
    match = RE_STATUS.match(message.content)
    if not match:
        return
    if message.server.id == "415120414323245057":
        try:
            channel = client.get_channel('529139075165192192')
            user_id = match[1]
            level = int(match[2])
            role_name = next((role[1] for role in ROLE_MAP if role[0](level)))
            role = discord.utils.get(message.server.roles,name=role_name)
            delete_role_names = [role[1] for role in ROLE_MAP if not role[0](level)]
            delete_roles = [discord.utils.get(message.server.roles,name=role_name) for role_name in
                            delete_role_names]
            for value in sorted(ROLE_LEVELS.values()):
                if value > level:
                    next_levels = value
                    break
            else:
                next_levels = '500000'
                for value in sorted(ROLE_LEVEL.values()):
                    if level > value:
                        await client.send_message(message.channel,
                                                  "```凄い！あなたは今鯖のレベル役職の付与範囲を超えてしまった！\nぜひ運営に役職を追加して貰ってください！\nこの鯖のMMOの最高レベル役職は『{}』です。```".format(
                                                      role_name))
                        return
            if role in discord.utils.get(message.server.members,id=user_id).roles:
                await client.send_message(message.channel,
                                          "次のレベル役職を得るためには{}Lvが必要です！".format(int(next_levels - level)))
                await client.send_message(channel,
                                          "```・MMO関連 \n\n発言鯖名:『{0}』 \nSTATUSを確認した人:『{1}』 \n現在のレベルは:{2}Lv \nこの人に適切な役職は『{3}』です。\n次の役職まで後{4}Lvです！\n\nログ報告時刻:{5}```".format(
                                              message.server,
                                              discord.utils.get(message.server.members,id=user_id),level,
                                              role_name,int(next_levels - level),
                                              datetime.now().strftime(" %Y/%m/%d %H:%M:%S")))
                print("----------------------------------")
                print(
                    "MMO関連 \n発言鯖名:『{0}』 \nSTATUSを確認した人:『{1}』 \n現在のレベルは:{2}Lv \nこの人に適切な役職は『{3}』です。\n次の役職まで後{4}Lvです！\nログ報告時刻:{5}".format(
                        message.server,discord.utils.get(message.server.members,id=user_id),level,role_name,
                        int(next_levels - level),datetime.now().strftime(" %Y/%m/%d %H:%M:%S")))
                print("----------------------------------")
                return
            else:
                await client.add_roles(discord.utils.get(message.server.members,id=user_id),role)
                await client.remove_roles(discord.utils.get(message.server.members,id=user_id),*delete_roles)
                await client.send_message(message.channel,
                                          "前の役職を削除しました。\n役職名:『{0}』を付与しました。\n次の役職まで後{1}Lvです！".format(
                                              discord.utils.get(message.server.roles,name=role_name),
                                              int(next_levels - level)))
                await client.send_message(channel,
                                          "```・MMO関連 \n\n発言鯖名:『{0}』 \nSTATUSを確認した人:『{1}』 \n現在のレベルは:{2}Lv \nこの人に適切な役職は『{3}』です。\n次の役職まで後{4}Lvです！\n\nログ報告時刻:{5}```".format(
                                                message.server,
                                                discord.utils.get(message.server.members,id=user_id),level,
                                                role_name,int(next_levels - level),
                                                datetime.now().strftime(" %Y/%m/%d %H:%M:%S")))
                print("---------------------------------")
                print(
                    "MMO関連 \n発言鯖名:『{0}』 \nSTATUSを確認した人:『{1}』 \n現在のレベルは:{2}Lv \nこの人に適切な役職は『{3}』です。\n次の役職まで後{4}Lvです！\nログ報告時刻:{5}".format(
                        message.server,discord.utils.get(message.server.members,id=user_id),level,role_name,
                        int(next_levels - level),datetime.now().strftime(" %Y/%m/%d %H:%M:%S")))
                print("----------------------------------")
        except ArithmeticError:
            await client.send_message(message.channel,"すいません。ERRORです。")
        except:
            await client.send_message(message.channel,"役職が付与されてると思いますが、\nなんか謎のERRORが出ています。\n付与されてなかったらスマナイ；；")
        finally:
            return

    # -------------------------------------------------------------------------------------------------------------------

client.loop.create_task(change_status())
client.run(os.getenv('TOKEN'))
