from environs import Env
# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot toekn
ADMINS =[1270439555, 952552114]
IP = env.str("ip")  # Xosting ip manzili


