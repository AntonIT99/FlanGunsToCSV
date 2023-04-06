import csv
import os

BULLET_PATH = "./bullets/"
GUN_PATH = "./guns/"


class Bullet:
    short_name: str
    damage: int
    damage_living: int
    damage_vehicle: int
    damage_plane: int
    file_name: str

    def __init__(self, file_name: str):
        self.file_name = file_name
        self.short_name = ""
        self.damage = None
        self.damage_living = None
        self.damage_vehicle = None
        self.damage_plane = None


class Gun:
    short_name: str
    shoot_delay: int
    damage: int
    file_name: str

    def __init__(self, file_name: str):
        self.file_name = file_name
        self.short_name = ""
        self.shoot_delay = None
        self.damage = None


def read_gun_file(path, file) -> Gun:
    txt_file = open(path + file, 'r')
    gun = Gun(file.split(".txt")[0])
    lines = txt_file.readlines()
    for line in lines:
        line = line.strip()
        if "//" in line or len(line.split(" ")) < 2:
            continue
        parameter = line.split(" ")[0]
        value = line.split(" ")[1]
        if parameter == "ShortName":
            gun.short_name = value
        elif parameter == "Damage":
            gun.damage = read_int(value)
        elif parameter == "ShootDelay":
            gun.shoot_delay = read_int(value)
        elif parameter == "RoundsPerMin":
            gun.shoot_delay = int(round(1200 / read_int(value)))
    return gun


def read_bullet_file(path, file) -> Bullet:
    txt_file = open(path + file, 'r')
    bullet = Bullet(file.split(".txt")[0])
    lines = txt_file.readlines()
    for line in lines:
        line = line.strip()
        if "//" in line or len(line.split(" ")) < 2:
            continue
        parameter = line.split(" ")[0]
        value = line.split(" ")[1]
        if parameter == "ShortName":
            bullet.short_name = value
        elif parameter == "Damage":
            bullet.damage = read_int(value)
        elif parameter == "DamageVsLiving":
            bullet.damage_living = read_int(value)
        elif parameter == "DamageVsVehicles":
            bullet.damage_vehicle = read_int(value)
        elif parameter == "DamageVsPlanes":
            bullet.damage_plane = read_int(value)
    return bullet


def read_int(number: str) -> int:
    return int(round(float(number)))


if __name__ == '__main__':

    try:
        files = os.listdir(BULLET_PATH)
        bullets_csv = open('bullets.csv', 'w', encoding='UTF8')
        writer = csv.writer(bullets_csv, delimiter=";", lineterminator=';\n')
        writer.writerow(["Short Name", "Damage", "DamageVsLiving", "DamageVsVehicles", "DamageVsPlanes", "File Name"])
        for filename in files:
            if ".txt" in filename:
                data = read_bullet_file(BULLET_PATH, filename)
                writer.writerow([data.short_name, data.damage, data.damage_living, data.damage_vehicle, data.damage_plane, data.file_name])
    except FileNotFoundError:
        print("No bullet files found")

    try:
        files = os.listdir(GUN_PATH)
        guns_csv = open('guns.csv', 'w', encoding='UTF8')
        writer = csv.writer(guns_csv, delimiter=";", lineterminator=';\n')
        writer.writerow(["Short Name", "Damage", "Shoot Delay", "File Name"])
        for filename in files:
            if ".txt" in filename:
                data = read_gun_file(GUN_PATH, filename)
                writer.writerow([data.short_name, data.damage, data.shoot_delay, data.file_name])
    except FileNotFoundError:
        print("No gun files found")
