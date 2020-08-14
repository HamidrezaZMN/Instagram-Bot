from selenium import webdriver
import time, random

class InstagramBot():

    """
    NUMBER_OF_FOLLOWS: number of follows per hour
    MAX_FOLLOWINGS: max number of following that the page wants
    TIME_GAP: gap between each task
    count_follows: total number of follows that are made
    FOLLOW_METHOD: method--> follow or unfollow
    FOLLOWED_LIST: a list of followed users to unfollow from
    """
    NUMBER_OF_FOLLOWS = 15
    TIME_GAP = (3600-NUMBER_OF_FOLLOWS*63)/(2*NUMBER_OF_FOLLOWS) # 40:follow(30)+unfollow(33)
    count_follows = 0
    FOLLOW_METHOD = 1
    FOLLOWED_LIST = []

    def __init__(self, username, password, targets, MAX_FOLLOWINGS):

        self.username = username
        self.password = password
        self.targets = targets
        self.MAX_FOLLOWINGS = MAX_FOLLOWINGS # maximum number of followings
        self.base_url = 'https://www.instagram.com/'

        self.driver = webdriver.Chrome('chromedriver.exe') # or (executable_path=r'C:/chromedriver.exe')

        self.login()


    # logins to teh account
    def login(self):        
        self.driver.get(self.base_url+'accounts/login/')

        self.driver.find_element_by_name('username').send_keys(self.username)
        self.driver.find_element_by_name('password').send_keys(self.password)
        self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]').click() # log in button

        time.sleep(3)


    # navigates to the user's profile
    def nav_user(self, user):
        self.driver.get(self.base_url+user+'/')

        time.sleep(3)


    # follows user (that is navigated to)
    def follow_user(self, user, method=True):
        self.nav_user(user)

        if method: # follow
            # clicking follow button
            self.driver.find_element_by_xpath('//button[contains(text(), "Follow")]').click()
        else: # unfollow
            # clicking unfollow button
            self.driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "yZn4P", " " ))]').click()
            time.sleep(1)
            # accepting
            self.driver.find_element_by_xpath('//button[contains(text(), "Unfollow")]').click()

        time.sleep(1)


    # prints appropriately
    def printer(self, text):
        f = open('results.txt', 'a')
        f.write(text)
        f.close()
        print(text)


    # follows one of the target user's followers
    def follow_from_followers(self, method, target=False):
        if method: # follow
            # nav to the target
            self.nav_user(target)
            # click followers
            self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a').click()
            time.sleep(2)
            # choose one of them randomly
            FOLLOWERS = self.driver.find_elements_by_xpath('/html/body/div[4]/div/div/div[2]/ul/div//li')
            NUMBER_OF_FOLLOWERS = len(FOLLOWERS)
            RANDOM_FOLLOW = random.randint(1, NUMBER_OF_FOLLOWERS-1)
            
            CHOSEN_ID = self.driver.find_element_by_xpath(f'/html/body/div[4]/div/div/div[2]/ul/div/li[{RANDOM_FOLLOW}]/div/div[2]/div[1]/div/div/span/a').text
            time.sleep(1)
            # follow the user
            self.driver.find_element_by_xpath(f'/html/body/div[4]/div/div/div[2]/ul/div/li[{RANDOM_FOLLOW}]/div/div[3]/button').click()
            # add followed user to the list
            self.FOLLOWED_LIST.append(CHOSEN_ID)
            self.printer('\nf : '+CHOSEN_ID)
        else: # unfollow
            chosen_to_delete = random.choice(self.FOLLOWED_LIST)
            self.nav_user(chosen_to_delete)
            self.follow_user(chosen_to_delete, False)
            self.FOLLOWED_LIST.remove(chosen_to_delete)
            self.printer('\nuf : '+chosen_to_delete)


    # chooses a target appropriately, and at the wanted times, and follow
    def start_bot(self):
        loop_time = time.time()
        while int(time.time()-loop_time)<3600: #if needed
            if self.count_follows > self.MAX_FOLLOWINGS:
                if self.count_follows%self.NUMBER_OF_FOLLOWS==0:
                    self.FOLLOW_METHOD *= -1
            
            if self.FOLLOW_METHOD == 1:
                self.follow_from_followers(True, self.targets[self.count_follows%len(self.targets)])
            else:
                self.follow_from_followers(False)
            self.count_follows += 1
            
            time.sleep(self.TIME_GAP)
            self.TIME_GAP += random.randint(-1, 1) # to confuse instagram bot detector ~hackerman~
    

    
if __name__ == "__main__":
    total = time.time()

    f = open('info.txt')
    lines = [i.strip() for i in f.readlines()]
    USERNAME = lines[0]
    PASSWORD = lines[1]
    f.close()

    f = open('target_pages.txt')
    TARGETS = [i.strip() for i in f.readlines()]
    f.close()

    ig_bot = InstagramBot(USERNAME, PASSWORD, TARGETS, 100)
    print('\n\n-------------START BOT--------------\n\n')

    try:
        ig_bot.start_bot()

    except :
        print('\n*******AN ERROR OCCURED*******\n') 
        
    finally:
        print('\n\n-------------START BOT--------------\n\n')

        print(f'\n\ntime spent with this bot: {time.time()-total} seconds')
        print(f'number of follows and unfollows: {obj.count_follows}')
        print(f'the size of followed list:', len(obj.FOLLOWED_LIST))