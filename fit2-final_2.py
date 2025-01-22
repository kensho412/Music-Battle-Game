import pyxel
import time
import pygame
import random

#BPMとか
class Data:
    def __init__(self):
        self.BPM = 180 * 16
        self.beat_counter = 0
        self.sbeat = 1
        self.ebeat = 1
        self.fbeat = 1
        self.bar = 0
        self.score1 = 0
        self.score2 = 0

        self.gen = set()

    def update(self):
        self.beat_counter += self.BPM / 60 /180
        if self.beat_counter >= 1:
            self.beat_counter -= 1
            self.sbeat += 1
        if self.sbeat > 4:  
            self.sbeat = 1
            self.ebeat += 1
        if self.ebeat > 4:
            self.ebeat = 1
            self.fbeat += 1
        if self.fbeat > 4:
            self.fbeat = 1
            self.bar += 1
            
    def draw(self):
        pyxel.text(5,5,f"{self.score1}",7)
        pyxel.text(205,5,f"{self.score2}",7)
        pyxel.text(1,312,"Q",6)
        pyxel.text(52,312,"W",6)
        pyxel.text(103,312,"E",6)
        pyxel.text(154,312,"R",6)
        pyxel.text(206,312,"U",6)
        pyxel.text(52+205,312,"I",6)
        pyxel.text(103+205,312,"O",6)
        pyxel.text(154+205,312,"P",6)

class Music:
    def __init__(self,filename):
        pygame.mixer.init()
        self.filename = filename
        self.is_playing = False
        self.start_time = None

    def play(self):
        if not self.is_playing:
            pygame.mixer.music.load(self.filename)
            pygame.mixer.music.play(1)
            self.is_playing = True

    def delayplay(self,delay):
        self.start_time = time.time() + delay

    def try_play(self):
        if self.start_time and time.time() >= self.start_time and not self.is_playing:
            self.play()

    def stopped(self):
        return not pygame.mixer.music.get_busy()
    
    def stop(self):
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False

class Bar:
    def __init__(self):
        self.y = 10

    def move(self):
        self.y += 300 / 200

    def draw(self):
        pyxel.rect(0, self.y, 406, 1, 6)

    def set(data,f,e,s):
        current_key = (f,e,s)
        if f == data.fbeat and e == data.ebeat and s == data.sbeat:
            if current_key not in data.gen:
                data.gen.add(current_key)
                return[Bar()]
        if f + 1 == data.fbeat:
            data.gen.discard(current_key)
        return[]
    

#ノート
class Notes:
    def __init__(self,x):
        self.x = x
        self.y = 0
        self.gen = False

    def move(self):
        self.y += 300 /200

    def draw(self):
        pyxel.rect(self.x, self.y, 50, 10, 11)

    def judge(self, data, feedback_list):
        key_map = {
            0: (pyxel.KEY_Q, 10, 295),
            51: (pyxel.KEY_W, 61, 295),
            102: (pyxel.KEY_E, 112, 295),
            153: (pyxel.KEY_R, 163, 295),
            205: (pyxel.KEY_U, 215, 295),
            256: (pyxel.KEY_I, 266, 295),
            307: (pyxel.KEY_O, 317, 295),
            358: (pyxel.KEY_P, 368, 295),
        }

        if self.x in key_map and pyxel.btnp(key_map[self.x][0]):
            feedback_x, feedback_y = key_map[self.x][1], key_map[self.x][2]

            if 270 < self.y + 10 <= 280 or 315 <= self.y + 10 < 320:
                score_to_add = 3
                feedback_text, feedback_color = "bad", 12  
            elif 280 < self.y + 10 <= 290 or 310 <= self.y + 10 < 315:
                score_to_add = 5
                feedback_text, feedback_color = "good", 9  
            elif 290 < self.y + 10 < 310:
                score_to_add = 10
                feedback_text, feedback_color = "perfect", 10  
            else:
                return  

            if self.x < 205:
                data.score1 += score_to_add
            else:
                data.score2 += score_to_add

            feedback_list.append(Feedback(feedback_x, feedback_y, feedback_text, feedback_color))

            return True
        return False
    def set(data,b,f,e,s,position):
        current_key = (b,f,e,s,position)
        if b == data.bar and f == data.fbeat and e == data.ebeat and s == data.sbeat:
            if current_key not in data.gen:
                data.gen.add(current_key)
                return[Notes(position),Notes(position + 205)]
        return[]

class Attack:
    def __init__(self,ax):
        self.ax = ax
        self.ay = 0
        self.perfect1 = False
        self.perfect2 = False

    def move(self):
        self.ay += 300 /200

    def draw(self):
        pyxel.rect(self.ax,self.ay,50,10,10)

    def judge(self, data, feedback_list):
        key_map = {
            0: (pyxel.KEY_Q, 10, 295),
            51: (pyxel.KEY_W, 61, 295),
            102: (pyxel.KEY_E, 112, 295),
            153: (pyxel.KEY_R, 163, 295),
            205: (pyxel.KEY_U, 215, 295),
            256: (pyxel.KEY_I, 266, 295),
            307: (pyxel.KEY_O, 317, 295),
            358: (pyxel.KEY_P, 368, 295),
        }

        if self.ax in key_map and pyxel.btnp(key_map[self.ax][0]):
            feedback_x, feedback_y = key_map[self.ax][1], key_map[self.ax][2]

            if 270 < self.ay + 10 <= 280 or 315 <= self.ay + 10 < 320:
                score_to_add = 3
                feedback_text, feedback_color = "bad", 12  
            elif 280 < self.ay + 10 <= 290 or 310 <= self.ay + 10 < 315:
                score_to_add = 5
                feedback_text, feedback_color = "good", 9  
            elif 290 < self.ay + 10 < 310:
                score_to_add = 10
                feedback_text, feedback_color = "perfect", 10  
                if self.ax < 205:
                    self.perfect2 = True
                else:
                    self.perfect1 = True
            else:
                return  

            if self.ax < 205:
                data.score1 += score_to_add     
            else:
                data.score2 += score_to_add
 
            feedback_list.append(Feedback(feedback_x, feedback_y, feedback_text, feedback_color))
            return True
        return False
    def set(data,b,f,e,s,position):
        current_key = (b,f,e,s,position)
        if b == data.bar and f == data.fbeat and e == data.ebeat and s == data.sbeat:
            if current_key not in data.gen:
                data.gen.add(current_key)
                return[Attack(position),Attack(position + 205)]
        return[]

class Penalty:
    def __init__(self,x):
        self.x = x
        self.y = 0
        self.miss = False

    def move(self):
        self.y += 300 /200

    def draw(self):
        pyxel.rect(self.x, self.y, 50, 10, 8)

    def judge(self, data, feedback_list):
        key_map = {
            0: (pyxel.KEY_Q, 10, 295),
            51: (pyxel.KEY_W, 61, 295),
            102: (pyxel.KEY_E, 112, 295),
            153: (pyxel.KEY_R, 163, 295),
            205: (pyxel.KEY_U, 215, 295),
            256: (pyxel.KEY_I, 266, 295),
            307: (pyxel.KEY_O, 317, 295),
            358: (pyxel.KEY_P, 368, 295),
        }

        if self.x in key_map and pyxel.btnp(key_map[self.x][0]):
            feedback_x, feedback_y = key_map[self.x][1], key_map[self.x][2]

            if 270 < self.y + 10 <= 280 or 315 <= self.y + 10 < 320:
                score_to_add = -10
                feedback_text, feedback_color = "bad", 12  
            elif 280 < self.y + 10 <= 290 or 310 <= self.y + 10 < 315:
                score_to_add = 0
                feedback_text, feedback_color = "good", 9  
            elif 290 < self.y + 10 < 310:
                score_to_add = 0
                feedback_text, feedback_color = "perfect", 10  
            else:
                return  

            if self.x < 205:
                data.score1 += score_to_add
            else:
                data.score2 += score_to_add

            feedback_list.append(Feedback(feedback_x, feedback_y, feedback_text, feedback_color))
            return True
        
        if self.y + 10 > 320 and not self.miss:
            self.miss = True
            score_to_add = -10
            if self.x < 205:
                data.score1 += score_to_add
                score_to_add = 0
            else:
                data.score2 += score_to_add
                score_to_add = 0

        return False
    
    def set(data,b,f,e,s,position,attack_list):
        penalties = []
        current_key = (b,f,e,s,position)
        if b == data.bar and f == data.fbeat and e == data.ebeat and s == data.sbeat:
            if current_key not in data.gen:
                data.gen.add(current_key)
                for atk in attack_list:
                    if atk.perfect1:
                        atk.perfect1 = False
                        penalties.append(Penalty(position))
                    if atk.perfect2:
                        atk.perfect2 = False
                        penalties.append(Penalty(position + 205))
        return penalties


class Feedback:
    def __init__(self, x, y, text, color):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.start_time = time.time()

    def draw(self):
        if time.time() - self.start_time <= 0.5:
            pyxel.text(self.x, self.y, self.text, self.color)

class App():
    def __init__(self):
        pyxel.init(406,320,fps=180)

        self.data = Data()

        self.notes = []
        self.notes = [note for note in self.notes if note[1] < 300]

        self.attack = []
        self.attack = [atk for atk in self.attack if atk[1] < 300]

        self.penalty = []
        self.penalty = [pen for pen in self.penalty if pen[1] < 300]

        self.feedback_list = []
        self.music = Music("zeropoint.mp3")

        self.bar = []
        self.bar = [b for b in self.bar if b[1] < 300]

        self.result = []

        pyxel.run(self.update,self.draw)

    def update(self):
        self.data.update()

        if self.data.bar == 1 and self.music.start_time is None:
            self.music.delayplay(1)

        self.music.try_play()


        self.bar.extend(Bar.set(self.data,1,1,1))

        r = random.choice([0,51,102,153])

        #Notes配置
        #0,51,102,153

        #intro
        self.attack.extend(Attack.set(self.data,1,1,1,1,0))
        self.notes.extend(Notes.set(self.data,1,2,1,1,51))
        self.attack.extend(Attack.set(self.data,1,3,1,1,102))
        self.notes.extend(Notes.set(self.data,1,4,1,1,153))

        self.notes.extend(Notes.set(self.data,2,1,1,1,0))
        self.penalty.extend(Penalty.set(self.data,2,1,3,1,r,self.attack))
        self.attack.extend(Attack.set(self.data,2,2,1,1,153))
        self.notes.extend(Notes.set(self.data,2,3,1,1,102))
        self.penalty.extend(Penalty.set(self.data,2,3,3,1,r,self.attack))
        self.attack.extend(Attack.set(self.data,2,4,1,1,51))

        self.notes.extend(Notes.set(self.data,3,1,1,1,0))
        self.penalty.extend(Penalty.set(self.data,3,1,3,1,r,self.attack))
        self.attack.extend(Attack.set(self.data,3,2,1,1,102))
        self.notes.extend(Notes.set(self.data,3,3,1,1,51))
        self.penalty.extend(Penalty.set(self.data,3,3,3,1,r,self.attack))
        self.attack.extend(Attack.set(self.data,3,4,1,1,153))
        
        self.notes.extend(Notes.set(self.data,4,1,1,1,102))
        self.penalty.extend(Penalty.set(self.data,4,1,3,1,r,self.attack))
        self.attack.extend(Attack.set(self.data,4,2,1,1,51))
        self.notes.extend(Notes.set(self.data,4,3,1,1,153))
        self.penalty.extend(Penalty.set(self.data,4,3,3,1,r,self.attack))
        self.attack.extend(Attack.set(self.data,4,4,1,1,0))
        

        self.attack.extend(Attack.set(self.data,5,1,1,1,0))
        self.penalty.extend(Penalty.set(self.data,5,1,3,1,r,self.attack))
        self.notes.extend(Notes.set(self.data,5,2,1,1,51))
        self.attack.extend(Attack.set(self.data,5,3,1,1,102))
        self.penalty.extend(Penalty.set(self.data,5,3,3,1,r,self.attack))
        self.notes.extend(Notes.set(self.data,5,4,1,1,153))

        self.notes.extend(Notes.set(self.data,6,1,1,1,0))
        self.penalty.extend(Penalty.set(self.data,6,1,3,1,r,self.attack))
        self.attack.extend(Attack.set(self.data,6,2,1,1,153))
        self.notes.extend(Notes.set(self.data,6,3,1,1,102))
        self.penalty.extend(Penalty.set(self.data,6,3,3,1,r,self.attack))
        self.attack.extend(Attack.set(self.data,6,4,1,1,51))

        self.notes.extend(Notes.set(self.data,7,1,1,1,0))
        self.penalty.extend(Penalty.set(self.data,7,1,3,1,r,self.attack))
        self.attack.extend(Attack.set(self.data,7,2,1,1,102))
        self.notes.extend(Notes.set(self.data,7,3,1,1,51))
        self.penalty.extend(Penalty.set(self.data,7,3,3,1,r,self.attack))
        self.attack.extend(Attack.set(self.data,7,4,1,1,153))
        
        self.notes.extend(Notes.set(self.data,8,1,1,1,102))
        self.penalty.extend(Penalty.set(self.data,8,1,3,1,r,self.attack))
        self.attack.extend(Attack.set(self.data,8,2,1,1,51))
        self.notes.extend(Notes.set(self.data,8,3,1,1,153))
        self.penalty.extend(Penalty.set(self.data,8,3,3,1,r,self.attack))
        self.attack.extend(Attack.set(self.data,8,4,1,1,0))


        self.attack.extend(Attack.set(self.data,9,1,1,1,0))
        self.penalty.extend(Penalty.set(self.data,9,1,3,1,r,self.attack))
        self.notes.extend(Notes.set(self.data,9,2,1,1,51))
        self.attack.extend(Attack.set(self.data,9,3,1,1,102))
        self.penalty.extend(Penalty.set(self.data,9,3,3,1,r,self.attack))
        self.notes.extend(Notes.set(self.data,9,4,1,1,153))

        self.notes.extend(Notes.set(self.data,10,1,1,1,0))
        self.penalty.extend(Penalty.set(self.data,10,1,3,1,r,self.attack))
        self.attack.extend(Attack.set(self.data,10,2,1,1,153))
        self.notes.extend(Notes.set(self.data,10,3,1,1,102))
        self.penalty.extend(Penalty.set(self.data,10,3,3,1,r,self.attack))
        self.attack.extend(Attack.set(self.data,10,4,1,1,51))

        self.notes.extend(Notes.set(self.data,11,1,1,1,0))
        self.penalty.extend(Penalty.set(self.data,11,1,3,1,r,self.attack))
        self.attack.extend(Attack.set(self.data,11,2,1,1,102))
        self.notes.extend(Notes.set(self.data,11,3,1,1,51))
        self.penalty.extend(Penalty.set(self.data,11,3,3,1,r,self.attack))
        self.attack.extend(Attack.set(self.data,11,4,1,1,153))
        
        self.notes.extend(Notes.set(self.data,12,1,1,1,102))
        self.penalty.extend(Penalty.set(self.data,12,1,3,1,r,self.attack))
        self.attack.extend(Attack.set(self.data,12,2,1,1,51))
        self.notes.extend(Notes.set(self.data,12,3,1,1,153))
        self.penalty.extend(Penalty.set(self.data,12,3,3,1,r,self.attack))
        self.attack.extend(Attack.set(self.data,12,4,1,1,0))


        self.attack.extend(Attack.set(self.data,13,1,1,1,0))
        self.penalty.extend(Penalty.set(self.data,13,1,3,1,r,self.attack))
        self.notes.extend(Notes.set(self.data,13,2,1,1,51))
        self.attack.extend(Attack.set(self.data,13,3,1,1,102))
        self.penalty.extend(Penalty.set(self.data,13,3,3,1,r,self.attack))
        self.notes.extend(Notes.set(self.data,13,4,1,1,153))

        self.notes.extend(Notes.set(self.data,14,1,1,1,0))
        self.penalty.extend(Penalty.set(self.data,14,1,3,1,r,self.attack))
        self.attack.extend(Attack.set(self.data,14,2,1,1,153))
        self.notes.extend(Notes.set(self.data,14,3,1,1,102))
        self.penalty.extend(Penalty.set(self.data,14,3,3,1,r,self.attack))
        self.attack.extend(Attack.set(self.data,14,4,1,1,51))

        self.notes.extend(Notes.set(self.data,15,1,1,1,0))
        self.penalty.extend(Penalty.set(self.data,15,1,3,1,r,self.attack))
        self.attack.extend(Attack.set(self.data,15,2,1,1,102))
        self.notes.extend(Notes.set(self.data,15,3,1,1,51))
        self.penalty.extend(Penalty.set(self.data,15,3,3,1,r,self.attack))
        self.attack.extend(Attack.set(self.data,15,4,1,1,153))
        
        self.notes.extend(Notes.set(self.data,16,1,1,1,102))
        self.penalty.extend(Penalty.set(self.data,16,1,3,1,r,self.attack))
        self.notes.extend(Notes.set(self.data,16,2,1,1,51))
        self.notes.extend(Notes.set(self.data,16,3,1,1,153))
        self.penalty.extend(Penalty.set(self.data,16,3,3,1,r,self.attack))
        self.notes.extend(Notes.set(self.data,16,4,1,1,0))

        self.notes.extend(Notes.set(self.data,17,1,1,1,0))
        self.notes.extend(Notes.set(self.data,17,1,2,1,0))
        self.notes.extend(Notes.set(self.data,17,2,1,1,51))
        self.notes.extend(Notes.set(self.data,17,2,2,1,51))
        self.notes.extend(Notes.set(self.data,17,3,1,1,102))
        self.notes.extend(Notes.set(self.data,17,3,2,1,102))
        self.notes.extend(Notes.set(self.data,17,4,1,1,153))

        #A
        self.attack.extend(Attack.set(self.data,18,1,1,1,0))
        self.notes.extend(Notes.set(self.data,18,2,1,1,51))
        self.attack.extend(Attack.set(self.data,18,3,1,1,102))
        self.notes.extend(Notes.set(self.data,18,4,1,1,153))

        self.notes.extend(Notes.set(self.data,19,1,1,1,0))
        self.penalty.extend(Penalty.set(self.data,19,1,3,1,r,self.attack))
        self.attack.extend(Attack.set(self.data,19,2,1,1,153))
        self.notes.extend(Notes.set(self.data,19,3,1,1,102))
        self.penalty.extend(Penalty.set(self.data,19,3,3,1,r,self.attack))
        self.attack.extend(Attack.set(self.data,19,4,1,1,51))

        self.notes.extend(Notes.set(self.data,20,1,1,1,0))
        self.penalty.extend(Penalty.set(self.data,20,1,3,1,r,self.attack))
        self.attack.extend(Attack.set(self.data,20,2,1,1,102))
        self.notes.extend(Notes.set(self.data,20,3,1,1,51))
        self.penalty.extend(Penalty.set(self.data,20,3,3,1,r,self.attack))
        self.attack.extend(Attack.set(self.data,20,4,1,1,153))
        
        self.notes.extend(Notes.set(self.data,21,1,1,1,102))
        self.penalty.extend(Penalty.set(self.data,21,1,3,1,r,self.attack))
        self.attack.extend(Attack.set(self.data,21,2,1,1,51))
        self.notes.extend(Notes.set(self.data,21,3,1,1,153))
        self.penalty.extend(Penalty.set(self.data,21,3,3,1,r,self.attack))
        self.attack.extend(Attack.set(self.data,21,4,1,1,0))
        

        self.attack.extend(Attack.set(self.data,22,1,1,1,0))
        self.penalty.extend(Penalty.set(self.data,22,1,3,1,r,self.attack))
        self.notes.extend(Notes.set(self.data,22,2,1,1,51))
        self.attack.extend(Attack.set(self.data,22,3,1,1,102))
        self.penalty.extend(Penalty.set(self.data,22,3,3,1,r,self.attack))
        self.notes.extend(Notes.set(self.data,22,4,1,1,153))

        self.notes.extend(Notes.set(self.data,23,1,1,1,0))
        self.penalty.extend(Penalty.set(self.data,23,1,3,1,r,self.attack))
        self.attack.extend(Attack.set(self.data,23,2,1,1,153))
        self.notes.extend(Notes.set(self.data,23,3,1,1,102))
        self.penalty.extend(Penalty.set(self.data,23,3,3,1,r,self.attack))
        self.attack.extend(Attack.set(self.data,23,4,1,1,51))

        self.notes.extend(Notes.set(self.data,24,1,1,1,0))
        self.penalty.extend(Penalty.set(self.data,24,1,3,1,r,self.attack))
        self.attack.extend(Attack.set(self.data,24,2,1,1,102))
        self.notes.extend(Notes.set(self.data,24,3,1,1,51))
        self.penalty.extend(Penalty.set(self.data,24,3,3,1,r,self.attack))
        self.attack.extend(Attack.set(self.data,24,4,1,1,153))
        
        self.notes.extend(Notes.set(self.data,25,1,1,1,102))
        self.penalty.extend(Penalty.set(self.data,25,1,3,1,r,self.attack))
        self.attack.extend(Attack.set(self.data,25,2,1,1,51))
        self.notes.extend(Notes.set(self.data,25,3,1,1,153))
        self.penalty.extend(Penalty.set(self.data,25,3,3,1,r,self.attack))
        self.attack.extend(Attack.set(self.data,25,4,1,1,0))


        self.attack.extend(Attack.set(self.data,26,1,1,1,0))
        self.penalty.extend(Penalty.set(self.data,26,1,3,1,r,self.attack))
        self.notes.extend(Notes.set(self.data,26,2,1,1,51))
        self.attack.extend(Attack.set(self.data,26,3,1,1,102))
        self.penalty.extend(Penalty.set(self.data,26,3,3,1,r,self.attack))
        self.notes.extend(Notes.set(self.data,26,4,1,1,153))

        self.notes.extend(Notes.set(self.data,27,1,1,1,0))
        self.penalty.extend(Penalty.set(self.data,27,1,3,1,r,self.attack))
        self.attack.extend(Attack.set(self.data,27,2,1,1,153))
        self.notes.extend(Notes.set(self.data,27,3,1,1,102))
        self.penalty.extend(Penalty.set(self.data,27,3,3,1,r,self.attack))
        self.attack.extend(Attack.set(self.data,27,4,1,1,51))

        self.notes.extend(Notes.set(self.data,28,1,1,1,0))
        self.penalty.extend(Penalty.set(self.data,28,1,3,1,r,self.attack))
        self.attack.extend(Attack.set(self.data,28,2,1,1,102))
        self.notes.extend(Notes.set(self.data,28,3,1,1,51))
        self.penalty.extend(Penalty.set(self.data,28,3,3,1,r,self.attack))
        self.attack.extend(Attack.set(self.data,28,4,1,1,153))
        
        self.notes.extend(Notes.set(self.data,29,1,1,1,102))
        self.penalty.extend(Penalty.set(self.data,29,1,3,1,r,self.attack))
        self.attack.extend(Attack.set(self.data,29,2,1,1,51))
        self.notes.extend(Notes.set(self.data,29,3,1,1,153))
        self.penalty.extend(Penalty.set(self.data,29,3,3,1,r,self.attack))
        self.attack.extend(Attack.set(self.data,29,4,1,1,0))


        self.attack.extend(Attack.set(self.data,30,1,1,1,0))
        self.penalty.extend(Penalty.set(self.data,30,1,3,1,r,self.attack))
        self.notes.extend(Notes.set(self.data,30,2,1,1,51))
        self.attack.extend(Attack.set(self.data,30,3,1,1,102))
        self.penalty.extend(Penalty.set(self.data,30,3,3,1,r,self.attack))
        self.notes.extend(Notes.set(self.data,30,4,1,1,153))

        self.notes.extend(Notes.set(self.data,31,1,1,1,0))
        self.penalty.extend(Penalty.set(self.data,31,1,3,1,r,self.attack))
        self.attack.extend(Attack.set(self.data,31,2,1,1,153))
        self.notes.extend(Notes.set(self.data,31,3,1,1,102))
        self.penalty.extend(Penalty.set(self.data,31,3,3,1,r,self.attack))
        self.attack.extend(Attack.set(self.data,31,4,1,1,51))

        self.notes.extend(Notes.set(self.data,32,1,1,1,0))
        self.penalty.extend(Penalty.set(self.data,32,1,3,1,r,self.attack))
        self.attack.extend(Attack.set(self.data,32,2,1,1,102))
        self.notes.extend(Notes.set(self.data,32,3,1,1,51))
        self.penalty.extend(Penalty.set(self.data,32,3,3,1,r,self.attack))
        self.attack.extend(Attack.set(self.data,32,4,1,1,153))
        
        self.notes.extend(Notes.set(self.data,33,1,1,1,102))
        self.penalty.extend(Penalty.set(self.data,33,1,3,1,r,self.attack))
        self.notes.extend(Notes.set(self.data,33,2,1,1,51))
        self.notes.extend(Notes.set(self.data,33,3,1,1,153))
        self.penalty.extend(Penalty.set(self.data,33,3,3,1,r,self.attack))
        self.notes.extend(Notes.set(self.data,33,4,1,1,0))


        self.attack.extend(Attack.set(self.data,34,1,1,1,0))
        self.attack.extend(Attack.set(self.data,34,2,3,1,153))

        self.notes.extend(Notes.set(self.data,35,1,1,1,0))
        self.penalty.extend(Penalty.set(self.data,35,2,3,1,r,self.attack))
        self.notes.extend(Notes.set(self.data,35,3,1,1,102))
        self.penalty.extend(Penalty.set(self.data,35,3,3,1,r,self.attack))

        self.notes.extend(Notes.set(self.data,36,1,1,1,0))
        self.attack.extend(Attack.set(self.data,36,2,3,1,51))
        self.notes.extend(Notes.set(self.data,36,4,1,1,102))

        self.notes.extend(Notes.set(self.data,37,1,1,1,153))
        self.attack.extend(Attack.set(self.data,37,2,3,1,102))
        self.notes.extend(Notes.set(self.data,37,4,1,1,51))
        self.penalty.extend(Penalty.set(self.data,37,4,3,1,r,self.attack))

        self.notes.extend(Notes.set(self.data,38,1,1,1,0))
        self.penalty.extend(Penalty.set(self.data,38,1,4,1,r,self.attack))
        self.notes.extend(Notes.set(self.data,38,2,3,1,51))
        self.notes.extend(Notes.set(self.data,38,4,1,1,102))

        self.notes.extend(Notes.set(self.data,39,1,1,1,0))
        self.notes.extend(Notes.set(self.data,39,2,3,1,153))
        self.notes.extend(Notes.set(self.data,39,4,1,1,102))

        self.notes.extend(Notes.set(self.data,40,1,1,1,153))
        self.attack.extend(Attack.set(self.data,40,1,4,1,102))
        self.notes.extend(Notes.set(self.data,40,2,3,1,51))
        self.notes.extend(Notes.set(self.data,40,3,1,1,102))
        self.attack.extend(Attack.set(self.data,40,3,4,1,51))
        self.notes.extend(Notes.set(self.data,40,4,3,1,0))

        self.notes.extend(Notes.set(self.data,41,1,1,1,0))
        self.penalty.extend(Penalty.set(self.data,41,1,3,1,r,self.attack))
        self.notes.extend(Notes.set(self.data,41,2,1,1,51))
        self.penalty.extend(Penalty.set(self.data,41,2,3,1,r,self.attack))
        self.notes.extend(Notes.set(self.data,41,3,1,1,0))
        self.notes.extend(Notes.set(self.data,41,3,4,1,0))

        self.notes.extend(Notes.set(self.data,42,1,1,1,0))
        self.notes.extend(Notes.set(self.data,42,2,3,1,153))
        self.notes.extend(Notes.set(self.data,42,4,1,1,102))

        self.notes.extend(Notes.set(self.data,43,1,1,1,0))
        self.notes.extend(Notes.set(self.data,43,2,3,1,153))
        self.notes.extend(Notes.set(self.data,43,4,1,1,102))

        self.notes.extend(Notes.set(self.data,44,1,1,1,153))
        self.notes.extend(Notes.set(self.data,44,2,1,1,102))
        self.notes.extend(Notes.set(self.data,44,3,1,1,51))
        self.notes.extend(Notes.set(self.data,44,4,1,1,0))

        self.notes.extend(Notes.set(self.data,45,1,1,1,51))
        self.notes.extend(Notes.set(self.data,45,2,1,1,102))
        self.notes.extend(Notes.set(self.data,45,3,1,1,153))

        self.notes.extend(Notes.set(self.data,46,1,1,1,153))
        self.notes.extend(Notes.set(self.data,46,2,1,1,102))
        self.notes.extend(Notes.set(self.data,46,3,1,1,51))
        self.notes.extend(Notes.set(self.data,46,4,1,1,0))

        self.notes.extend(Notes.set(self.data,47,1,1,1,153))
        self.notes.extend(Notes.set(self.data,47,2,1,1,102))
        self.notes.extend(Notes.set(self.data,47,3,1,1,51))
        self.notes.extend(Notes.set(self.data,47,4,1,1,0))

        self.notes.extend(Notes.set(self.data,48,1,1,1,0))
        self.notes.extend(Notes.set(self.data,48,2,3,1,153))
        self.notes.extend(Notes.set(self.data,48,4,1,1,102))

        self.notes.extend(Notes.set(self.data,49,1,1,1,153))
        self.notes.extend(Notes.set(self.data,49,2,1,1,102))
        self.notes.extend(Notes.set(self.data,49,3,1,1,51))
        self.notes.extend(Notes.set(self.data,49,4,1,1,0))

        self.notes.extend(Notes.set(self.data,50,1,1,1,0))
        self.notes.extend(Notes.set(self.data,50,2,1,1,0))
        self.notes.extend(Notes.set(self.data,50,3,1,1,0))
        self.notes.extend(Notes.set(self.data,50,4,1,1,0))
        self.notes.extend(Notes.set(self.data,51,1,1,1,51))
        self.notes.extend(Notes.set(self.data,51,2,1,1,51))
        self.notes.extend(Notes.set(self.data,51,3,1,1,51))
        self.notes.extend(Notes.set(self.data,51,4,1,1,51))
        self.notes.extend(Notes.set(self.data,52,1,1,1,102))
        self.notes.extend(Notes.set(self.data,52,2,1,1,102))
        self.notes.extend(Notes.set(self.data,52,3,1,1,102))
        self.notes.extend(Notes.set(self.data,52,4,1,1,102))
        self.notes.extend(Notes.set(self.data,53,1,1,1,153))
        self.notes.extend(Notes.set(self.data,53,2,1,1,153))
        self.notes.extend(Notes.set(self.data,53,3,1,1,153))

        #B
        self.attack.extend(Attack.set(self.data,54,1,1,1,0))

        self.attack.extend(Attack.set(self.data,54,3,1,1,153))
        self.penalty.extend(Penalty.set(self.data,54,3,3,1,r,self.attack))
        self.notes.extend(Notes.set(self.data,54,4,1,1,51))

        self.attack.extend(Attack.set(self.data,55,1,1,1,0))
        self.penalty.extend(Penalty.set(self.data,55,1,3,1,r,self.attack))
        self.notes.extend(Notes.set(self.data,55,2,1,1,0))

        self.attack.extend(Attack.set(self.data,55,3,1,1,153))
        self.penalty.extend(Penalty.set(self.data,55,3,3,1,r,self.attack))
        self.notes.extend(Notes.set(self.data,55,4,1,1,51))

        self.attack.extend(Attack.set(self.data,56,1,1,1,0))
        self.penalty.extend(Penalty.set(self.data,56,2,1,1,r,self.attack))

        self.attack.extend(Attack.set(self.data,56,3,1,1,153))
        self.penalty.extend(Penalty.set(self.data,56,3,3,1,r,self.attack))
        self.notes.extend(Notes.set(self.data,56,4,1,1,51))

        self.attack.extend(Attack.set(self.data,57,1,1,1,0))
        self.penalty.extend(Penalty.set(self.data,57,1,3,1,r,self.attack))
        self.notes.extend(Notes.set(self.data,57,2,1,1,0))

        self.notes.extend(Notes.set(self.data,57,3,1,1,153))
        self.penalty.extend(Penalty.set(self.data,57,3,3,1,r,self.attack))
        self.notes.extend(Notes.set(self.data,57,4,1,1,51))

        self.attack.extend(Attack.set(self.data,58,1,1,1,0))

        self.attack.extend(Attack.set(self.data,58,3,1,1,153))
        self.penalty.extend(Penalty.set(self.data,58,3,3,1,r,self.attack))
        self.notes.extend(Notes.set(self.data,58,4,1,1,51))

        self.attack.extend(Attack.set(self.data,59,1,1,1,0))
        self.penalty.extend(Penalty.set(self.data,59,1,3,1,r,self.attack))
        self.notes.extend(Notes.set(self.data,59,2,1,1,0))

        self.attack.extend(Attack.set(self.data,59,3,1,1,153))
        self.penalty.extend(Penalty.set(self.data,59,3,3,1,r,self.attack))
        self.notes.extend(Notes.set(self.data,59,4,1,1,51))

        self.attack.extend(Attack.set(self.data,60,1,1,1,0))
        self.penalty.extend(Penalty.set(self.data,60,2,1,1,r,self.attack))

        self.attack.extend(Attack.set(self.data,60,3,1,1,153))
        self.penalty.extend(Penalty.set(self.data,60,3,3,1,r,self.attack))
        self.notes.extend(Notes.set(self.data,60,4,1,1,51))

        self.attack.extend(Attack.set(self.data,61,1,1,1,0))
        self.penalty.extend(Penalty.set(self.data,61,1,3,1,r,self.attack))
        self.notes.extend(Notes.set(self.data,61,2,1,1,0))

        self.notes.extend(Notes.set(self.data,61,3,1,1,153))
        self.penalty.extend(Penalty.set(self.data,61,3,3,1,r,self.attack))
        self.notes.extend(Notes.set(self.data,61,4,1,1,51))

        self.notes.extend(Notes.set(self.data,62,1,1,1,0))
        self.notes.extend(Notes.set(self.data,62,2,1,1,0))
        self.notes.extend(Notes.set(self.data,62,3,1,1,0))
        self.notes.extend(Notes.set(self.data,62,3,4,1,51))
        self.notes.extend(Notes.set(self.data,62,4,3,1,102))

        self.notes.extend(Notes.set(self.data,63,1,1,1,153))
        self.notes.extend(Notes.set(self.data,63,2,1,1,153))
        self.notes.extend(Notes.set(self.data,63,3,1,1,153))
        self.notes.extend(Notes.set(self.data,63,3,4,1,102))
        self.notes.extend(Notes.set(self.data,63,4,3,1,51))

        self.notes.extend(Notes.set(self.data,64,1,1,1,0))
        self.notes.extend(Notes.set(self.data,64,2,1,1,0))
        self.notes.extend(Notes.set(self.data,64,3,1,1,0))
        self.notes.extend(Notes.set(self.data,64,3,4,1,51))
        self.notes.extend(Notes.set(self.data,64,4,3,1,102))

        self.notes.extend(Notes.set(self.data,65,1,1,1,153))
        self.notes.extend(Notes.set(self.data,65,2,1,1,153))
        self.notes.extend(Notes.set(self.data,65,3,1,1,153))
        self.notes.extend(Notes.set(self.data,65,3,4,1,102))
        self.notes.extend(Notes.set(self.data,65,4,3,1,51))

        self.notes.extend(Notes.set(self.data,66,1,1,1,0))
        self.notes.extend(Notes.set(self.data,66,2,1,1,0))
        self.notes.extend(Notes.set(self.data,66,3,1,1,51))
        self.notes.extend(Notes.set(self.data,66,4,1,1,51))

        self.notes.extend(Notes.set(self.data,67,1,1,1,102))
        self.notes.extend(Notes.set(self.data,67,2,1,1,102))
        self.notes.extend(Notes.set(self.data,67,3,1,1,153))
        self.notes.extend(Notes.set(self.data,67,4,1,1,153))

        self.notes.extend(Notes.set(self.data,68,1,1,1,153))
        self.notes.extend(Notes.set(self.data,68,1,3,1,153))
        self.notes.extend(Notes.set(self.data,68,2,1,1,102))
        self.notes.extend(Notes.set(self.data,68,2,3,1,102))
        self.notes.extend(Notes.set(self.data,68,3,1,1,51))
        self.notes.extend(Notes.set(self.data,68,3,3,1,51))
        self.notes.extend(Notes.set(self.data,68,4,1,1,0))
        self.notes.extend(Notes.set(self.data,68,4,3,1,0))

        self.notes.extend(Notes.set(self.data,69,1,1,1,153))
        self.notes.extend(Notes.set(self.data,69,1,3,1,153))
        self.notes.extend(Notes.set(self.data,69,2,1,1,102))
        self.notes.extend(Notes.set(self.data,69,2,3,1,102))
        self.notes.extend(Notes.set(self.data,69,3,1,1,51))
        self.notes.extend(Notes.set(self.data,69,3,3,1,51))
        self.notes.extend(Notes.set(self.data,69,4,1,1,0))
        self.notes.extend(Notes.set(self.data,69,4,3,1,0))

        self.notes.extend(Notes.set(self.data,70,1,1,1,153))

        #break
        self.notes.extend(Notes.set(self.data,72,1,1,1,0))

        self.notes.extend(Notes.set(self.data,73,1,1,1,51))

        self.attack.extend(Attack.set(self.data,74,1,1,1,102))

        self.notes.extend(Notes.set(self.data,75,1,1,1,153))
        self.penalty.extend(Penalty.set(self.data,75,3,1,1,r,self.attack))

        self.notes.extend(Notes.set(self.data,76,1,1,1,51))

        self.notes.extend(Notes.set(self.data,77,1,1,1,0))

        self.notes.extend(Notes.set(self.data,78,1,1,1,51))
        self.notes.extend(Notes.set(self.data,78,3,1,1,102))

        self.attack.extend(Attack.set(self.data,79,1,1,1,153))

        self.notes.extend(Notes.set(self.data,80,1,1,1,0))
        self.penalty.extend(Penalty.set(self.data,80,3,1,1,r,self.attack))
        self.notes.extend(Notes.set(self.data,80,4,1,1,51))

        self.attack.extend(Attack.set(self.data,81,1,1,1,0))
        self.notes.extend(Notes.set(self.data,81,2,1,1,51))
        self.notes.extend(Notes.set(self.data,81,3,1,1,102))
        self.notes.extend(Notes.set(self.data,81,4,1,1,153))

        self.notes.extend(Notes.set(self.data,82,1,1,1,0))
        self.penalty.extend(Penalty.set(self.data,82,3,1,1,r,self.attack))
        self.notes.extend(Notes.set(self.data,82,4,1,1,51))

        self.attack.extend(Attack.set(self.data,83,1,1,1,0))
        self.notes.extend(Notes.set(self.data,83,2,1,1,51))
        self.notes.extend(Notes.set(self.data,83,3,1,1,102))
        self.notes.extend(Notes.set(self.data,83,4,1,1,153))

        self.notes.extend(Notes.set(self.data,84,1,1,1,153))
        self.penalty.extend(Penalty.set(self.data,84,3,1,1,r,self.attack))
        self.notes.extend(Notes.set(self.data,84,4,1,1,102))

        self.attack.extend(Attack.set(self.data,85,1,1,1,153))
        self.notes.extend(Notes.set(self.data,85,2,1,1,102))
        self.notes.extend(Notes.set(self.data,85,3,1,1,51))
        self.notes.extend(Notes.set(self.data,85,4,1,1,0))

        self.notes.extend(Notes.set(self.data,86,1,1,1,153))
        self.penalty.extend(Penalty.set(self.data,86,3,1,1,r,self.attack))
        self.notes.extend(Notes.set(self.data,86,4,1,1,102))

        self.notes.extend(Notes.set(self.data,87,1,1,1,153))
        self.notes.extend(Notes.set(self.data,87,2,1,1,102))
        self.notes.extend(Notes.set(self.data,87,3,1,1,51))
        self.notes.extend(Notes.set(self.data,87,4,1,1,0))

        #buildup
        self.notes.extend(Notes.set(self.data,88,1,1,1,153))
        self.notes.extend(Notes.set(self.data,88,2,3,1,0))
        self.attack.extend(Attack.set(self.data,88,4,1,1,102))

        self.notes.extend(Notes.set(self.data,89,1,1,1,51))
        self.notes.extend(Notes.set(self.data,89,2,3,1,0))
        self.notes.extend(Notes.set(self.data,89,4,1,1,102))
        self.penalty.extend(Penalty.set(self.data,89,4,3,1,r,self.attack))

        self.notes.extend(Notes.set(self.data,90,1,1,1,0))
        self.notes.extend(Notes.set(self.data,90,2,3,1,153))
        self.notes.extend(Notes.set(self.data,90,4,1,1,102))

        self.notes.extend(Notes.set(self.data,91,1,1,1,51))
        self.notes.extend(Notes.set(self.data,91,2,3,1,0))
        self.notes.extend(Notes.set(self.data,91,4,1,1,102))

        self.notes.extend(Notes.set(self.data,92,1,1,1,153))
        self.notes.extend(Notes.set(self.data,92,1,3,1,0))
        self.notes.extend(Notes.set(self.data,92,2,1,1,102))
        self.notes.extend(Notes.set(self.data,92,2,3,1,51))
        self.notes.extend(Notes.set(self.data,92,3,1,1,153))
        self.notes.extend(Notes.set(self.data,92,3,3,1,0))
        self.notes.extend(Notes.set(self.data,92,4,1,1,102))
        self.notes.extend(Notes.set(self.data,92,4,3,1,51))

        self.notes.extend(Notes.set(self.data,93,1,1,1,153))
        self.notes.extend(Notes.set(self.data,93,1,3,1,51))
        self.notes.extend(Notes.set(self.data,93,2,1,1,102))
        self.notes.extend(Notes.set(self.data,93,2,3,1,0))
        self.notes.extend(Notes.set(self.data,93,3,1,1,153))
        self.notes.extend(Notes.set(self.data,93,3,3,1,51))
        self.notes.extend(Notes.set(self.data,93,4,1,1,102))
        self.notes.extend(Notes.set(self.data,93,4,3,1,0))

        self.notes.extend(Notes.set(self.data,94,1,1,1,153))
        self.notes.extend(Notes.set(self.data,94,1,3,1,153))
        self.notes.extend(Notes.set(self.data,94,2,1,1,102))
        self.notes.extend(Notes.set(self.data,94,2,3,1,102))
        self.notes.extend(Notes.set(self.data,94,2,3,1,51))
        self.notes.extend(Notes.set(self.data,94,3,3,1,51))
        self.notes.extend(Notes.set(self.data,94,4,1,1,0))
        self.notes.extend(Notes.set(self.data,94,4,3,1,0))

        self.notes.extend(Notes.set(self.data,95,1,1,1,0))
        self.notes.extend(Notes.set(self.data,95,1,1,1,153))
        self.notes.extend(Notes.set(self.data,95,1,3,1,0))
        self.notes.extend(Notes.set(self.data,95,1,3,1,153))
        self.notes.extend(Notes.set(self.data,95,2,1,1,0))
        self.notes.extend(Notes.set(self.data,95,2,1,1,153))
        self.notes.extend(Notes.set(self.data,95,2,3,1,0))
        self.notes.extend(Notes.set(self.data,95,2,3,1,153))
        self.notes.extend(Notes.set(self.data,95,3,1,1,0))
        self.notes.extend(Notes.set(self.data,95,3,1,1,153))
        self.notes.extend(Notes.set(self.data,95,3,3,1,0))
        self.notes.extend(Notes.set(self.data,95,3,3,1,153))

        self.notes.extend(Notes.set(self.data,96,1,1,1,0))
        self.notes.extend(Notes.set(self.data,96,1,1,1,153))
        self.notes.extend(Notes.set(self.data,96,1,3,1,0))
        self.notes.extend(Notes.set(self.data,96,1,3,1,153))
        self.notes.extend(Notes.set(self.data,96,2,1,1,0))
        self.notes.extend(Notes.set(self.data,96,2,1,1,153))
        self.notes.extend(Notes.set(self.data,96,2,3,1,0))
        self.notes.extend(Notes.set(self.data,96,2,3,1,153))
        self.notes.extend(Notes.set(self.data,96,3,1,1,0))
        self.notes.extend(Notes.set(self.data,96,3,1,1,153))
        self.notes.extend(Notes.set(self.data,96,3,3,1,0))
        self.notes.extend(Notes.set(self.data,96,3,3,1,153))

        self.notes.extend(Notes.set(self.data,97,1,1,1,0))
        self.notes.extend(Notes.set(self.data,97,1,1,1,153))
        self.notes.extend(Notes.set(self.data,97,1,3,1,0))
        self.notes.extend(Notes.set(self.data,97,1,3,1,153))
        self.notes.extend(Notes.set(self.data,97,2,1,1,0))
        self.notes.extend(Notes.set(self.data,97,2,1,1,153))
        self.notes.extend(Notes.set(self.data,97,2,3,1,0))
        self.notes.extend(Notes.set(self.data,97,2,3,1,153))
        self.notes.extend(Notes.set(self.data,97,3,1,1,51))
        self.notes.extend(Notes.set(self.data,97,3,1,1,102))
        self.notes.extend(Notes.set(self.data,97,3,3,1,51))
        self.notes.extend(Notes.set(self.data,97,3,3,1,102))
        self.notes.extend(Notes.set(self.data,97,4,1,1,51))
        self.notes.extend(Notes.set(self.data,97,4,1,1,102))
        self.notes.extend(Notes.set(self.data,97,4,3,1,51))
        self.notes.extend(Notes.set(self.data,97,4,3,1,102))

        self.notes.extend(Notes.set(self.data,98,3,1,1,0))
        self.notes.extend(Notes.set(self.data,98,3,2,1,153))
        self.notes.extend(Notes.set(self.data,98,3,3,1,0))
        self.notes.extend(Notes.set(self.data,98,3,4,1,153))
        self.notes.extend(Notes.set(self.data,98,4,1,1,0))
        self.notes.extend(Notes.set(self.data,98,4,2,1,153))
        self.notes.extend(Notes.set(self.data,98,4,3,1,0))
        self.notes.extend(Notes.set(self.data,98,4,4,1,153))

        #drop
        self.notes.extend(Notes.set(self.data,99,1,1,1,0))
        self.notes.extend(Notes.set(self.data,99,1,3,1,0))
        self.notes.extend(Notes.set(self.data,99,2,1,1,0))
        self.notes.extend(Notes.set(self.data,99,2,3,1,51))
        self.notes.extend(Notes.set(self.data,99,2,4,1,102))
        self.notes.extend(Notes.set(self.data,99,3,1,1,153))
        self.notes.extend(Notes.set(self.data,99,3,3,1,153))
        self.notes.extend(Notes.set(self.data,99,4,1,1,153))
        self.notes.extend(Notes.set(self.data,99,4,3,1,102))
        self.notes.extend(Notes.set(self.data,99,4,4,1,51))

        self.notes.extend(Notes.set(self.data,100,1,1,1,0))
        self.attack.extend(Attack.set(self.data,100,1,3,1,51))
        self.notes.extend(Notes.set(self.data,100,2,1,1,102))
        self.notes.extend(Notes.set(self.data,100,2,3,1,153))
        self.notes.extend(Notes.set(self.data,100,3,1,1,153))
        self.notes.extend(Notes.set(self.data,100,3,3,1,102))
        self.notes.extend(Notes.set(self.data,100,4,1,1,51))
        self.notes.extend(Notes.set(self.data,100,4,3,1,0))

        self.notes.extend(Notes.set(self.data,101,1,1,1,0))
        self.penalty.extend(Penalty.set(self.data,101,1,2,1,r,self.attack))
        self.notes.extend(Notes.set(self.data,101,1,3,1,0))
        self.notes.extend(Notes.set(self.data,101,2,1,1,0))
        self.notes.extend(Notes.set(self.data,101,2,3,1,51))
        self.notes.extend(Notes.set(self.data,101,2,4,1,102))
        self.notes.extend(Notes.set(self.data,101,3,1,1,153))
        self.notes.extend(Notes.set(self.data,101,3,3,1,153))
        self.notes.extend(Notes.set(self.data,101,4,1,1,153))
        self.notes.extend(Notes.set(self.data,101,4,3,1,102))
        self.notes.extend(Notes.set(self.data,101,4,4,1,51))

        self.notes.extend(Notes.set(self.data,102,1,1,1,0))
        self.attack.extend(Attack.set(self.data,102,1,3,1,51))
        self.notes.extend(Notes.set(self.data,102,2,1,1,102))
        self.notes.extend(Notes.set(self.data,102,2,3,1,153))
        self.notes.extend(Notes.set(self.data,102,3,1,1,153))
        self.notes.extend(Notes.set(self.data,102,3,3,1,102))
        self.notes.extend(Notes.set(self.data,102,4,1,1,51))
        self.notes.extend(Notes.set(self.data,102,4,3,1,0))

        self.notes.extend(Notes.set(self.data,103,1,1,1,0))
        self.notes.extend(Notes.set(self.data,103,1,3,1,0))
        self.notes.extend(Notes.set(self.data,103,2,1,1,0))
        self.notes.extend(Notes.set(self.data,103,2,3,1,51))
        self.notes.extend(Notes.set(self.data,103,2,4,1,102))
        self.notes.extend(Notes.set(self.data,103,3,1,1,153))
        self.notes.extend(Notes.set(self.data,103,3,3,1,153))
        self.notes.extend(Notes.set(self.data,103,4,1,1,153))
        self.notes.extend(Notes.set(self.data,103,4,3,1,102))
        self.notes.extend(Notes.set(self.data,103,4,4,1,51))

        self.notes.extend(Notes.set(self.data,104,1,1,1,0))
        self.attack.extend(Attack.set(self.data,104,1,3,1,51))
        self.notes.extend(Notes.set(self.data,104,2,1,1,102))
        self.notes.extend(Notes.set(self.data,104,2,3,1,153))
        self.notes.extend(Notes.set(self.data,104,3,1,1,153))
        self.notes.extend(Notes.set(self.data,104,3,3,1,102))
        self.notes.extend(Notes.set(self.data,104,4,1,1,51))
        self.notes.extend(Notes.set(self.data,104,4,3,1,0))

        self.notes.extend(Notes.set(self.data,105,1,1,1,0))
        self.penalty.extend(Penalty.set(self.data,105,1,2,1,r,self.attack))
        self.notes.extend(Notes.set(self.data,105,1,3,1,0))
        self.notes.extend(Notes.set(self.data,105,2,1,1,0))
        self.notes.extend(Notes.set(self.data,105,2,3,1,51))
        self.notes.extend(Notes.set(self.data,105,2,4,1,102))
        self.notes.extend(Notes.set(self.data,105,3,1,1,153))
        self.notes.extend(Notes.set(self.data,105,3,3,1,153))
        self.notes.extend(Notes.set(self.data,105,4,1,1,153))
        self.notes.extend(Notes.set(self.data,105,4,3,1,102))
        self.notes.extend(Notes.set(self.data,105,4,4,1,51))

        self.notes.extend(Notes.set(self.data,106,1,1,1,0))
        self.attack.extend(Attack.set(self.data,106,1,3,1,51))
        self.notes.extend(Notes.set(self.data,106,2,1,1,102))
        self.notes.extend(Notes.set(self.data,106,2,3,1,153))
        self.notes.extend(Notes.set(self.data,106,3,1,1,153))
        self.notes.extend(Notes.set(self.data,106,3,3,1,102))
        self.notes.extend(Notes.set(self.data,106,4,1,1,51))
        self.notes.extend(Notes.set(self.data,106,4,3,1,0))

        self.notes.extend(Notes.set(self.data,107,1,1,1,0))
        self.notes.extend(Notes.set(self.data,107,1,3,1,0))
        self.notes.extend(Notes.set(self.data,107,2,1,1,0))
        self.notes.extend(Notes.set(self.data,107,2,3,1,51))
        self.notes.extend(Notes.set(self.data,107,2,4,1,102))
        self.notes.extend(Notes.set(self.data,107,3,1,1,153))
        self.notes.extend(Notes.set(self.data,107,3,3,1,153))
        self.notes.extend(Notes.set(self.data,107,4,1,1,153))
        self.notes.extend(Notes.set(self.data,107,4,3,1,102))
        self.notes.extend(Notes.set(self.data,107,4,4,1,51))

        self.notes.extend(Notes.set(self.data,108,1,1,1,0))
        self.attack.extend(Attack.set(self.data,108,1,3,1,51))
        self.notes.extend(Notes.set(self.data,108,2,1,1,102))
        self.notes.extend(Notes.set(self.data,108,2,3,1,153))
        self.notes.extend(Notes.set(self.data,108,3,1,1,153))
        self.notes.extend(Notes.set(self.data,108,3,3,1,102))
        self.notes.extend(Notes.set(self.data,108,4,1,1,51))
        self.notes.extend(Notes.set(self.data,108,4,3,1,0))

        self.notes.extend(Notes.set(self.data,109,1,1,1,0))
        self.penalty.extend(Penalty.set(self.data,109,1,2,1,r,self.attack))
        self.notes.extend(Notes.set(self.data,109,1,3,1,0))
        self.notes.extend(Notes.set(self.data,109,2,1,1,0))
        self.notes.extend(Notes.set(self.data,109,2,3,1,51))
        self.notes.extend(Notes.set(self.data,109,2,4,1,102))
        self.notes.extend(Notes.set(self.data,109,3,1,1,153))
        self.notes.extend(Notes.set(self.data,109,3,3,1,153))
        self.notes.extend(Notes.set(self.data,109,4,1,1,153))
        self.notes.extend(Notes.set(self.data,109,4,3,1,102))
        self.notes.extend(Notes.set(self.data,109,4,4,1,51))

        self.notes.extend(Notes.set(self.data,110,1,1,1,0))
        self.attack.extend(Attack.set(self.data,110,1,3,1,51))
        self.notes.extend(Notes.set(self.data,110,2,1,1,102))
        self.notes.extend(Notes.set(self.data,110,2,3,1,153))
        self.notes.extend(Notes.set(self.data,110,3,1,1,153))
        self.notes.extend(Notes.set(self.data,110,3,3,1,102))
        self.notes.extend(Notes.set(self.data,110,4,1,1,51))
        self.notes.extend(Notes.set(self.data,110,4,3,1,0))

        self.notes.extend(Notes.set(self.data,111,1,1,1,0))
        self.notes.extend(Notes.set(self.data,111,1,3,1,0))
        self.notes.extend(Notes.set(self.data,111,2,1,1,0))
        self.notes.extend(Notes.set(self.data,111,2,3,1,51))
        self.notes.extend(Notes.set(self.data,111,2,4,1,102))
        self.notes.extend(Notes.set(self.data,111,3,1,1,153))
        self.notes.extend(Notes.set(self.data,111,3,3,1,153))
        self.notes.extend(Notes.set(self.data,111,4,1,1,153))
        self.notes.extend(Notes.set(self.data,111,4,3,1,102))
        self.notes.extend(Notes.set(self.data,111,4,4,1,51))

        self.notes.extend(Notes.set(self.data,112,1,1,1,0))
        self.attack.extend(Attack.set(self.data,112,1,3,1,51))
        self.notes.extend(Notes.set(self.data,112,2,1,1,102))
        self.notes.extend(Notes.set(self.data,112,2,3,1,153))
        self.notes.extend(Notes.set(self.data,112,3,1,1,153))
        self.notes.extend(Notes.set(self.data,112,3,3,1,102))
        self.notes.extend(Notes.set(self.data,112,4,1,1,51))
        self.notes.extend(Notes.set(self.data,112,4,3,1,0))

        self.notes.extend(Notes.set(self.data,113,1,1,1,0))
        self.penalty.extend(Penalty.set(self.data,113,1,2,1,r,self.attack))
        self.notes.extend(Notes.set(self.data,113,1,3,1,0))
        self.notes.extend(Notes.set(self.data,113,2,1,1,0))
        self.notes.extend(Notes.set(self.data,113,2,3,1,51))
        self.notes.extend(Notes.set(self.data,113,2,4,1,102))
        self.notes.extend(Notes.set(self.data,113,3,1,1,153))
        self.notes.extend(Notes.set(self.data,113,3,3,1,153))
        self.notes.extend(Notes.set(self.data,113,4,1,1,153))
        self.notes.extend(Notes.set(self.data,113,4,3,1,102))
        self.notes.extend(Notes.set(self.data,113,4,4,1,51))

        self.notes.extend(Notes.set(self.data,114,1,1,1,0))
        self.attack.extend(Attack.set(self.data,114,1,3,1,51))
        self.notes.extend(Notes.set(self.data,114,2,1,1,102))
        self.notes.extend(Notes.set(self.data,114,2,3,1,153))
        self.notes.extend(Notes.set(self.data,114,3,1,1,153))
        self.notes.extend(Notes.set(self.data,114,3,3,1,102))
        self.notes.extend(Notes.set(self.data,114,4,1,1,51))
        self.notes.extend(Notes.set(self.data,114,4,3,1,0))


        self.notes.extend(Notes.set(self.data,115,1,1,1,0))
        self.notes.extend(Notes.set(self.data,115,1,3,1,0))
        self.notes.extend(Notes.set(self.data,115,2,1,1,0))
        self.notes.extend(Notes.set(self.data,115,2,3,1,51))
        self.notes.extend(Notes.set(self.data,115,2,4,1,102))
        self.notes.extend(Notes.set(self.data,115,3,1,1,153))
        self.notes.extend(Notes.set(self.data,115,3,2,1,0))
        self.notes.extend(Notes.set(self.data,115,3,3,1,153))
        self.notes.extend(Notes.set(self.data,115,3,4,1,0))
        self.notes.extend(Notes.set(self.data,115,4,1,1,153))
        self.notes.extend(Notes.set(self.data,115,4,2,1,0))
        self.notes.extend(Notes.set(self.data,115,4,3,1,153))
        self.notes.extend(Notes.set(self.data,115,4,4,1,0))

        self.notes.extend(Notes.set(self.data,116,1,1,1,153))
        self.notes.extend(Notes.set(self.data,116,1,3,1,153))
        self.notes.extend(Notes.set(self.data,116,2,1,1,153))
        self.notes.extend(Notes.set(self.data,116,2,3,1,102))
        self.notes.extend(Notes.set(self.data,116,2,4,1,51))
        self.notes.extend(Notes.set(self.data,116,3,1,1,0))
        self.notes.extend(Notes.set(self.data,116,3,2,1,153))
        self.notes.extend(Notes.set(self.data,116,3,3,1,0))
        self.notes.extend(Notes.set(self.data,116,3,4,1,153))
        self.notes.extend(Notes.set(self.data,116,4,1,1,0))
        self.notes.extend(Notes.set(self.data,116,4,2,1,153))
        self.notes.extend(Notes.set(self.data,116,4,3,1,0))
        self.notes.extend(Notes.set(self.data,116,4,4,1,153))

        self.notes.extend(Notes.set(self.data,117,1,1,1,0))
        self.notes.extend(Notes.set(self.data,117,1,3,1,0))
        self.notes.extend(Notes.set(self.data,117,2,1,1,0))
        self.notes.extend(Notes.set(self.data,117,2,3,1,51))
        self.notes.extend(Notes.set(self.data,117,2,4,1,102))
        self.notes.extend(Notes.set(self.data,117,3,1,1,153))
        self.notes.extend(Notes.set(self.data,117,3,2,1,0))
        self.notes.extend(Notes.set(self.data,117,3,3,1,153))
        self.notes.extend(Notes.set(self.data,117,3,4,1,0))
        self.notes.extend(Notes.set(self.data,117,4,1,1,153))
        self.notes.extend(Notes.set(self.data,117,4,2,1,0))
        self.notes.extend(Notes.set(self.data,117,4,3,1,153))
        self.notes.extend(Notes.set(self.data,117,4,4,1,0))

        self.notes.extend(Notes.set(self.data,118,1,1,1,153))
        self.notes.extend(Notes.set(self.data,118,1,3,1,153))
        self.notes.extend(Notes.set(self.data,118,2,1,1,153))
        self.notes.extend(Notes.set(self.data,118,2,3,1,102))
        self.notes.extend(Notes.set(self.data,118,2,4,1,51))
        self.attack.extend(Attack.set(self.data,118,3,1,1,0))
        self.notes.extend(Notes.set(self.data,118,3,2,1,153))
        self.notes.extend(Notes.set(self.data,118,3,3,1,0))
        self.notes.extend(Notes.set(self.data,118,3,4,1,153))
        self.notes.extend(Notes.set(self.data,118,4,1,1,0))
        self.notes.extend(Notes.set(self.data,118,4,2,1,153))
        self.notes.extend(Notes.set(self.data,118,4,3,1,0))
        self.notes.extend(Notes.set(self.data,118,4,4,1,153))

        self.notes.extend(Notes.set(self.data,119,1,1,1,0))
        self.notes.extend(Notes.set(self.data,119,1,3,1,0))
        self.notes.extend(Notes.set(self.data,119,2,1,1,0))
        self.notes.extend(Notes.set(self.data,119,2,3,1,0))
        self.notes.extend(Notes.set(self.data,119,3,1,1,0))
        self.notes.extend(Notes.set(self.data,119,3,3,1,0))
        self.attack.extend(Attack.set(self.data,119,4,1,1,0))
        self.penalty.extend(Penalty.set(self.data,119,4,3,1,r,self.attack))

        self.notes.extend(Notes.set(self.data,120,1,1,1,153))
        self.notes.extend(Notes.set(self.data,120,1,3,1,153))
        self.notes.extend(Notes.set(self.data,120,2,1,1,153))
        self.notes.extend(Notes.set(self.data,120,2,3,1,153))
        self.notes.extend(Notes.set(self.data,120,3,1,1,153))
        self.notes.extend(Notes.set(self.data,120,3,3,1,153))
        self.notes.extend(Notes.set(self.data,120,4,1,1,153))
        self.penalty.extend(Penalty.set(self.data,120,4,3,1,r,self.attack))

        self.notes.extend(Notes.set(self.data,121,1,1,1,0))
        self.notes.extend(Notes.set(self.data,121,1,1,1,153))
        self.notes.extend(Notes.set(self.data,121,1,3,1,0))
        self.notes.extend(Notes.set(self.data,121,1,3,1,153))
        self.notes.extend(Notes.set(self.data,121,2,1,1,0))
        self.notes.extend(Notes.set(self.data,121,2,1,1,153))
        self.notes.extend(Notes.set(self.data,121,2,3,1,0))
        self.notes.extend(Notes.set(self.data,121,2,3,1,153))
        self.notes.extend(Notes.set(self.data,121,3,1,1,0))
        self.notes.extend(Notes.set(self.data,121,3,1,1,153))
        self.notes.extend(Notes.set(self.data,121,3,3,1,0))
        self.notes.extend(Notes.set(self.data,121,3,3,1,153))
        self.notes.extend(Notes.set(self.data,121,4,1,1,0))
        self.notes.extend(Notes.set(self.data,121,4,1,1,153))
        self.notes.extend(Notes.set(self.data,121,4,3,1,0))
        self.notes.extend(Notes.set(self.data,121,4,3,1,153))

        self.notes.extend(Notes.set(self.data,122,1,1,1,51))
        self.notes.extend(Notes.set(self.data,122,1,2,1,102))
        self.notes.extend(Notes.set(self.data,122,1,3,1,51))
        self.notes.extend(Notes.set(self.data,122,1,4,1,102))
        self.notes.extend(Notes.set(self.data,122,2,1,1,51))
        self.notes.extend(Notes.set(self.data,122,2,2,1,102))
        self.notes.extend(Notes.set(self.data,122,2,3,1,51))
        self.notes.extend(Notes.set(self.data,122,2,4,1,102))
        self.notes.extend(Notes.set(self.data,122,3,1,1,51))
        self.notes.extend(Notes.set(self.data,122,3,2,1,102))
        self.notes.extend(Notes.set(self.data,122,3,3,1,51))
        self.notes.extend(Notes.set(self.data,122,3,4,1,102))
        self.notes.extend(Notes.set(self.data,122,4,1,1,51))
        self.notes.extend(Notes.set(self.data,122,4,2,1,102))
        self.notes.extend(Notes.set(self.data,122,4,3,1,51))
        self.notes.extend(Notes.set(self.data,122,4,4,1,102))

        self.notes.extend(Notes.set(self.data,123,1,1,1,0))
        self.notes.extend(Notes.set(self.data,123,1,3,1,153))
        self.notes.extend(Notes.set(self.data,123,2,1,1,153))
        self.notes.extend(Notes.set(self.data,123,2,3,1,153))
        self.notes.extend(Notes.set(self.data,123,3,1,1,153))
        self.notes.extend(Notes.set(self.data,123,3,3,1,153))
        self.notes.extend(Notes.set(self.data,123,4,1,1,153))
        self.notes.extend(Notes.set(self.data,123,4,3,1,153))

        self.notes.extend(Notes.set(self.data,124,1,1,1,153))
        self.notes.extend(Notes.set(self.data,124,1,3,1,153))
        self.notes.extend(Notes.set(self.data,124,2,1,1,153))
        self.notes.extend(Notes.set(self.data,124,2,3,1,153))
        self.notes.extend(Notes.set(self.data,124,3,1,1,51))
        self.notes.extend(Notes.set(self.data,124,3,1,1,102))
        self.notes.extend(Notes.set(self.data,124,3,3,1,51))
        self.notes.extend(Notes.set(self.data,124,3,3,1,102))
        self.notes.extend(Notes.set(self.data,124,4,1,1,51))
        self.notes.extend(Notes.set(self.data,124,4,1,1,102))
        self.notes.extend(Notes.set(self.data,124,4,3,1,51))
        self.notes.extend(Notes.set(self.data,124,4,3,1,102))

        self.notes.extend(Notes.set(self.data,125,1,1,1,153))
        self.notes.extend(Notes.set(self.data,125,1,3,1,0))
        self.notes.extend(Notes.set(self.data,125,2,1,1,0))
        self.notes.extend(Notes.set(self.data,125,2,3,1,0))
        self.notes.extend(Notes.set(self.data,125,3,1,1,0))
        self.notes.extend(Notes.set(self.data,125,3,3,1,0))
        self.notes.extend(Notes.set(self.data,125,4,1,1,0))
        self.notes.extend(Notes.set(self.data,125,4,3,1,0))

        self.notes.extend(Notes.set(self.data,126,1,1,1,0))
        self.notes.extend(Notes.set(self.data,126,1,3,1,0))
        self.notes.extend(Notes.set(self.data,126,2,1,1,0))
        self.notes.extend(Notes.set(self.data,126,2,3,1,0))
        self.notes.extend(Notes.set(self.data,126,3,1,1,51))
        self.notes.extend(Notes.set(self.data,126,3,1,1,102))
        self.notes.extend(Notes.set(self.data,126,3,3,1,51))
        self.notes.extend(Notes.set(self.data,126,3,3,1,102))
        self.notes.extend(Notes.set(self.data,126,4,1,1,51))
        self.notes.extend(Notes.set(self.data,126,4,1,1,102))
        self.notes.extend(Notes.set(self.data,126,4,3,1,51))
        self.notes.extend(Notes.set(self.data,126,4,3,1,102))

        self.notes.extend(Notes.set(self.data,127,1,1,1,0))
        self.notes.extend(Notes.set(self.data,127,1,1,1,153))

        for notes in self.notes:
            notes.move()
            notes.judge(self.data,self.feedback_list)

        for atk in self.attack:
            atk.move()
            atk.judge(self.data,self.feedback_list)

        for pen in self.penalty:
            pen.move()
            pen.judge(self.data,self.feedback_list)

        for b in self.bar:
            b.move()

        self.feedback_list = [fb for fb in self.feedback_list if time.time() - fb.start_time <= 0.5]

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(406 // 2 - 2 // 2, 0, 2, 320, 8)
        for i in range(1, 8):
            pyxel.rect(50 * i + (i-1), 0, 1, 320, 6)
        pyxel.rect(0,300,406,5,8)

        self.data.draw()

        for b in self.bar:
            b.draw()

        for notes in self.notes:
            notes.draw()
        
        for atk in self.attack:
            atk.draw()

        for pen in self.penalty:
            pen.draw()

        for fb in self.feedback_list:
            fb.draw()


App()

