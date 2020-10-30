import pygame
import random

pygame.init()

display_width = 800
display_height = 600

display = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Dyno")

clock = pygame.time.Clock()

pictures = r'pictures/'
sounds = r'sounds/'

pygame.mixer.music.load(sounds + r'untitled.mp3')
pygame.mixer.music.set_volume(0.3)

jump_sound = pygame.mixer.Sound(sounds + 'pounce-achivment.wav')

cactus_img = [pygame.image.load(pictures + r"cactus1.png"),pygame.image.load(pictures + r"cactus2.png"),pygame.image.load(pictures + r"cactus3.png")]
cactus_options = [20,430,30,450,25,420]

dino_img = [pygame.image.load(pictures + r"dinoblindmonster1.png"),pygame.image.load(pictures + r"dinoblindmonster2.png"),pygame.image.load(pictures + r"dinoblindmonster3.png"),pygame.image.load(pictures + r"dinoblindmonster5.png"),pygame.image.load(pictures + r"dinoblindmonster4.png"),pygame.image.load(pictures + r"dinoblindmonster6.png")]

stoun_img = [pygame.image.load(pictures + r"stoun1.png"),pygame.image.load(pictures + r"stoun2.png")]

cloud_img = [pygame.image.load(pictures + r"cloud1.png"),pygame.image.load(pictures + r"cloud2.png")]

jump_img = [pygame.image.load(pictures + r"dinoblindmonsterjump1.png"),pygame.image.load(pictures + r"dinoblindmonsterjump2.png")]

scores = 0
above_cactus = []
health_img = pygame.image.load(pictures + r'hp.png')
health_img = pygame.transform.scale(health_img,(30,30))

try:
    f = open('scores.txt','r')
    max_scores = int(f.readline())
    f.close()
except:
    f = open('scores.txt','w')
    f.write('0')
    max_scores = 0
    f.close()

def object_return(objects, obj):
    radius = find_radius(objects) 

    choice = random.randrange(0,3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice*2+1]

    obj.return_self(radius,height,width,img )

class Button():
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.inactive_color = (13,162,58)
        self.active_color = (23,204,58)
    def draw(self,x,y,message, action = None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if (x < mouse[0] < x + self.width):
            if (y < mouse[1] < y + self.height):
                pygame.draw.rect(display, self.active_color,(x,y,self.width,self.height))

                if (click[0]== 1 and action is not None):
                    action()
            else:
                pygame.draw.rect(display, self.inactive_color,(x,y,self.width,self.height))
        else:
            pygame.draw.rect(display, self.inactive_color,(x,y,self.width,self.height))

        print_text(message,x + 10, y + 10)

class Dino():
    def __init__(self,x=display_width // 3,y = display_height, width = 80, height = 105, image = dino_img):
        self.x = x
        self.y = y - 100 - height
        self.width = width
        self.height = height
        self.image = image

        self.img_counter = 0

        self.jump_counter = 30
        self.health = 2
        self.make_jump = False
    def hearts_plus(self, heart):
        if heart.x <= -heart.width:
            radius = display_width + random.randrange(1000,2000)
            heart.return_self(radius,random.randrange(280,450),heart.width, heart.image)

        if(self.x <= heart.x <= self.x + self.width):
            if (self.y <= heart.y + 30 <= self.y + self.height) or (self.y <= heart.y <= self.y + self.height):
                if(self.health < 3):
                    self.health += 1
                
                radius = display_width + random.randrange(2500,4000)
                heart.return_self(radius,random.randrange(280,450),heart.width, heart.image)

    def check(self,barriers):
        for barrier in barriers:
            if not self.make_jump:
                if barrier.x <= self.x + self.width - 7 <= barrier.x + barrier.width:
                    if self.check_health():
                        object_return(barriers,barrier)
                    else:
                        return True
            elif self.jump_counter >= 0:
                if self.y + self.height - 5 >= barrier.y:
                    if barrier.x <= self.x + self.width - 10 <=barrier.x + barrier.width:
                        if self.check_health():
                            object_return(barriers,barrier)
                        else:
                            return True
            else:
                if barrier.x <= self.x + self.width / 2 <= barrier.x + barrier.width:
                    if self.y + self.height - 13 >= barrier.y:
                        if self.check_health():
                            object_return(barriers,barrier)
                        else:
                            return True
                if self.y + self.height - 13 >= barrier.y:
                    if barrier.x <= self.x <=barrier.x + barrier.width:
                        if self.check_health():
                            object_return(barriers,barrier)
                        else:
                            return True
        return False

    def draw(self):
        global jump_img
        if self.jump_counter == 30:
            if self.img_counter == 60:
                self.img_counter = 0
            display.blit(self.image[self.img_counter // 10],(self.x,self.y))
            self.img_counter += 1
        else:
            if self.jump_counter > 0:
                display.blit(jump_img[0],(self.x,self.y))
            else:
                display.blit(jump_img[1],(self.x,self.y))
    def jump(self):
        global jump_sound
        if(self.jump_counter >= -30):
            if(self.jump_counter == 30):
                pygame.mixer.Sound.play(jump_sound)
            self.y -= self.jump_counter / 2.5
            self.jump_counter -= 1
        else:
            self.jump_counter = 30
            self.make_jump = False
    def check_health(self):
        self.health -= 1
        if self.health == 0:
            death_sound = pygame.mixer.Sound(sounds + 'depth.wav')
            pygame.mixer.Sound.play(death_sound)
            return False
        return True

class Object():
    def __init__(self,x,y,width, speed, image):
        self.x = x
        self.y = y
        self.width = width
        self.speed = speed
        self.image = image
    def move(self):
        if(self.x >= -self.width):
            #pygame.draw.rect(display,(224,121,31),(self.x,self.y,self.width,70))
            display.blit(self.image,(self.x,self.y))
            self.x -= self.speed
            return True
        else:
            self.x = display_width + 100 + random.randrange(-80,60)
            return False
    def return_self(self, radius, y, width, image):
        self.x = radius
        self.image = image
        self.y = y
        self.width = width
        display.blit(self.image,(self.x,self.y))

dino = Dino()

def run_game():
    global dino
    pygame.mixer.music.play(-1)
    game = True
    cactus_arr = []
    create_cactus_arr(cactus_arr)
    land = pygame.image.load(pictures + r"Land.png")
    stone,cloud = open_random_object()
    heart = Object(display_width + random.randrange(280,450), random.randrange(1000, 2000), 30, 4, health_img) 
    button = Button(50,50)
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        display.blit(land,(0,0))        
        draw_cactus_array(cactus_arr)
        move_objects(stone,cloud)
        dino.draw()
        print_text("scores:" + str(scores),700,10)
        button.draw(20,70,"wow",None)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            dino.make_jump = True
        if keys[pygame.K_ESCAPE]:
            pause()

        if dino.make_jump:
            dino.make_jump = True
            dino.jump()
            
        #pygame.draw.rect(display,(247,240,22),(user_x,user_y,user_width - 10,user_height))
        
        clock.tick(80)
        if dino.check(cactus_arr):
                #pygame.mixer.music.stop()
            game = False
        count_scores(cactus_arr,dino)
        print_text("scores:" + str(scores),700,10)
        heart.move()
        dino.hearts_plus(heart)
        show_health()

        pygame.display.update()
    return game_over()

def show_health():
    global dino
    show = 0
    x = 20
    while show != dino.health:
        display.blit(health_img,(x, 20))
        x += 30
        show += 1

def count_scores(barriers, user):
    global scores, above_cactus
    for barrier in barriers:
        if user.y + user.height - 5 <= barrier.y:
            if barrier.x <= user.x <= barrier.x + barrier.width:
                if barrier not in above_cactus:
                    above_cactus.append(barrier)
    if user.jump_counter == -30:
        scores += len(above_cactus)
        above_cactus.clear()
   
def create_cactus_arr(array):
    choice = random.randrange(0,3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice*2+1]
    array.append(Object(display_width + 50, height, width, 4, img))

    choice = random.randrange(0,3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice*2+1]
    array.append(Object(display_width + 300, height,  width, 4, img))

    choice = random.randrange(0,3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice*2+1]
    array.append(Object(display_width + 600, height, width, 4, img))

def find_radius(array):
    maximum = max(array[0].x,array[1].x,array[2].x)
    if (maximum < display_width):
        radius = display_width
        if( radius - maximum < 50):
            radius += 150
    else:
        radius = maximum

    choice = random.randrange(0,5)
    if (choice == 0):
        radius += random.randrange(10,15)
    else:
        radius += random.randrange(250,370)
    return radius

def draw_cactus_array(array):
    for cactus in array:
        check = cactus.move()
        if(not check):
            object_return(array,cactus)

def open_random_object():
    choice = random.randrange(0,2)
    st_img = stoun_img[choice]
    choice = random.randrange(0,2)
    cl_img = cloud_img[choice]

    stone = Object(display_width, display_height - 80, 10, 4,st_img)
    cloud = Object(display_width, 80, 60, 2,cl_img)

    return stone, cloud

def move_objects(stone,cloud):
    check = stone.move()
    if(not check):
        choice = random.randrange(0,2)
        stone_im = stoun_img[choice]
        stone.return_self(display_width, 500 + random.randrange(10,80),stone.width, stone_im)
    check = cloud.move()
    if(not check):
        choice = random.randrange(0,2)
        cloud_im = cloud_img[choice]
        cloud.return_self(display_width, random.randrange(10,200),cloud.width, cloud_im)

def print_text(message,x,y, font_color = (0,0,0), font_type = 'shrift.ttf', font_size = 30):
    font_type = pygame.font.Font(font_type,font_size)
    text = font_type.render(message, True, font_color)
    display.blit(text,(x,y))

def pause():
    paused = True

    pygame.mixer.music.pause()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        print_text('Paused. Enter to continue',315,250)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
            paused = False
        pygame.display.update()
        clock.tick(15)
    pygame.mixer.music.unpause()

def game_over():
    global scores, max_scores
    pygame.mixer.music.stop()
    if scores > max_scores:
        f = open('scores.txt','w')
        max_scores = scores
        f.write(str(max_scores))
        f.close()
    stopped = True
    while stopped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
            
        print_text('Game Over. Press enter to play game or esc to exit',200,260)
        print_text('Max score : ' + str(max_scores),330,290)
        print_text('Your score : ' + str(scores),330,320)
        if keys[pygame.K_ESCAPE]:
            return False
        if keys[pygame.K_RETURN]:
            return True

        pygame.display.update()
        clock.tick(15)

while run_game():
    dino.jump_counter = 30
    dino.make_jump = False
    dino.y = display_height - 205
    scores = 0
    dino.health = 2
    

pygame.quit()
quit()