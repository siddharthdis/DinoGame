from ursina import *
app = Ursina(
    title='Jurassic Run',
    icon = 'icon1.ico',
    borderless=False,
    fullscreen = False,    
)
initialised = False
global gameover
gameover = False
def windowinit():
    window.icon = 'icon1.ico'
    window.entity_counter.enabled = False
    window.fps_counter.enabled = False
    window.exit_button.visible = False
    app.development_mode = False
    window.collider_counter.enabled = False
    window.fullscreen = True
def splash():
    camera.overlay.color = color.black
    logo = Sprite(name='ursina_splash', parent=camera.ui, texture='splash', world_z=camera.overlay.z-1, scale=.15, color=color.clear)
    logo.animate_color(color.white, duration=2, delay=1, curve=curve.out_quint_boomerang)
    camera.overlay.animate_color(color.clear, duration=1, delay=4)
    destroy(logo, delay=5)

    def splash_input(key):
        destroy(logo)
        camera.overlay.animate_color(color.clear, duration=.25)

    logo.input = splash_input
def login():
    background = Entity(parent=camera.ui, model='quad', texture='shore', scale=(1.7777, 1), z=1)
    logintxt = Text(text='Login',color = color.black, y=0, scale=2, origin=(0,0))
    username_field = InputField(y=-.12)
    password_field = InputField(y=-.18, hide_content=True)
    username_field.next_field = password_field
    
    def submit():
        if username_field.text == 'gamer' and password_field.text == '123456':
            destroy(background)
            destroy(logintxt)
            destroy(username_field)
            destroy(password_field)
            destroy(btn)
            menu()
            
        else:
            logintxt.text = 'Login\n\nIncorrect username or password'
    
    btn=(Button('Login', scale=(0.1,0.05), color=color.cyan.tint(-.4), y=-.26,on_click=submit))

def menu():
    global bg
    global menutxt
    global btn1
    # global btn2
    global btn3
    try:
        destroy(menutxt)
    except:
        pass
    bg = Entity(parent=camera.ui, model='quad',color = color.gray, texture='bg', scale=(1.7777, 1), z=1)
    menutxt = Text(text='Jurassic Run',color = color.white, y=0.3, scale=4, origin=(0,0))
    btn1 = Button('Play', scale=(0.5,0.05), color=color.cyan.tint(-.4), y=-.06, on_click=Func(loading,run))
    # btn2 = Button('Settings', scale=(0.5,0.05), color=color.cyan.tint(-.4), y=-.12)
    btn3 = Button('Quit', scale=(0.5,0.05), color=color.cyan.tint(-.4), y=-.18, on_click=application.quit)

def loading(inv):
    global bg
    global menutxt
    global btn1
    # global btn2
    global btn3
    destroy(bg)
    destroy(menutxt)
    destroy(btn1)
    # destroy(btn2)
    destroy(btn3)
    bg = Entity(parent=camera.ui, model='quad',color = color.white, texture='loading', scale=(2, 4),y = 0.2, z=1)
    menutxt = Text(text='Loading...',color = color.white, y=0.3, scale=4, origin=(0,0))
    invoke(inv, delay=3)

def run():
    global initialised
    
    destroy(bg)
    destroy(menutxt)
    destroy(btn1)
    # destroy(btn2)
    destroy(btn3)
    camerainit()
    playerinit()
    floorinit()
    initialised = True
    
def camerainit():
    camera.orthographic = True
    camera.position = (0,0,-2)
    camera.rotation_x = 0
    camera.rotation_y = 0
    camera.rotation_z = 0
    camera.fov = 20
    Sky(color=color.white, texture='sky_sunset')
    EditorCamera()


def playerinit():
    global dyno
    global y
    global g
    global groundray
    global cactus1
    global speed
    global cactus2
    global cac1pas
    global fr
    global cac2pas
    global scr
    global score
    fr = 0
    y = 0
    cac1pas = False
    cac2pas = False
    
    speed = 0.2
    g = -0.1
    scr = 0
    score = Text(text=f'Score: {scr}',color = color.black, y=0.3, scale=1, origin=(0.5,0.5))
    dyno = Entity(model='cube', scale=(1.5, 1.5, 1), position=(-15, 0, 0),texture='dynomain')
    cactus1 = Entity(model='cube', scale=(1.5, 1.5, 1), position=(20, -0.25, 0),color=color.gray,texture='cactus',collider='box')
    cactus2 = Entity(model='cube', scale=(1.5, 1.5, 1), position=(35, -0.25, 0),color=color.gray,texture='cactus',collider='box')
    
def floorinit():
    global floor
    floor = Entity(model='cube', color=color.black90, scale=(40, 0.1, 1), position=(0, -1, 0))
    floor.collider = 'box'


def update():
    global y
    global g
    global dyno
    global speed
    global cac1pas 
    global cac2pas
    global cactus1
    global initialised 
    global cactus2
    global scr
    global fr
    global score
    
    if initialised:
        groundray = raycast(dyno.position, direction=(0, -1, 0), distance=0.77, ignore=(dyno,))
        if groundray.hit:
            g = 0
            y = 0 
            dyno.y = -0.2
        if (held_keys['space'] or held_keys['left mouse']) and groundray.hit and groundray.entity == floor:
            g = -0.01
            y = 0.2563 
        
        y += g
        dyno.y += y
        downray = raycast(dyno.position, direction=(0, -1, 0), distance=30, ignore=(dyno,))
        cactus1.x -= speed
        cactus2.x -= speed
        fr += 1
        if not groundray.hit:
            dyno.texture = 'dynomain.png'
        elif fr %20 == 0:
            dyno.texture = 'dyno1.png'
        elif fr %20 == 10:
            dyno.texture = 'dyno2.png'
        if downray.hit and downray.entity == cactus1 or downray.entity == cactus2:
            
            if downray.entity == cactus1:
                cac1pas = True
            if downray.entity == cactus2:
                cac2pas = True
        if cac1pas == True and cactus1.x < -20:
            cactus1.x = 20+scr*2/3
            cac1pas = False
            scr += 1
            score.text = f'Score: {scr*20}'
            speed += 0.01
        if cac2pas == True and cactus2.x < -20:
            cactus2.x = 20+scr*2/3
            cac2pas = False
            scr += 1
            score.text = f'Score: {scr*20}'
            speed += 0.01
        
        feetray = raycast((dyno.x,dyno.y-0.7,dyno.z), direction=(0, 0, 0), distance=0.77, ignore=(dyno,))
        if feetray.hit and feetray.entity == cactus1 or feetray.entity == cactus2:
            initialised = False
            score.text = f'Game Over\nScore: {scr*20}\nPress R to restart'
            global gameover
            gameover = True
    try:
        if gameover == True and held_keys['r']:
            destroy(dyno)
            destroy(cactus1)
            destroy(cactus2)
            destroy(floor)
            destroy(score)
            camerainit()
            playerinit()
            floorinit()
            initialised = True
    except:
        pass
def input(key):
    global initialised
    if key == 'escape' and initialised:
        destroy(dyno)
        destroy(cactus1)
        destroy(cactus2)
        destroy(floor)
        destroy(score)
        initialised = False
        loading(menu)

    elif key == 'escape' and not initialised:
        application.quit()

windowinit()
splash()
login()

app.run()
