import time
from plane_sprite import *


class MainGame(object):
    def __init__(self):
        # 1.创建游戏窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        # 2.创建游戏时钟
        self.clock = pygame.time.Clock()
        # 3.调用私有方法，精灵和精灵组的创建
        self.__creat_sprites()
        # 4.设置定时器事件-创建敌机
        pygame.time.set_timer(CREAT_ENEMY_SPRITES, 1000)
        pygame.time.set_timer(FIRE_EVENT, 300)
        # 5.记录分数
        self.scores = 0

    def __creat_sprites(self):
        # 创建背景精灵和精灵组
        bg1 = Background()
        bg2 = Background(True)
        self.back_group = pygame.sprite.Group(bg1, bg2)
        # 创建敌机精灵和精灵组
        self.enemy_group = pygame.sprite.Group()
        # 创建英雄精灵和精灵组
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

    def start_game(self):
        """开始游戏"""
        while True:
            # 1.设置游戏帧率
            self.clock.tick(60)
            # 2.事件监听
            self.__event_handler()
            # 3.碰撞检测
            self.__check_cash()
            # 4.更新绘制精灵组
            self.__update_sprites()
            # 5.更新显示
            self.__show_scores(0, 0)
            self.show_bullets()
            pygame.display.update()

    def __event_handler(self):
        """事件监听"""
        is_firing = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__game_over()
            elif event.type == CREAT_ENEMY_SPRITES:
                self.enemy_group.add(Enemy())
            elif event.type == FIRE_EVENT:
                is_firing = 1
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.hero.speed_x = SPEED_X
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.hero.speed_x = -SPEED_X
        if pygame.key.get_pressed()[pygame.K_UP]:
            self.hero.speed_y = -SPEED_Y
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.hero.speed_y = SPEED_Y
        if pygame.key.get_pressed()[pygame.K_SPACE] and is_firing:
            self.hero.fire()

    def __check_cash(self):
        """碰撞检测"""
        # 1. 检测子弹与敌机
        start_num = len(self.hero.bullets)
        for enemy in self.enemy_group:
            if enemy.modnum == 1:
                if pygame.sprite.spritecollide(enemy, self.hero.bullets, True):
                    self.hero.bullets_num += 2
                    enemy.modnum = 2
        end_num = len(self.hero.bullets)
        self.scores += start_num - end_num
        # 2. 检测敌机与英雄
        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, False)
        if enemies:
            for n in (1, 2, 3, 4):
                time.sleep(0.2)
                self.screen.blit(pygame.image.load("./images/me_destroy_%d.png" % n), self.hero.rect)
                self.screen.blit(pygame.image.load("./images/enemy1_down%d.png" % n), enemies[0].rect)
                pygame.display.update()
            self.hero.kill()
            self.__game_over()

    def __update_sprites(self):
        self.back_group.update()
        self.enemy_group.update()
        self.hero_group.update()
        self.hero.bullets.update()
        self.back_group.draw(self.screen)
        self.enemy_group.draw(self.screen)
        self.hero_group.draw(self.screen)
        self.hero.bullets.draw(self.screen)

    def __show_scores(self, *args, center=False):
        scores_surface = fontObj.render("scores:%d" % self.scores, True, (0, 0, 0))
        scores_rect = scores_surface.get_rect()
        if not center:
            scores_rect.x = args[0]
            scores_rect.y = args[1]
        else:
            scores_rect.center = args
        self.screen.blit(scores_surface, scores_rect)

    def show_bullets(self):
        if self.hero.bullets_num > 0:
            string = "bullets:%d" % self.hero.bullets_num
        else:
            string = "no bullet!"
        tip_surface = fontObj.render("%s" % string, True, (0, 0, 0))
        tip_rect = tip_surface.get_rect()
        tip_rect.x = 0
        tip_rect.y = 20
        self.screen.blit(tip_surface, tip_rect)

    def __game_over(self):
        """游戏结束"""
        self.screen.blit(pygame.image.load("./images/gameover.png"), GAMEOVER_RECT)
        self.__show_scores((240, 350), center=True)
        data = open("./game_data")
        high_score = int(data.read())
        data.close()
        if self.scores > high_score:
            high_score = self.scores
        high_score_surface = fontObj.render("high scores:%d" % high_score, True, (0, 0, 0))
        high_score_rect = high_score_surface.get_rect()
        high_score_rect.center = (240, 390)
        self.screen.blit(high_score_surface, high_score_rect)
        pygame.display.update()
        data = open("./game_data", "w")
        data.write(str(high_score))
        time.sleep(0.5)
        pygame.quit()
        exit()


if __name__ == '__main__':
    PlaneGame = MainGame()
    PlaneGame.start_game()
