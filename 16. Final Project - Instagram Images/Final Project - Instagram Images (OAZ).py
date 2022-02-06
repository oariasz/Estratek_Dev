from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from sympy import imageset
from xlsxwriter import Workbook
import os
import requests
import shutil


'''
Instagram
——————————
User: oariasz2020
Pass: M…1
'''
# target_username='claherrera96', 

'''
def __init__(self, username='oariasz2020', password='Miramar1', target_username='cotufacnnutella', 
                 path='/Users/omararias/OneDrive/Estratek/Pub/Dev/Webscraping with Python/16. Final Project - Instagram Images/img'):'''

class App:
    def __init__(self, username='oariasz2020', password='Miramar1', target_username='cotufacnnutella', 
                 path='/Users/oariasz/OneDrive/Estratek/Pub/Dev/Webscraping with Python/16. Final Project - Instagram Images'):
        self.username = username
        self.password = password
        self.target_username = target_username
        self.path = path + '/' + target_username
        # self.driver = webdriver.Opera()
        # self.driver = webdriver.Chrome('/Users/omararias/OneDrive/Estratek/Pub/Dev/Webscraping with Python/15. Selenium/chromedriver')
        self.driver = webdriver.Safari()
        self.driver.maximize_window() # For maximizing window
        self.driver.implicitly_wait(20) # gives an implicit wait for 20 seconds
        
        self.error = False

        self.main_url = 'https://instagram.com'
        self.driver.get(self.main_url)
        
        #write log in fuction
        self.log_in()
    
        if self.error is False:
            self.close_dialog_box()     # Cierra la caja de diálogo que aparece al entrar en la cuenta de Instagram
            sleep(2)
            self.open_target_profile()    # Busca la cuenta destino de la que se van a descargar las imágenes
        if self.error is False:
            sleep(2)
            self.scroll_down()          # Hace el scroll de todas las imágenes disponibles
        if self.error is False:
            if not os.path.exists(self.path):
                os.mkdir(self.path)
            self.download_images()
            
        sleep(3)
        self.driver.close()
        sleep (2)
        print ('Todo OK')
        
    def __enter_password(self, pass_field):
        for car in self.password:
            # print("\n",car)
            pass_field.send_keys(car)
        return 0
    
    # NO USAR:  Esto es solo para demostrar cómo cerrar una ventana indeseada (Tutorial)
    def __close_windows(self):
        try:
            self.drive.switch_to_window(self.driver.window_handles[1])     # Cierra la ventana settings que se abrió por error de Google Chrome
            sleep(2)
            self.driver.close()
            self.driver.switch_to_window(self.driver.window_handles[0])    # Vuelve a la ventana inicial donde estaba Instagram
        except:
            print("Error: Problemas con el cierre del de la ventana indeseada al entrar (caso Tutorial)")
            self.error = True            
             
    # Cierra el diálog box que aparece al loguearse en Instagram        
    def close_dialog_box(self):
        # Cierra el diáglo de entrada "Quiere guardar el password desde este navegador?"
        try:
            sleep(2)
            ahorano_button = self.driver.find_element(By.XPATH,'//*[@id="react-root"]/section/main/div/div/div/div/button')
            ahorano_button.click()        
        except:
            print("Problemas con el cierre del diálogo")
            self.error = True
    
    # Abre la página de Instagram de la cuenta destino
    def open_target_profile(self):
        try:
            search_bar = self.driver.find_element(By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')
            '''
            search_bar.send_keys(self.target_username)
            sleep(3)
            search_bar.send_keys(Keys.RETURN)
            sleep(3)
            search_bar.send_keys(Keys.RETURN)
            search_bar.send_keys(Keys.RETURN)
            search_bar.submit()
            '''  
            target_profile_url = self.main_url + '/' + self.target_username + '/'
            self.driver.get(target_profile_url)
        except:
            print('Error: Buscando la cuenta destino de la que se van a bajar las imágenes')
            self.error = True              
            
    # Hace scroll down en la página destino de Instagram para cargar todas las imágenes posible       
    def scroll_down(self):
        try:
            no_of_posts = self.driver.find_element(By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/span/span')
            no_of_posts = str(no_of_posts.text).replace('.','').replace(',','')        # elimina todos los puntos o comas de millares
            self.no_of_posts = int(no_of_posts)
            if self.no_of_posts > 12:
                no_of_scrolls = int(self.no_of_posts/12) + 3     # 3 de holgura para garantizar que se llegue hasta el fondo
                for value in range(no_of_scrolls):
                    self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                    sleep(1)
            print ("Número de Posts: ", no_of_posts)       
        except:
            print('Error: haciendo el scroll de la imágenes en la cuenta destino')
            self.error = True                
    
    def download_images(self):
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        all_images = soup.find_all('img')
        self.download_captions(all_images)
        print('Total de Imágenes: ', len(all_images))
        for index, image in enumerate(all_images):
            filename = 'img_' + str(index) + '.jpg'
            image_path = os.path.join(self.path, filename)        # Garantiza que funcione en cualquier OS
            link = image['src']
            print ('Descargando imagen: ', index)
            print ('Link: ', link)

            try:
                response = requests.get(link, stream = True)       # AQUI ESTÁ FALLANDO >>>>>>>>>
                with open(image_path, 'wb') as file:
                    shutil.copyfileobj(response.raw, file)    # carga lo que se trajo el request en forma binaria y lo guarda en un archivo
            except Exception as e1:
                sleep(3)
                print('No se pudo descargar la imagen número ', index,'.  Se hará otro intento\n')
                # Segundo intento
                try:
                    response = requests.get(link, stream = True)       # AQUI ESTÁ FALLANDO >>>>>>>>>
                    with open(image_path, 'wb') as file:
                        shutil.copyfileobj(response.raw, file)    # carga lo que se trajo el request en forma binaria y lo guarda en un archivo
                except Exception as e:
                    print (e)
                    print('No se pudo descargar la imagen número ', index)
                    print('Link de la imagen ---> ', link)

    
    def download_captions(self, images):
        captions_folder_path = os.path.join(self.path,'captions')
        if not os.path.exists(captions_folder_path):
            os.mkdir(captions_folder_path)
        self.download_captions2excel(images, captions_folder_path)    
        '''
            for index, image in enumerate(images):
                try:
                    caption = image['alt']
                except KeyError:
                    caption = "Imagen " + index + ': Sin título'
                file_name = 'caption_' + str(index) + '.txt'
                file_path = os.path.join(captions_folder_path, file_name)
                link = image['src']
                with open(file_path, 'wb') as file:
                    file.write(str('link: ' + str(link) + '\n' + 'caption' + caption).encode())
        '''
                 
    def download_captions2excel(self, images, captions_path):
        workbook = Workbook(os.path.join(captions_path, 'captions.xlsx'))
        worksheet = workbook.add_worksheet()
        row = 0
        worksheet.write(row, 0, 'Imagen')    # 3 ----> row number, column number, value
        worksheet.write(row, 1, 'Caption')   
        row += 1

        for index, image in enumerate(images):
            filename = 'image_' + str(index) + 'jpg'
            try:
                caption = image['alt']
            except KeyError:
                caption = "Imagen " + index + ': Sin título'
            worksheet.write(row, 0, filename)
            worksheet.write(row, 1, caption)
            row += 1
        workbook.close()
                
        captions_folder_path = os.path.join(self.path,'captions')
        if not os.path.exists(captions_folder_path):
            os.mkdir(captions_folder_path)
            for index, image in enumerate(images):
                try:
                    caption = image['alt']
                except KeyError:
                    caption = "Imagen " + index + ': Sin título'
                file_name = 'caption_' + str(index) + '.txt'
                file_path = os.path.join(captions_folder_path, file_name)
                link = image['src']
                with open(file_path, 'wb') as file:
                    file.write(str('link: ' + str(link) + '\n' + 'caption' + caption).encode())              

    # Pasos iniciales para loguearse en la página de instagram.com
    def log_in(self,):
        try:
            # Introduce login name
            sleep(3)
            login_name = self.driver.find_element(By.XPATH,'/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input')
            # login_name = self.driver.find_element(By.XPATH,'//*[@id="loginForm"]/div/div[1]/div/label/input')

                
            # Introduce el password de Instagram
            login_pass = self.driver.find_element(By.XPATH,'/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input')
            login_name.send_keys(self.username)
            self.__enter_password(login_pass)

            # Presiona el botón de login
            login_pass.submit()
            # login_button = self.driver.find_element(By.XPATH,'//*[@id="loginForm"]/div/div[3]/button/div')
            # login_button.click()
                
            sleep(3)
                    
        except:
            print('Error: Introduciendo el login name')
            self.error = True
                                 

if __name__ == '__main__':
    app = App()
    


