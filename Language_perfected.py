######## Imports ########
from selenium import webdriver
import keyboard
import time
from tkinter import *
from tkinter import messagebox

activated = False # Program is turned off

words = []
matchingwords = []

email = "your@email" # Your email
password = "Password" # Your password

origin = ''

def login():
    global driver
    driver = webdriver.Chrome("C:\\Users\harry\Documents\chromedriver.exe") # Where your chrome driver is
    driver.get("https://www.educationperfect.com/app/#/login") # Opens website
    time.sleep(5)

    userinput = driver.find_element_by_id("login-username").click()
    keyboard.write(email) # Types email

    passwordinput = driver.find_element_by_id("login-password").click()
    keyboard.write(password) # Types password

    loginbutton = driver.find_element_by_id("login-submit-button").click() # Clicks the login button

def scrape_answer_sheet():
    try:
        txt = []
        
        allelements = driver.find_elements_by_xpath("//div[contains(@class,'preview-grid ng-isolate-scope')]") # Gets all of the elements inside the table
        for i in allelements:
            if i.text not in txt:
                txt.append(i.text)  # Appends the text value

        clean_and_sort(txt)
        messagebox.showerror(title = 'ERROR', message="Sucessful")
    except:
        messagebox.showerror(title = 'ERROR', message="Couldn't scrape data")

def clean_and_sort(txt):
    global words, matchingwords
    text = txt[0] # Makes text 1 string
    text = text.split("\n") # Splits all the values into one array
    words = text[0::2] # Sets words to one of the languages
    matchingwords = text[1::2] # Sets matchingwords to the other
    print(words)

def start():
    global activated
    activated = True

    while activated == True:
        time.sleep(0.5) # Makes the program wait for the next question
        try: # Try loop so if an error occurs the program will not crash
            scrape_question()
        except:
            messagebox.showerror(message='Program stopped')
            break

def stop():
    global activated
    activated = False
    messagebox.showerror(message='Program stopped')
    
def scrape_question():
    global txtquestion

    questiontxt = driver.find_elements_by_xpath("//div[contains(@id,'question-block')]")
    for i in questiontxt:
        txtquestion = i.text

    if ("starts with") or ("ends with") in txtquestion:
        txtquestion, waste = txtquestion.split(" (")
    if "he," in txtquestion:
        pass

    elif "," in txtquestion:
        txtquestion = txtquestion.replace(',',';')

    i = index_question()
    output_on_screen(i)

def index_question():
    global origin
    try:
        if txtquestion in words:
            origin = 'words'
            i = words.index(txtquestion)
            return i

        elif txtquestion in matchingwords:
            origin = 'matching'
            i1 = matchingwords.index(txtquestion)
            return i1
    except:
        messagebox.showerror(title = 'ERROR', message="Question doesn't exist")

def output_on_screen(i):
    global origin

    answer = driver.find_element_by_xpath("//input[contains(@id,'answer-text')]").click()

    if origin == 'words':

        otherword = str(matchingwords[i])
        if ";" in otherword:
            otherword = otherword.replace(';', ',')
        keyboard.write(otherword)
        keyboard.press_and_release('enter')

    elif origin == 'matching':

        word = str(words[i])
        if ";" in word:
            word = word.replace(';', ',')
        keyboard.write(word)
        keyboard.press_and_release('enter')
        

    elif origin != ('words' or 'matching'):
        messagebox.showerror(title = 'ERROR', message="Something went wrong")

def ui():
    root = Tk()
    root.title("Language perfected (a rip-off of ken's (in python (so better (in every way))))")
    root.minsize(width=400,height=400)
    root.geometry("600x500")
    
    headingFrame1 = Frame(root,bg="#FFBB00",bd=5)
    headingFrame1.place(relx=0.2,rely=0.1,relwidth=0.6,relheight=0.16)
    headingLabel = Label(headingFrame1, text="Welcome to \n Language Perfected", bg='black', fg='white', font=('Courier',15))
    headingLabel.place(relx=0,rely=0, relwidth=1, relheight=1)
    
    btn1 = Button(root,text="Login",bg='black', fg='white', command=login)
    btn1.place(relx=0.28,rely=0.4, relwidth=0.45,relheight=0.1)
    
    btn2 = Button(root,text="Get words",bg='black', fg='white', command=scrape_answer_sheet)
    btn2.place(relx=0.28,rely=0.5, relwidth=0.45,relheight=0.1)
    
    btn3 = Button(root,text="Start",bg='green', fg='white', command=start)
    btn3.place(relx=0.28,rely=0.6, relwidth=0.45,relheight=0.1)
    
    root.mainloop()

keyboard.add_hotkey('ctrl+shift+e', start)
keyboard.add_hotkey('ctrl+shift+z', stop)

ui()
