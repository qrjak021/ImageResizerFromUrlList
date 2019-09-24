from tkinter import *
from tkinter.filedialog import *
import os
from PIL import Image
import urllib.request
import re
from threading import Thread


class ImageResizer:
    def __init__(self,root):
        self.root = root
   
        self.root.title('URL ImageResizer')
        self.root.grid_rowconfigure(0,minsize=30)
        self.lab = Label(root,text='Input image url:').grid(row=0,columnspan=2,padx=10)
        self.image_url = Entry(root,width=80)
        self.image_url.grid(row=0,column=2,columnspan=3,padx=10)

        self.root.grid_rowconfigure(1,minsize=30)
        self.lab = Label(root,text='OR').grid(row=1,column=2,columnspan=2,padx=10)

        self.root.grid_rowconfigure(2,minsize=30)
        self.button_resize = Button(root, text='Select .txt file with IMAGES URLS list', font='Ariel 10 bold', command=self.open_urls_list_file)
        self.button_resize.grid(row=2,column=1,columnspan=4,sticky=W+E,padx=(10,10))

        self.root.grid_rowconfigure(3,minsize=40)
        self.lab = Label(root,text='Set image WIDTH (px):').grid(row=3,column=1,padx=(10,0),sticky=E+W)
        self.image_width = Entry(root,width=10)
        self.image_width.grid(row=3,column=2,sticky=W+E,padx=(5,10))

        self.lab = Label(root,text='Set image HEIGHT (px):').grid(row=3,column=3,sticky=E)
        self.image_height = Entry(root,width=10)
        self.image_height.grid(row=3,column=4,sticky=W+E,padx=(5,10))
        
        
        self.root.grid_rowconfigure(4,minsize=40)
        self.scrollbar = Scrollbar(root)
        self.scrollbar.grid(row=4, column=5, sticky=N+S+E, padx=(0,10))
        self.textfield = Text(root)        
        self.textfield.grid(row=4,column=1,columnspan=4, padx=(10,0))
        self.textfield.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.textfield.yview)
                         
        self.root.grid_rowconfigure(5,minsize=40)
        self.button_resize = Button(root, text='RESIZE', font='Ariel 11 bold', command=self.run_resize)
        self.button_resize.grid(row=5,column=2,columnspan=2,sticky=W+E,padx=(10,10))

        self.root.grid_rowconfigure(6,minsize=40)
        self.button_resize = Button(root, text='ABOUT', font='Ariel 11 bold', command=self.about)
        self.button_resize.grid(row=6,column=1,sticky=W+E,padx=(10,10))

        self.root.grid_rowconfigure(6,minsize=40)
        self.button_exit = Button(root, text='EXIT', fg='red', font='Ariel 11 bold', command=self.exit)
        self.button_exit.grid(row=6,column=4,sticky=W+E,padx=(10,10))

        if not os.path.exists('Original_Images'):
                os.mkdir('Original_Images')
                
        if not os.path.exists('Resized_Images'):
                os.mkdir('Resized_Images')

        self.resized_images_dir_list =  os.listdir(os.path.join(os.getcwd(),'Resized_Images'))

        # Part of code for natural sorting. Credits goes to Jeff Atwood and Mark Byers on Stackoverflow
        # https://stackoverflow.com/questions/2669059/how-to-sort-alpha-numeric-set-in-python
        convert = lambda text: int(text) if text.isdigit() else text
        alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
        self.resized_images_dir_list_sorted = sorted(self.resized_images_dir_list, key = alphanum_key)
        
        self.textfield.insert(END,'List of files in Resized_Images directory:\n\n')
        
        for self.resized_image in self.resized_images_dir_list_sorted:
            self.textfield.insert(END,self.resized_image+'\n')
        
        self.root.mainloop()

    def run_resize(self):

        t1 = Thread(target=self.textfield.insert(END,'\nRESIZING IN PROGRESS...\nIMAGES ASPECT RATIO WILL BE MAINTAIN...\nALTERATIONS OF ENTERED WIDTH OR HEIGHT VALUES ARE POSSIBLE...\n\n'))
        t2 = Thread(target=self.resize_engine)
        t1.start()
        t2.start()
        
        
    def resize_engine(self):
       
        try:            
            if not hasattr(self,'urls_list_split'):               # if variable 'urls_list' not exists
                self.image_url_resize = [self.image_url.get()]    # make an array of one item from main window
            else:
                self.image_url_resize = self.urls_list_split      # already return as array

            
            self.image_W = int(self.image_width.get())
            self.image_H = int(self.image_height.get())
            
            for self.image_in_url in self.image_url_resize:
                                  
                try:
                    
                    self.image_number = os.listdir(os.path.join(os.getcwd(),'Resized_Images'))
                    self.i = len(self.image_number)

                    urllib.request.urlretrieve(self.image_in_url, os.path.join(os.getcwd(),'Original_Images', str(self.i)+'_Image.jpg'))
                    self.img = Image.open(os.path.join(os.getcwd(),'Original_Images', str(self.i)+'_Image.jpg'))
                    self.img.thumbnail((self.image_W,self.image_H))
                    self.image_W_resized, self.image_H_resized  = self.img.size
                    self.img.save(os.path.join(os.getcwd(),'Resized_Images', str(self.i)+'_ResizedImage_'+str(self.image_W_resized)+'x'+str(self.image_H_resized)+'.jpg'))

                    self.textfield.insert(END,os.path.join('Resized_Images',str(self.i)+'_ResizedImage_'+str(self.image_W_resized)+'x'+str(self.image_H_resized)+'.jpg','\n'))
                 

                except Exception as e:
                    self.textfield.insert(END,'\nLink '+ self.image_in_url + ' is corrupted..\n' + str(e) +'\n\n')
                

            self.textfield.insert(END,'IMAGE RESIZING FINISHED\n')
            self.textfield.see(END)

            del self.urls_list_split

        except AttributeError: # if self.urls_list_split has already been deleted
            pass

        except ValueError:
            self.textfield.insert(END,'NO URL || HEIGHT AND WIDTH ARE NOT ENTERED OR VALUES ARE NOT AN INTEGER\n')


    def open_urls_list_file(self):
    
        self.open_url_address_file = askopenfilename(title = "Select file with image url addresses",filetypes = [("url txt file","*.txt")])

        with open(self.open_url_address_file,'r') as file:
            self.urls_list = file.read()

        if ('http://' in self.urls_list) or ('https://' in self.urls_list):
            self.textfield.delete('1.0',END)
            self.urls_list_split = self.urls_list.split()
            self.textfield.insert(END, self.open_url_address_file+ ' file with urls list loaded... \nSet image dimensions and click RESIZE.')
            return self.urls_list_split

        else:
            self.textfield.delete('1.0',END)
            self.textfield.insert(END,"CAN'T FIND PROPER URL ADRESS IN SELECTED FILE. CHOOSE ANOTHER FILE\n")
        
    def about(self):
        self.about = Toplevel(self.root)
        self.about.title('About')
        self.lab_name = Label(self.about,text='Author: Aleksandar Kurjakov', font='Ariel 12 bold').grid(row=1,column=1,padx=20,pady=15)
        self.lab_contact = Label(self.about,text='Contact: kurjak021@gmail.com', font='Ariel 12 bold').grid(row=2,column=1,padx=20,pady=15)
        self.lab_version = Label(self.about,text='URL ImageResizer V1.0', font='Ariel 10 bold').grid(row=3,column=1,padx=20,pady=15)
        self.about.focus_set()                                                        
        self.about.grab_set()

    def exit(self):
        self.root.destroy()
            
root = Tk()
App = ImageResizer(root)
