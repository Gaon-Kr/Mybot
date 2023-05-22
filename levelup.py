import discord
from discord.ext import commands
from pymongo import MongoClient

class LevelUp(commands.Cog):
    def __init__(self, client):
        self.bot = client
        self.base_exp = 10 # 레벨 업에 필요한 기본 경험치
        self.exp_increment = 5  # 레벨당 추가 경험치량

        # MongoDB 클라이언트 연결
        mongo_connection_string = "mongodb+srv://Gaon_0901:Aszx1122..@gameserver.7srangt.mongodb.net/"
        self.mongo_client = MongoClient(mongo_connection_string)
        self.db = self.mongo_client['level_up_db']
        self.user_data_collection = self.db['user_data']

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:  # 봇의 메시지는 무시
            return

        author_id = str(message.author.id)
        user_data = self.user_data_collection.find_one({"_id": author_id})

        if user_data is None:
            # 사용자 데이터가 없을 경우 생성
            user_data = {"_id": author_id, "count": 1, "level": 1}
            self.user_data_collection.insert_one(user_data)
        else:
            # 채팅 수 증가
            self.user_data_collection.update_one({"_id": author_id}, {"$inc": {"count": 1}})

        # 레벨 체크 및 처리
        count = self.user_data_collection.find_one({"_id": author_id})["count"]
        level = self.user_data_collection.find_one({"_id": author_id})["level"]
        if count >= self.get_level_up_threshold(level):
            self.user_data_collection.update_one({"_id": author_id}, {"$set": {"count": 0, "level": level + 1}})
            await message.channel.send(f"축하합니다! 레벨이 {level + 1}로 올라갔습니다.")

    def get_level_up_threshold(self, level):
        return self.base_exp + (self.exp_increment * (level - 1))

    @commands.command()
    async def 레벨(self, ctx):
        author_id = str(ctx.author.id)
        user_data = self.user_data_collection.find_one({"_id": author_id})

        if user_data is None:
            level = 1
            remaining_exp = self.get_level_up_threshold(level)
        else:
            level = user_data["level"]
            count = user_data["count"]
            remaining_exp = self.get_level_up_threshold(level) - count

        embed = discord.Embed(title="레벨", description=f"당신의 현재 레벨은 {level}입니다.", color=discord.Color.green())
        embed.add_field(name="다음 레벨까지 남은 경험치", value=f"{remaining_exp}입니다.")
        await ctx.send(embed=embed)

    @commands.command()
    async def db(self, ctx):
        author_id = str(ctx.author.id)

        # 허용된 유저만 데이터 확인
        allowed_users = ["765545657242353714"]  # 허용된 유저 아이디 목록
        if author_id not in allowed_users:
            await ctx.send("권한이 없습니다.")
            return

        data = self.user_data_collection.find()
        result = []
        for item in data:
            count = item["count"]
            level = item["level"] + (count // self.get_level_up_threshold(item["level"]))
            count %= self.get_level_up_threshold(item["level"])
            result.append(f"유저 아이디: {item['_id']}, 레벨: {level} (<@유저아이디>입력시 멘션이 됨 무조건 <> 해당 기호를 붙일 것.)")

        if result:
            await ctx.send("\n".join(result))
        else:
            await ctx.send("데이터가 없습니다.")

    @commands.command()
    async def dbclear(self, ctx):
        author_id = str(ctx.author.id)

        # 허용된 유저만 DB 초기화 가능
        allowed_users = ["765545657242353714"]  # 허용된 유저 아이디 목록
        if author_id not in allowed_users:
            await ctx.send("권한이 없습니다.")
            return

        message = await ctx.send("진짜로 db를 초기화 하시겠습니까?")
        await message.add_reaction("✅")  # 체크 이모지
        await message.add_reaction("❌")  # 엑스 이모지

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["✅", "❌"]

        try:
            reaction, _ = await self.bot.wait_for("reaction_add", timeout=60.0, check=check)
        except TimeoutError:
            await ctx.send("응답 시간이 초과되었습니다. 초기화를 취소합니다.")
        else:
            if str(reaction.emoji) == "✅":
                self.user_data_collection.delete_many({})
                await ctx.send("DB가 초기화되었습니다.")
            else:
                await ctx.send("초기화가 취소되었습니다.")

def setup(client):
    client.add_cog(LevelUp(client))
