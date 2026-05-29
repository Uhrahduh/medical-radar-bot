from config import TOKEN

print("BOT INICIANDO")
print("TOKEN:", TOKEN)

if TOKEN is None:
    print("ERROR: TOKEN NO CONFIGURADO")
    exit(1)
