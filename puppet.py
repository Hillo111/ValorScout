import tkinter as tk
import json
import qrcode
from PIL import Image, ImageTk
import cv2 as cv
from qrstuff import make_qr_code, scan_qr_code

class CounterApp:
    def __init__(self, root: tk.Tk, fields={}, settings={}):
        self.root = root
        self.root.geometry("400x400")
        self.settings = settings
        self.settings_items = {}

        self.settings_button = tk.Button(self.root, command=self.open_settings, text='Settings')
        self.settings_button.pack(anchor=tk.NW)
        
        self.load_form_button = tk.Button(self.root, command=lambda: self.load_form(json.loads(scan_qr_code())), text='Load form')
        self.load_form_button.pack(anchor=tk.NE)

        self.inputs_frame = tk.Frame(self.root)
        self.inputs_frame.pack()

        self.fields = {}
        self.load_form(fields)
            
        self.export_button = tk.Button(self.root, command=self.export_data, text='Show QR code')
        self.export_button.pack()

    def load_form(self, fields):
        if self.fields != {}:
            for field in self.fields:
                self.fields[field]['frame'].destroy()

        self.fields = {}
        for field in fields:
            fi = fields[field]
            d = {'type': fi['type']}
            if fi['type'] == 'counter':
                d['value'] = fi['value'] if 'value' in fi else 0
                d['frame'] = tk.Frame(self.inputs_frame)
                d['name_label'] = tk.Label(d['frame'], text=field)
                d['count_label'] = tk.Label(d['frame'], text='0')
                d['inc'] = tk.Button(d['frame'], text='+', command=lambda n=field: self.update_value(n, +1))
                d['dec'] = tk.Button(d['frame'], text='-', command=lambda n=field: self.update_value(n, -1))
                d['frame'].pack()
                d['name_label'].pack()
                d['dec'].pack(side='left')
                d['count_label'].pack(side='left')
                d['inc'].pack(side='left')
            elif fi['type'] == 'text':
                d['value'] = ''
                d['frame'] = tk.Frame(self.inputs_frame)
                d['label'] = tk.Label(d['frame'], text=field)
                d['input'] = tk.Text(d['frame'], height = 5, width = 20)
                if 'value' in fi:
                    d['input'].insert("1.0", fi['value'])
                    d['value'] = fi['value']
                d['input'].bind("<KeyRelease>", lambda event, n=field: self.update_value(n))
                d['frame'].pack() 
                d['label'].pack()
                d['input'].pack()
            elif fi['type'] == 'selector':
                d['value'] = ''
                d['frame'] = tk.Frame(self.inputs_frame)
                d['label'] = tk.Label(d['frame'], text=field)
                d['label'].pack()
                d['var'] = tk.StringVar()
                d['buttons'] = []
                for option in fi['options']:
                    d['buttons'].append(tk.Radiobutton(d['frame'], text=option, variable=d['var'], value=option, command=lambda n=field: self.update_value(n)))
                    d['buttons'][-1].pack(side='left')
                d['frame'].pack()

            self.fields[field] = d

    def update_value(self, field, v=None):
        if self.fields[field]['type'] == 'counter':
            self.fields[field]['value'] += v
            self.fields[field]['count_label'].config(text=str(self.fields[field]['value']))
        elif self.fields[field]['type'] == 'text':
            self.fields[field]['value'] = str(self.fields[field]['input'].get(1.0, 'end-1c'))
        elif self.fields[field]['type'] == 'selector':
            self.fields[field]['value'] = str(self.fields[field]['var'].get())

    def export_data(self):
        d = {'data': {}}
        for field in self.fields:
            print(self.fields[field])
            d['data'][field] = self.fields[field]['value']
        d['info'] = self.settings
        print(d)
        img = make_qr_code(json.dumps(d))
        img.save('test.png')
        self.tk_image = ImageTk.PhotoImage(img)
        self.image_label = tk.Label(self.root, image=self.tk_image)
        self.image_label.place(x=0, y=0, relwidth=1, relheight=1)  # Image label covers the entire window
        self.destroy_button = tk.Button(self.root, command=self.destroy_qrcode_label, text='Hide code')
        self.destroy_button.place(x=0, y=0)
        self.root.geometry(f'{img.size[0] + 50}x{img.size[1] + 50}')

    def destroy_qrcode_label(self):
        self.image_label.destroy()
        self.destroy_button.destroy()

    def open_settings(self):
        self.settings_frame = tk.Frame(self.root)
        for s in self.settings:
            d = {
                'label': tk.Label(self.settings_frame, text=s),
                'input': tk.Text(self.settings_frame, height=5, width=10)
            }
            d['label'].pack()
            d['input'].insert("1.0", str(self.settings[s]))
            d['input'].pack()
            self.settings_items[s] = d

        self.close_settings_button = tk.Button(self.settings_frame, command=self.save_settings, text='Save')
        self.close_settings_button.pack()
        self.settings_frame.place(x=0, y=0, relwidth=1, relheight=1)

    def save_settings(self):
        for s in self.settings:
            new_v = self.settings_items[s]['input'].get(1.0, "end-1c")
            if type(self.settings[s]) == int:
                new_v = int(new_v)
            self.settings[s] = new_v
            for k in ('label', 'input'):
                self.settings_items[s][k].destroy()
        self.close_settings_button.destroy()
        self.settings_frame.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CounterApp(root, {}, {'ID': 3, 'name': 'bob'})
    root.mainloop()
