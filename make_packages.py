import git
import subprocess
import shutil
import os

token = "bb8czxqpbkzn5PHp3nda"
# git = Git(self)
repo_url = f"https://oauth2:{token}@git.orlan.in/breo_mcu/drivers/CMSIS_5.git"

# subprocess.run("rm -r ./cmsis", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
# repo = git.Repo(repo_url)
# Удаление папки, если она существует
if os.path.exists("./cmsis"):
    print(f"Удаление папки ./cmsis...")
    shutil.rmtree("./cmsis")
    print(f"Папка ./cmsis удалена.")
else:
    print(f"Папка ./cmsis не существует.")

repo = git.Repo.clone_from(repo_url, "./cmsis")
tags = repo.tags
print("tag: ", tags)
for tag in tags:
    comand = f"export URL=\"{repo_url}\" && export TAG=\"{tag}\" && conan create . --version={str(tag).lower()} --build-require"
    print(comand)
    result = subprocess.run(comand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode == 0:
        comand = f" conan upload cmsis/{tag} -r=BREO"
        result = subprocess.run(comand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("Команда завершилась успешно")
        print("Вывод команды:", result.stdout)
    if result.returncode !=0:
        print("Команда завершилась с ошибкой")
        print("Ошибка:", result.stderr)
        # raise ValueError(f"сборка пакета не удалась, почините скрипт сборки")


#export URL="https://oauth2:bb8czxqpbkzn5PHp3nda@git.orlan.in/breo_mcu/drivers/CMSIS_5.git" && export TAG="5.9.1-dev" && conan create . --version=5.9.1-dev --build-require
#conan upload cmsis/5.9.1-dev -r=BREO

