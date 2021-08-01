from telegram import Update
from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram.ext import CallbackContext
from telegram.ext import Updater
from telegram.ext import Filters 
from telegram.ext import MessageHandler
import API
#import finder 
from selenium import webdriver
from time import sleep

button_help = '/help'
version = API.__version__
password = API.password
indentifiation = 0
count_reg_users = 0
find_text = '33'
search_read_to_begin = False

def button_help_handler(update: Update,context: CallbackContext):
	update.message.reply_text(
		text = f'''
		Привет,это бот Find Vidios,благодаря этому боту \n ты сможешь найти какое либо видео на ютубе!!

		Бот сделан благодаря библиотекам - python-telegram-bot И selemium

		by  Danil Yazvitskiy
        (что бы посмотреть команды,введи /cmd)

        {version}''',
        
        reply_markup = ReplyKeyboardMarkup(
		    keyboard=[
		        [
		            KeyboardButton(text='/cmd'),
		        ],
	    ],
	    resize_keyboard=True
	)        
	)	
     
def cmd_handler(update: Update,context: CallbackContext):
   update.message.reply_text(
      text = '''
      Команда поиска видео на YouTube - /search_videos вопрос''',
        reply_markup = ReplyKeyboardRemove(),

   )  



def finder_handler(update: Update,context: CallbackContext):
    search = find_text 
    search_ready = 'https://www.youtube.com/results?search_query=' + search
    driver = webdriver.Chrome()
    driver.get(search_ready)
    sleep(2)
    videos = driver.find_elements_by_id('video-title')
    for i in range(len(videos)):
        update.message.reply_text(
		    text = videos[i].get_attribute('href'),
	    )
    driver.quit()
	    	


def password_handler(update: Update,context: CallbackContext):
	update.message.reply_text(
		text = 'Добро пожаловать в приложение Find_Youtube,для продолжения введите пароль:'
	)	
def password_check_handler(update: Update,context: CallbackContext): 
	global indentifiation, count_reg_users
	indentifiation += 1
	count_reg_users += 1
	print(f'''Зарегистрировался новый пользователь!
		Всего пользователей:{count_reg_users}''')
	update.message.reply_text(
		text = '''Пользователь зарегистрирован...

		Для продолжения напишите /help'''

	)	


def message_handler(update: Update,context: CallbackContext):
    global find_text
    #main cmd
    text = update.message.text
    if text == button_help and indentifiation == 1:
    	return button_help_handler(update=update,context=context)
    if search_read_to_begin == True:
    	return finder_handler(update=update,context=context)


    if text[:14] == '/search_videos' and indentifiation == 1:
    	find_text = text[14:]
    	return finder_handler(update=update,context=context)

    if text == '/find' and indentifiation == 1:
    	return find_handler(update=update,context=context)

    if text == '/cmd' and indentifiation == 1:
    	return cmd_handler(update=update,context=context)
    reply_markup = ReplyKeyboardMarkup(
		keyboard=[
		    [
		        KeyboardButton(text=button_help),
		    ],
	    ],
	    resize_keyboard=True
	)
    

    #registr
    if text == password and indentifiation == 0:
        return password_check_handler(update=update,context=context)
    if text == '/start' and indentifiation == 0:
        return password_handler(update=update,context=context)
    if indentifiation == 0:
        update.message.reply_text(
		    text='Для начала введите команду /start',
	    )
    if indentifiation == 1:
        update.message.reply_text(
		    text='Я ботяра работяга!',
	    )    	    

def main():
	print('''Start!\n
		..........................,d888888888b,
.........................,dP"'................`"Qb,
...............,d88buP"..................."Qud88b,
.............dP".....8'...........................`8..... "Qb
...........dP".....::8.._.:...@;.._..;@..:._..8::....."Qb
..........,8'......: P"..............` '............"Qb::.....8,
..........dP.....:::8(...........`--^--'..........)8:::.......b
.........8'.......::::"Qba,.....,......,......,adP"::::......`8
.......,8...........::::::,p`""..............""'q,::::::.........8,
......,d'..........:::::,d'......................`b,:::::.........b,
.....,d'...........:::: d'........................`b::::::.........b,
....,d'.......q888q8b,.d......,p.......q,......,d8p888p.....b,
....d'......d",.....;..`b,....8,.........,8.....,d'...,"b.......`b
...,8......8.`.....`.....b,.....`b,..,d'.....,d'.... ...'.8......8,'
....d..,.`b,............`b..a88a..a88a..d'...........,d'.....,p
..`q,.....`b,............8.......8.8.......8............,d "...,p'
....`"Q888`b,.....`Q888P"."Q888P.Q888.'......,d'888P"'
................"Q88P".........................."Q88P''')
	print(version)
	updater = Updater(
        token = API.apikey,
		use_context=True,
	)

	updater.dispatcher.add_handler(MessageHandler(filters=Filters.all,callback=message_handler))


	updater.start_polling()
	updater.idle()

if __name__ == '__main__':
	main()