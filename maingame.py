from classes import *

backgr_map = Background("floor.bmp")
backgr_map.objects.append(tardis)

theme = pygame.mixer.Sound(sound_dir+"theme.wav")
theme.set_volume(0.1)
theme.play()

while 1:
    rect_bases = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            theme.stop()
        elif event.type == pygame.KEYDOWN:
            temprects = []
            if event.key == pygame.K_RETURN:
                m, selection = show_menu(menu1)
                if m == 1:
                    pygame.display.quit()
                    theme.stop()
                else:
                    continue
            elif event.key == pygame.K_UP:
                doctor.face_direction("up")
                newpos = [0, tile]
                dir = "up"
                if doctor.base.topright == tardis.rect.bottomright:
                    backgr_map.move(newpos)
                    for obj in backgr_map.objects:
                        obj.move(newpos)
                    tardis.close_door()
                    update_screen(backgr_map, doctor)
                    new_map = transport()
                    if new_map != -1:
                        backgr_map = new_map
                    continue
            elif event.key == pygame.K_DOWN:
                doctor.face_direction("down")
                newpos = [0, -tile]
                dir = "down"
            elif event.key == pygame.K_LEFT:
                newpos = [tile, 0]
                dir = "left"
            elif event.key == pygame.K_RIGHT:
                newpos = [-tile, 0]
                dir = "right"
            for obj in backgr_map.objects:
                rect_bases.append(obj.base.move(newpos))
            map_move = backgr_map.rect.move(newpos)
            if map_move.contains(doctor.base):
                obstacle = doctor.base.collidelist(rect_bases)
                if obstacle == -1:
                    move_map(backgr_map, doctor, newpos, dir)
                    if dir == "up" or dir == "down":
                        doctor.face_direction(dir)
                elif backgr_map.objects[obstacle] != tardis:
                    opponent = backgr_map.objects[obstacle]
                    if opponent.name == "DALEK":
                        win = fight(doctor, opponent)
                    else:
                        win = argue(doctor, opponent, 50.0, 50.0)
                    if win == True:
                        backgr_map.objects.remove(opponent)
                    elif win == False:
                        game_over()
                    doctor.rect.bottomleft = doctor.base.bottomleft
                    opponent.rect.bottomleft = opponent.base.bottomleft
        
        # Re-writing the various images to the screen at the end of every loop
        update_screen(backgr_map, doctor)
