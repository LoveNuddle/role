# -------------------------------------------------------------------------------------------------------------------
import os
import asyncio
import sys
import sqlite3
import random
import platform

from datetime import datetime
from contextlib import closing
from collections import defaultdict

ROLE_PER_SERVER = defaultdict(list)
ROLE_LEVEL_PER_SERVER = defaultdict(dict)

try:
    from discord.ext import commands
    from discord.ext.commands import Bot
    from discord.voice_client import VoiceClient
    from discord import ChannelType
    import discord
except ImportError:
    print("Discord.py がインストールされていません。\nDiscord.pyをインストールしてください。")
    sys.exit(1)
# -------------------------------------------------------------------------------------------------------------------
client = Bot(command_prefix='&',pm_help=True)

# -------------------------------------------------------------------------------------------------------------------
@client.event
async def on_ready():
    print("起動完了じゃああああああああああああああああああああ")


# -------------------------------------------------------------------------------------------------------------------
@client.event
async def on_server_join(server):
    await client.send_message(server.owner,
                              f"""```
                              {server.owner}さん
                              このBOTを入れてくれてありがとう！
                              このBOTは管理:The.First.Step#3454
                              多大なるサポート:FaberSidさん,midoristさん
                              の協力のもと作成しました！
                              ```""")
    up = discord.Color(random.randint(0,0xFFFFFF))
    embed = discord.Embed(
        title=server.name + "鯖にこのBOTが導入されました",
        description="このBOTはTAOと連動しています",
        color=up
    )
    embed.set_author(
        name="役職自動付与BOT-NEWを導入した鯖情報:"
    )
    embed.set_thumbnail(
        url=server.icon_url
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
    await client.send_message(client.get_channel('529139075165192192'),embed=embed)


# -------------------------------------------------------------------------------------------------------------------
@client.event
async def on_member_join(member):
    if not member.server.id == "337524390155780107":
        return
    if client.user == member:
        return
    if int(50 - len(member.server.members) % 50) == int(50):
        await client.send_message(client.get_channel('537973804052512779'),f"@here \nクランイベント～～～～！！")
        return
    await client.send_message(client.get_channel('537973804052512779'),
                              "TAOクランイベント情報!!\n後`『{}』`人がこの鯖に入ったらクランイベント開始です！".format(
                                  int(50 - len(member.server.members) % 50)))
    await client.send_message(member,
                              "`{0}さんようこそ{1}へ！\nこの鯖はMMOくんとTAOくん専門の鯖です！\n今後ともよろしくお願いします！`".format(member.name,
                                                                                                 member.server.name))
    mmo = client.get_channel('337860614846283780')
    tao = client.get_channel('528113643330600971')
    self = client.get_channel('537228631097737216')
    yakushoku = client.get_channel('535957520666066954')
    up = discord.Color(random.randint(0,0xFFFFFF))
    embed = discord.Embed(
        title="よろしくお願いします～",
        description=f"""
        `現在の鯖の人数: `{len(member.server.members)}

        `MMOのstatusを表示させる場合は: `{mmo.mention}

        `TAOのstatusを表示させる場合は: `{tao.mention}


        `statusの表示のさせ方`
        `MMOの場合が!!status
        TAOの場合は::stか::statusです！`

        {tao.mention}でTAOのstatusを表示させると
        自動で役職がもらえるよ！

        `自己紹介よろしくお願いします。`
        {self.mention}で自己紹介お願いします～
        """,
        color=up
    )
    embed.set_author(
        name=member.name + "さんがこの鯖に入りました！"
    )
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(member)
    )
    await client.send_message(client.get_channel('338173860719362060'),embed=embed)
    embed = discord.Embed(
        title="もしこのBOTが起動してなく役職を付与されなかったら...",
        description=f"""
        `この鯖で発言権限を得るためには『暇人』役職が必要です。`
        もしこのBOTが起動してなく役職が付与されてない場合は
        このBOTが起動しているときに{yakushoku.mention}で『役職付与』と打ってください。
        """,
        color=up
    )
    await client.send_message(client.get_channel('338173860719362060'),embed=embed)
    role = discord.utils.get(member.server.roles,name="暇人")
    await client.add_roles(member,role)
    await client.send_message(client.get_channel('338173860719362060'),"{}さんに役職を付与しました。".format(member.mention))


# -------------------------------------------------------------------------------------------------------------------
@client.event
async def on_member_remove(member):
    if not member.server.id == "337524390155780107":
        return
    up = discord.Color(random.randint(0,0xFFFFFF))
    embed = discord.Embed(
        title="ありがとうございました！",
        description=f"{member.name}さんが\nこの鯖から退出しました...；；\n\n現在の鯖の人数: {len(member.server.members)}名",
        color=up
    )
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(member)
    )
    await client.send_message(client.get_channel('338173860719362060'),embed=embed)


# -------------------------------------------------------------------------------------------------------------------
async def change_status():
    await client.wait_until_ready()

    while not client.is_closed:
        await client.change_presence(game=discord.Game(name="&helpしてね！"))
        await asyncio.sleep(30)

# -------------------------------------------------------------------------------------------------------------------
@client.event
async def on_message(message):
    if message.content.find("https://discord.gg/") != -1:
        if message.server.id == "337524390155780107":
            if not message.channel.id == "421954703509946368":
                if not message.channel.name == "mmo-global-chat":
                    channel = client.get_channel('421954703509946368')
                    await client.delete_message(message)
                    up = discord.Color(random.randint(0,0xFFFFFF))
                    embed = discord.Embed(
                        title="このチャンネルでは宣伝は禁止です！",
                        description="{0}さん\nもし鯖の宣伝をしたいなら{1}でやってください！\n時間制限無しの宣伝をお願いします！\n\n鯖にTAOかMMOくんが入っていないと宣伝はしてはいけません！".format(
                            message.author.mention,channel.mention),
                        color=up
                    )
                    await client.send_message(message.channel,embed=embed)
                    return

    if message.content == "&help":
        up = discord.Color(random.randint(0,0xFFFFFF))
        embed = discord.Embed(
            title="Help一覧:",
            description=f"""
            [**このBOTの招待**](<https://discordapp.com/oauth2/authorize?client_id=550248294551650305&permissions=8&scope=bot>)
            何かがおかしい...。あれ...？なんで動かないの？
            と思ったらThe.First.Stepにお申し付けください。

            [`&help`]
            このコマンドを表示。

            [`&help command`]
            このBOTのコマンドの機能を表示。

            [`&help tao`]
            TAOと連動するための設定方法を表示！

            [`&help clan`]
            TAO公式鯖でのクランの機能説明。

            ```このBOTは
管理者:The.First.Step#3454
副管理者:FaberSid#2459さん
副管理者:midorist#5677さん
の3人で制作しました！```
            """,
            color=up
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
        )
        await client.send_message(message.channel,embed=embed)

    if message.content == "&help command":
        up = discord.Color(random.randint(0,0xFFFFFF))
        embed = discord.Embed(
            title="Command Help一覧:",
            description=f"""
            [`リスト 役職名`]
            リスト　役職名でその役職が何人に
            付与されているのかを表示します。

            [`全役職一覧`]
            メッセージが送信された鯖でのすべての役職を
            埋め込みメッセージで送信します。

            [`役職一覧`]
            自分が付与されている役職を
            埋め込みメッセージで送信します。

            [`全鯖一覧`]
            このBOTを導入している鯖を全て表示します。

            [`バンリスト`]
            その鯖でBANされている人たちを表示します。
            """,
            color=up
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
        )
        await client.send_message(message.channel,embed=embed)

    if message.content == "&help tao":
        up = discord.Color(random.randint(0,0xFFFFFF))
        embed = discord.Embed(
            title="TAO Help一覧:",
            description=f"""
            注意:これらのレベル設定コマンドは管理者権限が
            ないと設定できません。

            [`&level lower upper 役職名`]
            これでそのレベルが何処からどこまでの範囲で
            対応したいのかを設定することが出来ます！

            `[例: &level 1 10 aaa]`
            これで自分のTAOでのレベルが1~10の時に
            『aaa』という役職が付与されるようになりました。

            [`&list`]
            これで今設定されているレベル役職の全てを
            表示することが出来ます。

            [`&reset`]
            今のところ設定されているレベル役職の範囲を
            全てリセットいたします。

            (間違えてレベル役職の範囲を設定してしまった場合とかに
            お使いいただけたらなと思っています。)
            """,
            color=up
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
        )
        await client.send_message(message.channel,embed=embed)

    if message.content == "&help clan":
        up = discord.Color(random.randint(0,0xFFFFFF))
        embed = discord.Embed(
            title="Clan Help一覧:",
            description=f"""
            これらの機能は[**TAO公式鯖**](<https://discord.gg/d7Qqfhy>)に入りクランに参加
            して頂かないとほとんど意味が無いです。 

            [`クラン勢力図`]
            他のクランと自分のクランとの比較をしたり、
            メンバーの数を確認したり、総長などは誰なのかを把握出来ます。

            [`自クラン勢力図`]
            自分が入っているクランの具体的なメンバーや
            総長などを表示することが出来ます。

            [`除外 @メンション 理由`]
            注意:これは総長や副総長ではないと使用できないです。
            自分のクランで悪目立ちしている人や荒らしなどの権限を
            剥奪することが出来ます。理由を書かないと除外できません。
            """,
            color=up
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
        )
        await client.send_message(message.channel,embed=embed)

    if message.content == "役職付与":
        if not message.channel.id == "535957520666066954":
            channel = client.get_channel('535957520666066954')
            await client.delete_message(message)
            await client.send_message(message.channel,"このコマンドは{}でしか使うことが出来ません".format(channel.mention))
            return
        role = discord.utils.get(message.server.roles,name="暇人")
        if role in message.author.roles:
            up = discord.Color(random.randint(0,0xFFFFFF))
            embed = discord.Embed(
                description=f"{message.author.mention}さん\nあなたはもう既にこの役職を持っています！！",
                color=up
            )
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(message.author)
            )
            await client.send_message(message.channel,embed=embed)
        else:
            await client.add_roles(message.author,role)
            await client.send_message(message.channel,"{0}さんに『{1}』役職を付与しました。".format(message.author.mention,role))

    if message.content.startswith("リスト"):
        async def send(member_data):
            up = discord.Color(random.randint(0,0xFFFFFF))
            name = message.content[4:]
            role = discord.utils.get(message.server.roles,name=message.content[4:])
            if not role == None:
                nick_name = f"『{name}』役職を持っているメンバー！！"
            else:
                nick_name = f"{message.author}さん\n『{name}』役職はこの鯖には存在しておりません..."
            embed = discord.Embed(
                title=nick_name,
                description=member_data,
                color=up,
                timestamp=message.timestamp
            )
            embed.set_author(
                name="メンバー詳細:"
            )
            embed.set_footer(
                text="現在時刻:"
            )
            await client.send_message(message.channel,embed=embed)

        i = 1
        member_data = ""
        role = discord.utils.get(message.server.roles,name=message.content[4:])
        for member in message.server.members:
            if role is None:
                member_data = ""
                await send(member_data)
                return
            if role in member.roles:
                member_data += "{0}人目:『{1}』\n".format(i,member.name)
                if i % 100 == 0:
                    await send(member_data)
                    # リセットする
                    member_data = ""
                i += 1
        else:
            await send(member_data)
            return

    if message.content == "全役職一覧":
        def slice(li,n):
            while li:
                yield li[:n]
                li = li[n:]

        for roles in slice(message.server.role_hierarchy,50):
            role = "\n".join(f'{i}: {role.mention}' for (i,role) in enumerate(roles,start=1) if role.mentionable)
            userembed = discord.Embed(
                title="役職一覧:",
                description=role,
                color=discord.Color.light_grey()
            )

            userembed.set_thumbnail(
                url=message.server.icon_url
            )
            userembed.set_author(
                name=message.server.name + "の全役職情報:"
            )
            await client.send_message(message.channel,embed=userembed)
        await client.send_message(message.channel,"この鯖の役職の合計の数は`{}`です！".format(str(len(message.server.roles))))

    if message.content == '役職一覧':
        role = "\n".join([r.mention for r in message.author.roles if r.mentionable][::-1])
        up = discord.Color(random.randint(0,0xFFFFFF))
        embed = discord.Embed(
            title="**{}**に付与されてる役職一覧:".format(message.author),
            description=role,
            color=up
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(message.author)
        )
        await client.send_message(message.channel,embed=embed)

    if message.content == "全鯖一覧":
        def slice(li,n):
            while li:
                yield li[:n]
                li = li[n:]

        for servers in slice(list(client.servers),50):
            embed = discord.Embed(
                title="全鯖一覧",
                description='\n'.join(f'{i}: `{server.name}`' for (i,server) in enumerate(servers,start=1)),
                colour=discord.Color(random.randint(0,0xFFFFFF))
            )
            embed.set_footer(
                text="合計:{}鯖がこのBOTを導入しています！".format(len(client.servers))
            )
            await client.send_message(message.channel,embed=embed)

    if message.content == "バンリスト":
        bannedUsers = await client.get_bans(message.server)
        embed = discord.Embed(
            title="Banされた人たちリスト",
            description='\n'.join(
                f'{i}:`{user.name}` | `ID:{user.id}`' for (i,user) in enumerate(bannedUsers,start=1)),
            colour=discord.Color(random.randint(0,0xFFFFFF))
        )
        embed.set_thumbnail(
            url=message.server.icon_url
        )
        embed.set_footer(
            text="この鯖のBANされている人たちの合計の数は{}人です！".format(len(bannedUsers))
        )
        await client.send_message(message.channel,embed=embed)
        return

    if message.content == "&get":
        if message.author.server_permissions.administrator:
            counter = 0
            channel_name = client.get_channel("550674420222394378")
            for i in message.server.channels:
                async for log in client.logs_from(i,limit=99999999999):
                    if log.server.id == message.server.id:
                        counter += 1
                await client.edit_channel(channel_name,name="Message Count: {}".format(counter))
            a = await client.send_message(message.channel,
                                          "{0}さん。\n合計で『{1}』のメッセージが検出されました。".format(message.author.mention,counter))
            await asyncio.sleep(120)
            await client.delete_message(a)
            return
    # クラン関連
    # -------------------------------------------------------------------------------------------------------------------
    if message.channel.id == "550941424065970176":
        if message.author.id == client.user.id:
            return
        await asyncio.sleep(2)
        await client.delete_message(message)
        if "に入りたいです" in message.content:
            role = discord.utils.get(message.server.roles,name="境界線の彼方")
            if role in message.author.roles:
                a = await client.send_message(message.channel,f"{message.author.mention}さん！\nあなたは既に一つのクランに所属しています！")
                await asyncio.sleep(10)
                await client.delete_message(a)
                return
            role = discord.utils.get(message.server.roles,name="輝く星の最果て")
            if role in message.author.roles:
                a = await client.send_message(message.channel,f"{message.author.mention}さん！\nあなたは既に一つのクランに所属しています！")
                await asyncio.sleep(10)
                await client.delete_message(a)
                return
            role = discord.utils.get(message.server.roles,name="大地の根源と終末")
            if role in message.author.roles:
                a = await client.send_message(message.channel,f"{message.author.mention}さん！\nあなたは既に一つのクランに所属しています！")
                await asyncio.sleep(10)
                await client.delete_message(a)
                return
            role = discord.utils.get(message.server.roles,name="休日のとある一日")
            if role in message.author.roles:
                a = await client.send_message(message.channel,f"{message.author.mention}さん！\nあなたは既に一つのクランに所属しています！")
                await asyncio.sleep(10)
                await client.delete_message(a)
                return
            role = discord.utils.get(message.server.roles,name="宇宙に広がる星屑の集合体")
            if role in message.author.roles:
                a = await client.send_message(message.channel,f"{message.author.mention}さん！\nあなたは既に一つのクランに所属しています！")
                await asyncio.sleep(10)
                await client.delete_message(a)
                return
            else:
                attachable_roles = ("境界線の彼方","輝く星の最果て","大地の根源と終末","休日のとある一日","宇宙に広がる星屑の集合体")
                roles = [role for role in message.server.roles if
                         role.name in attachable_roles and role.name in message.content]
                if not roles:
                    a = await client.send_message(message.channel,
                                                  f"{message.author.mention}さん。この鯖にはこの役職名の役職は存在しないか付与することが出来ない役職です！")
                    await asyncio.sleep(10)
                    await client.delete_message(a)
                    return
                else:
                    await client.add_roles(message.author,*roles)
                    up = discord.Color(random.randint(0,0xFFFFFF))
                    role = discord.utils.get(message.server.roles,name=message.content[2:-7])
                    embed = discord.Embed(
                        title="クラン参加ログ",
                        description=f"""
                        {role.mention}情報!!:
                        {message.author.mention}さんが『{role}』に参加しました！

                        今現在の{role}のメンバー数は{len([m for m in message.server.members if role in m.roles])}名です！
                        """,
                        colour=up,
                        timestamp=message.timestamp
                    )
                    embed.set_thumbnail(
                        url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(message.author)
                    )
                    embed.set_footer(
                        text="加入時刻: "
                    )
                    await client.send_message(client.get_channel("553028767702974464"),embed=embed)
                    return

    if message.content.startswith("除外"):
        user = message.mentions[0]
        try:
            reason = message.content.split()[2]
        except Exception:
            reason = None
        role = discord.utils.get(message.server.roles,name="境界線の彼方:総長&副総長")
        role1 = discord.utils.get(message.server.roles,name="境界線の彼方")
        for member in message.server.members:
            if role in member.roles:
                if message.channel.id == "550936853281243136":
                    if role1 in user.roles:
                        if not reason:
                            await client.send_message(message.channel,"理由をお書きください。\n[例:除外 @メンション 理由]")
                            return
                        else:
                            await client.remove_roles(user,role1)
                            await client.send_message(message.channel,
                                                      f"{message.author.mention}さんが『{user}』さんを除外しました。")
                            up = discord.Color(random.randint(0,0xFFFFFF))
                            embed = discord.Embed(
                                title="除外ログ",
                                description=f"{role1.mention}情報!!:\n\n{message.author.mention}さんが『{user.mention}』さんを除外しました。\n\n理由:\n```{reason}```",
                                colour=up
                            )
                            embed.set_footer(
                                text=f"今現在の境界線の彼方のメンバー数は{len([m for m in message.server.members if role1 in m.roles])}名です！"
                            )
                            await client.send_message(client.get_channel("553028767702974464"),embed=embed)
                            return
        role = discord.utils.get(message.server.roles,name="輝く星の最果て:総長&副総長")
        role1 = discord.utils.get(message.server.roles,name="輝く星の最果て")
        for member in message.server.members:
            if role in member.roles:
                if message.channel.id == "550937108915945473":
                    if role1 in user.roles:
                        if not reason:
                            await client.send_message(message.channel,"理由をお書きください。\n[例:除外 @メンション 理由]")
                            return
                        else:
                            await client.remove_roles(user,role1)
                            await client.send_message(message.channel,
                                                      f"{message.author.mention}さんが『{user}』さんを除外しました。")
                            up = discord.Color(random.randint(0,0xFFFFFF))
                            embed = discord.Embed(
                                title="除外ログ",
                                description=f"{role1.mention}情報!!:\n\n{message.author.mention}さんが『{user.mention}』さんを除外しました。\n\n理由:\n```{reason}```",
                                colour=up
                            )
                            embed.set_footer(
                                text=f"今現在の輝く星の最果てのメンバー数は{len([m for m in message.server.members if role1 in m.roles])}名です！"
                            )
                            await client.send_message(client.get_channel("553028767702974464"),embed=embed)
                            return
        role = discord.utils.get(message.server.roles,name="大地の根源と終末:総長&副総長")
        role1 = discord.utils.get(message.server.roles,name="大地の根源と終末")
        for member in message.server.members:
            if role in member.roles:
                if message.channel.id == "550937434569965576":
                    if role1 in user.roles:
                        if not reason:
                            await client.send_message(message.channel,"理由をお書きください。\n[例:除外 @メンション 理由]")
                            return
                        else:
                            await client.remove_roles(user,role1)
                            await client.send_message(message.channel,
                                                      f"{message.author.mention}さんが『{user}』さんを除外しました。")
                            up = discord.Color(random.randint(0,0xFFFFFF))
                            embed = discord.Embed(
                                title="除外ログ",
                                description=f"{role1.mention}情報!!:\n\n{message.author.mention}さんが『{user.mention}』さんを除外しました。\n\n理由:\n```{reason}```",
                                colour=up
                            )
                            embed.set_footer(
                                text=f"今現在の大地の根源と終末のメンバー数は{len([m for m in message.server.members if role1 in m.roles])}名です！"
                            )
                            await client.send_message(client.get_channel("553028767702974464"),embed=embed)
                            return
        role = discord.utils.get(message.server.roles,name="休日のとある一日:総長&副総長")
        role1 = discord.utils.get(message.server.roles,name="休日のとある一日")
        for member in message.server.members:
            if role in member.roles:
                if message.channel.id == "550937533878370338":
                    if role1 in user.roles:
                        if not reason:
                            await client.send_message(message.channel,"理由をお書きください。\n[例:除外 @メンション 理由]")
                            return
                        else:
                            await client.remove_roles(user,role1)
                            await client.send_message(message.channel,
                                                      f"{message.author.mention}さんが『{user}』さんを除外しました。")
                            up = discord.Color(random.randint(0,0xFFFFFF))
                            embed = discord.Embed(
                                title="除外ログ",
                                description=f"{role1.mention}情報!!:\n\n{message.author.mention}さんが『{user.mention}』さんを除外しました。\n\n理由:\n```{reason}```",
                                colour=up
                            )
                            embed.set_footer(
                                text=f"今現在の休日のとある一日のメンバー数は{len([m for m in message.server.members if role1 in m.roles])}名です！"
                            )
                            await client.send_message(client.get_channel("553028767702974464"),embed=embed)
                            return
        role = discord.utils.get(message.server.roles,name="宇宙に広がる星屑の集合体:総長&副総長")
        role1 = discord.utils.get(message.server.roles,name="宇宙に広がる星屑の集合体")
        for member in message.server.members:
            if role in member.roles:
                if message.channel.id == "551523371364384779":
                    if role1 in user.roles:
                        if not reason:
                            await client.send_message(message.channel,"理由をお書きください。\n[例:除外 @メンション 理由]")
                            return
                        else:
                            await client.remove_roles(user,role1)
                            await client.send_message(message.channel,
                                                      f"{message.author.mention}さんが{user}さんを除外しました。")
                            up = discord.Color(random.randint(0,0xFFFFFF))
                            embed = discord.Embed(
                                title="除外ログ",
                                description=f"{role1.mention}情報!!:\n\n{message.author.mention}さんが『{user.mention}』さんを除外しました。\n\n理由:\n```{reason}```",
                                colour=up
                            )
                            embed.set_footer(
                                text=f"今現在の宇宙に広がる星屑の集合体のメンバー数は{len([m for m in message.server.members if role1 in m.roles])}名です！"
                            )
                            await client.send_message(client.get_channel("553028767702974464"),embed=embed)
                            return

    if message.content == "自クラン勢力図":
        role1 = discord.utils.get(message.server.roles,name="境界線の彼方")
        if role1 in message.author.roles:
            up = discord.Color(random.randint(0,0xFFFFFF))

            async def send(member_data):
                role1 = discord.utils.get(message.server.roles,name="境界線の彼方")
                role = discord.utils.get(message.server.roles,name="境界線の彼方:総長&副総長")
                embed = discord.Embed(
                    title="『境界線の彼方クラン』の勢力図",
                    description=f"{role.mention}権限持ち:\n今はだれも居ません！\n\n{role1.mention}のメンバー表:\n" + member_data,
                    color=up
                )
                embed.set_footer(
                    text=f"今現在の境界線の彼方のメンバー数は{len([m for m in message.server.members if role1 in m.roles])}名です！"
                )
                await client.send_message(message.channel,embed=embed)

            i = 1
            member_data = ""
            role1 = discord.utils.get(message.server.roles,name="境界線の彼方")
            for member in message.server.members:
                if role1 in member.roles:
                    member_data += "{0}人目:『{1}』\n".format(i,member.name)
                    if i % 100 == 0:
                        await send(member_data)
                        # リセットする
                        member_data = ""
                    i += 1
            else:
                await send(member_data)
                return

        role1 = discord.utils.get(message.server.roles,name="輝く星の最果て")
        if role1 in message.author.roles:
            up = discord.Color(random.randint(0,0xFFFFFF))

            async def send(member_data):
                role1 = discord.utils.get(message.server.roles,name="輝く星の最果て")
                role = discord.utils.get(message.server.roles,name="輝く星の最果て:総長&副総長")
                embed = discord.Embed(
                    title="『輝く星の最果てクラン』の勢力図",
                    description=f"{role.mention}権限持ち:\n総長:<@376728551904247808>さん\n副総長:<@527716276643299329>さん\n\n{role1.mention}のメンバー表:\n" + member_data,
                    color=up
                )
                embed.set_footer(
                    text=f"今現在の輝く星の最果てのメンバー数は{len([m for m in message.server.members if role1 in m.roles])}名です！"
                )
                await client.send_message(message.channel,embed=embed)

            i = 1
            member_data = ""
            role1 = discord.utils.get(message.server.roles,name="輝く星の最果て")
            for member in message.server.members:
                if role1 in member.roles:
                    member_data += "{0}人目:『{1}』\n".format(i,member.name)
                    if i % 100 == 0:
                        await send(member_data)
                        # リセットする
                        member_data = ""
                    i += 1
            else:
                await send(member_data)
                return

        role1 = discord.utils.get(message.server.roles,name="大地の根源と終末")
        if role1 in message.author.roles:
            up = discord.Color(random.randint(0,0xFFFFFF))

            async def send(member_data):
                role = discord.utils.get(message.server.roles,name="大地の根源と終末:総長&副総長")
                role1 = discord.utils.get(message.server.roles,name="大地の根源と終末")
                embed = discord.Embed(
                    title="『大地の根源と終末クラン』の勢力図",
                    description=f"{role.mention}権限持ち:\n総長:<@460208854362357770>さん\n副総長:<@507161988682743818>さん\n\n{role1.mention}のメンバー表:\n" + member_data,
                    color=up
                )
                embed.set_footer(
                    text=f"今現在の大地の根源と終末のメンバー数は{len([m for m in message.server.members if role1 in m.roles])}名です！"
                )
                await client.send_message(message.channel,embed=embed)

            i = 1
            member_data = ""
            role1 = discord.utils.get(message.server.roles,name="大地の根源と終末")
            for member in message.server.members:
                if role1 in member.roles:
                    member_data += "{0}人目:『{1}』\n".format(i,member.name)
                    if i % 100 == 0:
                        await send(member_data)
                        # リセットする
                        member_data = ""
                    i += 1
            else:
                await send(member_data)
                return

        role1 = discord.utils.get(message.server.roles,name="休日のとある一日")
        if role1 in message.author.roles:
            up = discord.Color(random.randint(0,0xFFFFFF))

            async def send(member_data):
                role = discord.utils.get(message.server.roles,name="休日のとある一日:総長&副総長")
                role1 = discord.utils.get(message.server.roles,name="休日のとある一日")
                embed = discord.Embed(
                    title="『休日のとある一日クラン』の勢力図",
                    description=f"{role.mention}権限持ち:\n今はだれも居ません！\n\n{role1.mention}のメンバー表:\n" + member_data,
                    color=up
                )
                embed.set_footer(
                    text=f"今現在の休日のとある一日のメンバー数は{len([m for m in message.server.members if role1 in m.roles])}名です！"
                )
                await client.send_message(message.channel,embed=embed)

            i = 1
            member_data = ""
            role1 = discord.utils.get(message.server.roles,name="休日のとある一日")
            for member in message.server.members:
                if role1 in member.roles:
                    member_data += "{0}人目:『{1}』\n".format(i,member.name)
                    if i % 100 == 0:
                        await send(member_data)
                        # リセットする
                        member_data = ""
                    i += 1
            else:
                await send(member_data)
                return

        role1 = discord.utils.get(message.server.roles,name="宇宙に広がる星屑の集合体")
        if role1 in message.author.roles:
            up = discord.Color(random.randint(0,0xFFFFFF))

            async def send(member_data):
                role = discord.utils.get(message.server.roles,name="宇宙に広がる星屑の集合体:総長&副総長")
                role1 = discord.utils.get(message.server.roles,name="宇宙に広がる星屑の集合体")
                embed = discord.Embed(
                    title="『宇宙に広がる星屑の集合体クラン』の勢力図",
                    description=f"{role.mention}権限持ち:\n今はだれも居ません！\n\n{role1.mention}のメンバー表:\n" + member_data,
                    color=up
                )
                embed.set_footer(
                    text=f"今現在の宇宙に広がる星屑の集合体のメンバー数は{len([m for m in message.server.members if role1 in m.roles])}名です！"
                )
                await client.send_message(message.channel,embed=embed)

            i = 1
            member_data = ""
            role1 = discord.utils.get(message.server.roles,name="宇宙に広がる星屑の集合体")
            for member in message.server.members:
                if role1 in member.roles:
                    member_data += "{0}人目:『{1}』\n".format(i,member.name)
                    if i % 100 == 0:
                        await send(member_data)
                        # リセットする
                        member_data = ""
                    i += 1
            else:
                await send(member_data)
                return

    if message.content == "クラン勢力図":
        role1 = discord.utils.get(message.server.roles,name="境界線の彼方")
        count1 = len([m for m in message.server.members if role1 in m.roles])
        role2 = discord.utils.get(message.server.roles,name="輝く星の最果て")
        count2 = len([m for m in message.server.members if role2 in m.roles])
        role3 = discord.utils.get(message.server.roles,name="大地の根源と終末")
        count3 = len([m for m in message.server.members if role3 in m.roles])
        role4 = discord.utils.get(message.server.roles,name="休日のとある一日")
        count4 = len([m for m in message.server.members if role4 in m.roles])
        role5 = discord.utils.get(message.server.roles,name="宇宙に広がる星屑の集合体")
        count5 = len([m for m in message.server.members if role5 in m.roles])
        up = discord.Color(random.randint(0,0xFFFFFF))
        embed = discord.Embed(
            title="クランの勢力表:",
            description=f"""
                        {role1.mention}: {count1}名
                        総長:現在無し | 副総長:現在無し

                        {role2.mention}: {count2}名
                        総長:<@376728551904247808>さん | 副総長:<@527716276643299329>さん

                        {role3.mention}: {count3}名
                        総長:<@460208854362357770>さん | 副総長:<@507161988682743818>さん

                        {role4.mention}: {count4}名
                        総長:現在無し | 副総長:現在無し

                        {role5.mention}: {count5}名
                        総長:現在無し | 副総長:現在無し

                        ※総長や副総長などはそのクランで
                        15名を超えないと就任することが出来ません。

                        総長や副総長は悪目立ちしてる人や
                        荒らしが入ってきた場合、自分のクランのメンバーだけに対して
                        『除外 @メンション 理由』とすればそのメンバーは除外されます。
                        """,
            colour=up
        )
        await client.send_message(message.channel,embed=embed)
        return
    # -------------------------------------------------------------------------------------------------------------------

    # globalチャット関連
    # -------------------------------------------------------------------------------------------------------------------
    channel = [c for c in message.server.channels if message.channel.name == "tao-global"]
    if channel:
        if not message.author == client.user:
            if not message.author.bot:
                await client.delete_message(message)
                embed = discord.Embed(
                    title="発言者:" + message.author.name + "#" + message.author.discriminator,
                    description=message.content,
                    color=discord.Color.dark_grey(),
                    timestamp=message.timestamp
                )
                embed.set_thumbnail(
                    url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(message.author)
                )
                embed.set_footer(
                    text="発言時刻: "
                )
                embed.set_author(
                    name=message.server.name,
                    icon_url=message.server.icon_url
                )
                await asyncio.gather(*(client.send_message(c,embed=embed) for c in client.get_all_channels() if
                                       c.name == 'tao-global'))

                if message.content == "グローバルリスト":
                    async def send(server_data):
                        up = discord.Color(random.randint(0,0xFFFFFF))
                        embed = discord.Embed(
                            title="tao-globalチャンネルに接続してるサバリスト:",
                            description=server_data,
                            color=up,
                            timestamp=message.timestamp
                        )
                        embed.set_footer(
                            text="現在時刻:"
                        )
                        await asyncio.gather(*(client.send_message(c,embed=embed) for c in client.get_all_channels() if
                                               c.name == 'tao-global'))

                    i = 1
                    server_data = ""
                    for server in client.servers:
                        if [client.get_all_channels() for channel in server.channels if channel.name == "tao-global"]:
                            server_data += "{0}:『{1}』\n".format(i,server.name)
                            if i % 100 == 0:
                                await send(server_data)
                                # リセットする
                                server_data = ""
                            i += 1
                    else:
                        await send(server_data)
                        return

    # -------------------------------------------------------------------------------------------------------------------
    if message.content.startswith('&shutdown'):
        if not message.author.id == "304932786286886912":
            await client.send_message(message.channel,"**これは全権限者しか使用できないコマンドです.**")
            return
        await client.logout()
        await client.close()
    # TAOのstatusの処理
    # -------------------------------------------------------------------------------------------------------------------
    if message.content == "&list":
        if message.author.server_permissions.administrator:
            if len(list(db_read(message.server.id))) == 0:
                embed = discord.Embed(
                    description="この鯖にはレベル役職が登録されてません。",
                    color=discord.Color(random.randint(0,0xFFFFFF))
                )
                await client.send_message(message.channel,embed=embed)
                return
            i = 0
            reply = ""
            for row in db_read(message.server.id):
                if i % 50 == 0:
                    if i > 0:
                        embed = discord.Embed(
                            title="",
                            description=reply,
                            color=discord.Color(random.randint(0,0xFFFFFF))
                        )
                        embed.set_author(
                            name="現在の役職リストはこちらです。",
                            url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
                        )
                        embed.set_footer(
                            text=f"発言者:{message.author.name}さん"
                        )
                        await client.send_message(message.channel,embed=embed)
                    reply = "`[{}]: Lv{}~{}:『{}』`\n".format(i + 1,row[0],row[1],discord.utils.get(
                        message.server.roles,id=str(row[2])).name)
                else:
                    reply += "`[{}]: Lv{}~{}:『{}』`\n".format(i + 1,row[0],row[1],discord.utils.get(
                        message.server.roles,id=str(row[2])).name)
                i += 1
            if i % 50 >= 0 or i <= 50:
                embed = discord.Embed(
                    title="",
                    description=reply,
                    color=discord.Color(random.randint(0,0xFFFFFF))
                )
                embed.set_author(
                    name="現在の役職リストはこちらです。"
                )
                embed.set_footer(
                    text=f"発言者:{message.author.name}さん"
                )
                embed.set_thumbnail(
                    url=message.server.icon_url
                )
                await client.send_message(message.channel,embed=embed)

    if message.content == "&reset":
        if message.author.server_permissions.administrator:
            db_reset(int(message.server.id))
            embed = discord.Embed(
                description="レベル役職の設定を全てリセットしました。",
                color=discord.Color(random.randint(0,0xFFFFFF))
            )
            await client.send_message(message.channel,embed=embed)

    if message.content.startswith("&level "):
        if message.author.server_permissions.administrator:
            role = discord.utils.get(message.server.roles,name=message.content.split()[3])
            ans = db_write(
                int(message.server.id),
                int(message.content.split()[1]),
                int(message.content.split()[2]),
                role.id
            )
            if ans == True:
                embed = discord.Embed(
                    description="`『{}』役職が[{}~{}Lv]の間に設定されました。`".format(role.name,int(message.content.split()[1]),
                                                                       int(message.content.split()[2])),
                    color=discord.Color(random.randint(0,0xFFFFFF))
                )
                await client.send_message(message.channel,embed=embed)
            elif ans == -1 or ans == -2:
                embed = discord.Embed(
                    description=f"{message.author.mention}さん\nこの役職のレベルの範囲は既に設定されています...",
                    color=discord.Color(random.randint(0,0xFFFFFF))
                )
                await client.send_message(message.channel,embed=embed)
            elif ans == -3:
                embed = discord.Embed(
                    description=f"{message.author.mention}さん\nこの役職は既に設定されています...",
                    color=discord.Color(random.randint(0,0xFFFFFF))
                )
                await client.send_message(message.channel,embed=embed)
            else:
                embed = discord.Embed(
                    description="`未対応の戻り値`",
                    color=discord.Color(random.randint(0,0xFFFFFF))
                )
                await client.send_message(message.channel,embed=embed)

    if len(message.embeds) != 0:
        embed = message.embeds[0]
        if embed.get("author") and embed["author"].get("name"):
            if embed["author"]["name"][-7:] != "のステータス:":
                return
            authos = embed["author"]["name"][:-7]
            for f in embed["fields"]:
                if f["name"] == "Lv":
                    level = int(f["value"])
            member = discord.utils.get(message.server.members,display_name=authos)
            server_id = message.server.id
            role_range = []
            role_level = {}
            for lower,upper,role_id in db_read(server_id):
                role = discord.utils.get(message.server.roles,id=str(role_id))
                if role is None:
                    continue
                role_range.append((lambda x: lower <= x < upper,role.name))
                role_level[role.name] = (lower,upper)
            next_level = 0
            for _,upper in sorted(role_level.values()):
                if upper > level:
                    next_level = upper + 1
                    break
            if max([upper for _,upper in role_level.values()]) < level:
                await client.send_message(message.channel,
                                          "```凄い！あなたはこの鯖のレベル役職の付与範囲を超えてしまった！\nぜひ運営に役職を追加して貰ってください！\nこの鯖のTAOの最高レベル役職は『{}』です。```".format(
                                              role))
                return
            if role in member.roles:
                await client.send_message(message.channel,
                                          "`次のレベル役職まで後{}Lvです！`".format(int(next_level - level)))
                return
            else:
                await client.add_roles(member,role)
                await client.send_message(message.channel,
                                          "`役職名:『{0}』を付与しました。\n次のレベル役職まで後{1}Lvです！`".format(
                                              role,int(next_level - level)))
                mem = str(member.name)
                if message.content.find("役職名:"):
                    if message.author.id == "550248294551650305":
                        embed = discord.Embed(
                            title=mem + "さんが役職を更新しました！",
                            description=f"```役職名:『{role}』```",
                            color=discord.Color(random.randint(0,0xFFFFFF)),
                            timestamp=message.timestamp
                        )
                        embed.set_thumbnail(
                            url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(
                                member)
                        )
                        embed.set_footer(
                            text="役職更新時刻 :"
                        )
                        embed.set_author(
                            name=message.server.me.name
                        )
                        for channel in message.server.channels:
                            if channel.name == '役職更新ログ':
                                await client.send_message(channel,embed=embed)
                        return


def db_read(server_id):
    server_id = int(server_id)
    with closing(sqlite3.connect("MMOくん.db",isolation_level=None)) as con:
        c = con.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS roles(server_id INTEGER,lower INTEGER,upper INTEGER,role_id INTEGER)")
        c.execute('SELECT lower,upper,role_id FROM roles WHERE server_id=? ORDER BY lower',(server_id,))
        ans = c.fetchall()
        for row in ans:
            yield (row[0],row[1],row[2])


def db_reset(server_id):
    server_id = int(server_id)
    with closing(sqlite3.connect("MMOくん.db",isolation_level=None)) as con:
        c = con.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS roles(server_id INTEGER,lower INTEGER,upper INTEGER,role_id INTEGER)")
        c.execute("delete from roles where server_id=?",(server_id,))
        return True  # print("リセット完了")


def db_write(server_id,lower,upper,role_id):
    server_id = int(server_id)
    lower = int(lower)
    upper = int(upper)
    role_id = int(role_id)
    with closing(sqlite3.connect("MMOくん.db",isolation_level=None)) as con:
        c = con.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS roles(server_id INTEGER,lower INTEGER,upper INTEGER,role_id INTEGER)")
        if lower > upper:
            lower,upper = upper,lower
        c.execute('SELECT * FROM roles WHERE server_id=? AND lower<=? AND upper>=?',(server_id,lower,lower))
        if len(c.fetchall()) > 0:
            return -1  # "役職の範囲が重なっています"
        c.execute('SELECT * FROM roles WHERE server_id=? AND lower<=? AND upper>=?',(server_id,upper,upper))
        if len(c.fetchall()) > 0:
            return -2  # "役職の範囲が重なっています"
        c.execute('SELECT * FROM roles WHERE server_id=? AND role_id=?',(server_id,role_id))
        if len(c.fetchall()) > 0:
            return -3  # "役職はもう既にあります"
        c.execute("INSERT INTO roles(server_id, lower, upper, role_id) VALUES(?,?,?,?)",(server_id,lower,upper,role_id))
        return True


client.loop.create_task(change_status())
client.run(os.environ.get("TOKEN"))
