# chip8_opcode_fix.py with Welcome Screen (no pause feature)
import pygame
import sys
import random

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 64, 32
SCALE = 10
FPS = 60

KEYMAP = {
    pygame.K_x: 0x0, pygame.K_1: 0x1, pygame.K_2: 0x2, pygame.K_3: 0x3,
    pygame.K_q: 0x4, pygame.K_w: 0x5, pygame.K_e: 0x6, pygame.K_a: 0x7,
    pygame.K_s: 0x8, pygame.K_d: 0x9, pygame.K_z: 0xA, pygame.K_c: 0xB,
    pygame.K_4: 0xC, pygame.K_r: 0xD, pygame.K_f: 0xE, pygame.K_v: 0xF,
}

def update_keys(chip8):
    keys = [0] * 16
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pressed = pygame.key.get_pressed()
    for key, val in KEYMAP.items():
        if pressed[key]:
            keys[val] = 1
    chip8.set_keys(keys)

class Chip8:
    def __init__(self):
        self.memory = [0] * 4096
        self.V = [0] * 16
        self.I = 0
        self.pc = 0x200
        self.stack = []
        self.display = [[0] * SCREEN_WIDTH for _ in range(SCREEN_HEIGHT)]
        self.keys = [0] * 16
        self.delay_timer = 0
        self.sound_timer = 0

    def load_rom(self, path):
        with open(path, 'rb') as f:
            rom = f.read()
            for i in range(len(rom)):
                self.memory[0x200 + i] = rom[i]

    def emulate_cycle(self):
        if self.pc >= len(self.memory) - 1:
            print("PC out of bounds.")
            return

        opcode = (self.memory[self.pc] << 8) | self.memory[self.pc + 1]
        self.pc += 2
        self.decode_execute(opcode)

        if self.delay_timer > 0:
            self.delay_timer -= 1
        if self.sound_timer > 0:
            self.sound_timer -= 1

    def decode_execute(self, opcode):
        first_nibble = opcode & 0xF000

        if opcode == 0x00E0:
            self.display = [[0] * SCREEN_WIDTH for _ in range(SCREEN_HEIGHT)]
        elif opcode == 0x00EE:
            self.pc = self.stack.pop()
        elif first_nibble == 0x1000:
            self.pc = opcode & 0x0FFF
        elif first_nibble == 0x2000:
            self.stack.append(self.pc)
            self.pc = opcode & 0x0FFF
        elif first_nibble == 0x3000:
            x = (opcode & 0x0F00) >> 8
            if self.V[x] == (opcode & 0x00FF):
                self.pc += 2
        elif first_nibble == 0x4000:
            x = (opcode & 0x0F00) >> 8
            if self.V[x] != (opcode & 0x00FF):
                self.pc += 2
        elif first_nibble == 0x5000 and (opcode & 0x000F) == 0:
            x = (opcode & 0x0F00) >> 8
            y = (opcode & 0x00F0) >> 4
            if self.V[x] == self.V[y]:
                self.pc += 2
        elif first_nibble == 0x6000:
            x = (opcode & 0x0F00) >> 8
            self.V[x] = opcode & 0x00FF
        elif first_nibble == 0x7000:
            x = (opcode & 0x0F00) >> 8
            self.V[x] = (self.V[x] + (opcode & 0x00FF)) & 0xFF
        elif first_nibble == 0x9000 and (opcode & 0x000F) == 0:
            x = (opcode & 0x0F00) >> 8
            y = (opcode & 0x00F0) >> 4
            if self.V[x] != self.V[y]:
                self.pc += 2
        elif first_nibble == 0xA000:
            self.I = opcode & 0x0FFF
        elif first_nibble == 0xC000:
            x = (opcode & 0x0F00) >> 8
            self.V[x] = random.randint(0, 255) & (opcode & 0x00FF)
        elif first_nibble == 0xD000:
            x = self.V[(opcode & 0x0F00) >> 8]
            y = self.V[(opcode & 0x00F0) >> 4]
            height = opcode & 0x000F
            self.V[0xF] = 0
            for row in range(height):
                sprite = self.memory[self.I + row]
                for col in range(8):
                    if sprite & (0x80 >> col):
                        px = (x + col) % SCREEN_WIDTH
                        py = (y + row) % SCREEN_HEIGHT
                        if self.display[py][px] == 1:
                            self.V[0xF] = 1
                        self.display[py][px] ^= 1
        elif first_nibble == 0xE000:
            x = (opcode & 0x0F00) >> 8
            if (opcode & 0x00FF) == 0x9E:
                if self.keys[self.V[x]]:
                    self.pc += 2
            elif (opcode & 0x00FF) == 0xA1:
                if not self.keys[self.V[x]]:
                    self.pc += 2
        elif first_nibble == 0xF000:
            x = (opcode & 0x0F00) >> 8
            nn = opcode & 0x00FF
            if nn == 0x07:
                self.V[x] = self.delay_timer
            elif nn == 0x15:
                self.delay_timer = self.V[x]
            elif nn == 0x18:
                self.sound_timer = self.V[x]
            elif nn == 0x1E:
                self.I = (self.I + self.V[x]) & 0xFFF
            else:
                print(f"Unknown FX opcode: {hex(opcode)}")
        else:
            print(f"Unknown opcode: {hex(opcode)}")

    def get_display(self):
        return self.display

    def set_keys(self, keys):
        self.keys = keys

def draw(screen, display):
    screen.fill((0, 0, 0))
    for y in range(SCREEN_HEIGHT):
        for x in range(SCREEN_WIDTH):
            if display[y][x]:
                pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x*SCALE, y*SCALE, SCALE, SCALE))
    pygame.display.flip()

def show_welcome_screen(screen, clock):
    font = pygame.font.SysFont("Consolas", 20)
    messages = [
        "              Anish Bommena's Emulator ",
        "                     TETRIS GAME",
        "-----------------------------",
        "TETRIS CONTROLS:",
        "  - Q = Left",
        "  - E = Right",
        "  - W = Rotate",
        "  - S = Drop",
        
        "Press ENTER to start the game",
    ]

    while True:
        screen.fill((0, 0, 0))
        for i, msg in enumerate(messages):
            text = font.render(msg, True, (255, 255, 255))
            screen.blit(text, (40, 40 + i * 30))
        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH * SCALE, SCREEN_HEIGHT * SCALE))
    pygame.display.set_caption("Anish Bommena's TETRIS Emulator")
    clock = pygame.time.Clock()

    show_welcome_screen(screen, clock)

    chip8 = Chip8()
    chip8.load_rom("TETRIS.ch8")

    while True:
        update_keys(chip8)
        chip8.emulate_cycle()
        draw(screen, chip8.get_display())
        clock.tick(FPS)

if __name__ == "__main__":
    main()
