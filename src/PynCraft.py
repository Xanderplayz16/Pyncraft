from ursina import *
from ursina.color import *
from ursina.prefabs.first_person_controller import FirstPersonController
from VoxelTypes import *
from Objects import *
from WorldGeneration import GenerateWorld, World
from utils import get_current_commit_hash
import configparser
import json

app = Ursina()



def input(key):
    if key == 'right mouse down':
        hit_info = raycast(camera.world_position, camera.forward, distance=5)
        if hit_info.hit:
            try:
                Voxel(Block=hotbar.items[hotbar.selected_slot].block, position=hit_info.entity.position + hit_info.normal)
            except AttributeError:
                print("Placed nil block")
    if key == 'left mouse down' and mouse.hovered_entity:
        hit_info = raycast(camera.world_position, camera.forward, distance=5)
        if hit_info.hit:
            destroy(mouse.hovered_entity)
    if key == "escape" and pause_menu.enabled:
        pause_menu.close_menu()
        mouse.locked = True
    elif key == "escape":
        pause_menu.enabled = True
        mouse.locked = False
        player.enabled = False
    for i in range(10):
        if held_keys[str(i+1)]:
            hotbar.select_slot(i)
    print(f"Key {key} pressed")

def update():
    nllu = 0

ver = "0.1"


config = configparser.ConfigParser()
config.read('conf.ini')

player = FirstPersonController()
if config['Camera']['Orthographic'] == "True":
    print("Crosshair disabled")
else:
    crosshair = Crosshair()


window.title = 'PynCraft' 
window.show_ursina_splash = False
player.cursor = False

camera.orthographic = config['Camera']['Orthographic'] == "True"
camera.fov = config['Camera']['FOV']  # Adjust the field of view as needed
camera.clip_plane_far = config['Camera']['ClipPlaneFar']

pause_menu = PauseMenu(player)
hotbar = Hotbar(num_slots=10)
text_entity = Text(text=f"Pyncraft {ver}-{get_current_commit_hash()[:5]}", x=0, y=0.5, scale=1, color=white)




hotbar.add_item(cobblestone().item, 128, 0)
hotbar.add_item(dirt().item, 128, 1)
hotbar.add_item(cobblestonesphere().item, 128, 2)




print(save_class(GenerateWorld(1), "wrld.pk1"))


app.run()