
from enum import EnumMeta
import bs4
from cssutils.tokenize2 import has_at
import requests
from bs4 import BeautifulSoup as bs
import os
from urllib.parse import urljoin
import glob
import re
import json
import tinycss
import bs4
import tinycss2
import requests
import urllib.request 
import glob
import os
import cssutils
import json
import time


class CreateReact:
    def __init__(self,dir_name,url):
        self.url =  url
        self.dir_name =  dir_name

    
    def getRequest(self):
                session = requests.Session()
                # set the User-agent as a regular browser
                session.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"

                # get the HTML content
                html = session.get(self.url).content

                # parse HTML using beautiful soup
                soup = bs(html, "html.parser")

                return soup

    def getImages(self):
        # get the JavaScript files
        script_files = []

        for script in self.getRequest().find_all("img"):
            if script.attrs.get("src"):
                # if the tag has the attribute 'src'
                script_url = urljoin(self.url, script.attrs.get("src"))
                script_files.append(script_url)
        return script_files

    def get_all_class(self,soup):
               
            class_list = []
            # get all tags
            so = bs(soup, "html.parser")
            tags = {tag.name for tag in so.find_all()}
            
            # iterate all tags
            for tag in tags:
                    ls = []
                    dic = {}
                    dic['tag'] = tag
                    class_list.append(dic)
            
                    # find all element of tag
                    for i in self.getRequest().find_all( tag ):
                        dicti = {}
                    
                        # if tag has attribute of class
                        if i.has_attr( "class" ):
                            print(i['class'])
                
                            if len( i['class'] ) != 0:
                                dicti['class'] = i['class']
                                class_list.append(dicti)
                        if i.has_attr("name") :
                            print(i['name'])
                            if len( i['name'] ) != 0:
                                dicti['name'] = i['name']
                                class_list.append(dicti)
                        if i.has_attr("id") : 
                            print(i['id'])
                            if len( i['id'] ) != 0:
                                dicti['id'] = i['id']
                                class_list.append(dicti)
            return class_list

    def opencss(self,path):
        for filename in glob.glob(os.path.join(path, '*.css')):
                with open(filename, 'r') as f:
                    text = f.read()
                    sheet = cssutils.parseString(str(text))
                    empty_list = []
                    for rule in sheet:
                        if rule:
                            try:
                                dictii = {}
                                selector = rule.selectorText
                                styles = rule.style.cssText
                                dictii['selector'] = selector
                                dictii['value'] = styles
                                print(dictii)
                                empty_list.append(dictii)
                            except:
                                pass
                    with open(f"{filename}.json", "w") as f:
                        json.dump(empty_list, f,indent=4) 
                    print(empty_list)


    def getCss(self):
    # get the CSS files
        css_files = []
        for css in self.getRequest().find_all("link"):
            if css.attrs.get("href"):
                # if the link tag has the 'href' attribute
                css_url = urljoin(self.url, css.attrs.get("href"))
                css_files.append(css_url)
        return css_files

    def class_to_json(self,dirname,filename):
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        file_path = os.path.join(dirname, f"{filename}.json")
        data =  self.get_all_class()
        with open(file_path, "w") as f:
            json.dump(data, f,indent=4) 
            print(data)


    def download_filess(self,url: str, dest_folder: str):
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)  # create folder if it does not exist

        filename = url.split('/')[-1].replace(" ", "_")  # be careful with file names
        file_path = os.path.join(dest_folder, filename)

        r = requests.get(url, stream=True)
        if r.ok:
            try:
                print("saving to", os.path.abspath(file_path))
                with open(file_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024 * 8):
                        if chunk:
                            f.write(chunk)
                            f.flush()
                            os.fsync(f.fileno())
            except:
                pass
        else:  # HTTP status code 4XX/5XX
            print("Download failed: status code {}\n{}".format(r.status_code, r.text))
    def download_to_save(self):
        css_urls =  self.getCss()
        for i in css_urls:
            dd  =  self.download_filess(i,"css")


    def download_images(self):
        css_urls =  self.getImages()
        for i in css_urls:
            dd  =  self.download_filess(i,"img")

    
    def create_new_css(self,css_path,class_path,filepath):
        empty_string = []
        for filename in glob.glob(os.path.join(css_path, '*.json')):
            with open(filename, 'r') as f:
                    text = f.read()
                    js =  json.loads(text)
                    print(class_path)
                    for fm in glob.glob(os.path.join(class_path,"*.json")):
                        
                        with open(fm,'r') as c:
                            class_m = c.read()
                            class_l = json.loads(class_m)
                            for m in js:
                                selector = m['selector']
                                for k in class_l:
                                    try: 
                                        dicti = {}
                                        print(k['tag'],"tag class....")
                                        class_ki = k['tag']
                                        if class_ki in selector.lower():
                                           dicti[f"{selector}"] =  {m['value']}
                                        #    file_poa = os.path.join(class_path, f"{filepath}class.css")
                                           css_writer = """%s {
                                                %s
                                            }
                                            """%(selector,m['value'])
                                           empty_string.append(css_writer)
                                           print(dicti)
                                           
                                    except:
                                        try:
                                            dicti1 = {}
                                            print(k['id'],"id class....")
                                            class_kim = "#"+k['id']
                                            if class_kim in selector.lower():
                                    
                                                dicti1[f"{selector}"] =  {m['value']}
                                                # file_pa = os.path.join(class_path, f"{filepath}class.css")
                                                css_writer2 = """%s {
                                                %s
                                                    }
                                                    """%(selector,m['value'])
                                                empty_string.append(css_writer2) 
                                                print(dicti1)
                                                
                                        except:
                                            try:
                                                dicti2 = {}
                                                print(k['name'],"name class....")
                                                class_kimm = k['name']
                                                if class_kimm in selector.lower():
                                                   
                                                    dicti2[f"{selector}"] =  {m['value']}
                                                    # file_pia = os.path.join(class_path, f"{filepath}class.css")
                                                    css_writer3 = """%s {
                                                            %s
                                                        }
                                                        """%(selector,m['value'])
                                                    empty_string.append(css_writer3) 
                                                    print(dicti2)
                                                    
                                            except:
                                                dicti3 = {}
                                                print(k['class'],"class class....")
                                                class_kimm = k['class']
                                                for o in class_kimm:
                                                    if o in selector.lower():
                                                        
                                                        dicti3[f"{selector}"] =  {m['value']}
                                                        # file_pppa = os.path.join(class_path, f"{filepath}class.css")
                                                        css_writer4 = """%s {
                                                                %s
                                                            }
                                                            """%(selector,m['value'])
                                                        empty_string.append(css_writer4)
                                                        print(dicti3)

        file_pppa = os.path.join(class_path, f"{filepath}class.css")
        with open(file_pppa, "w") as ff:
            ff.write("\n".join(empty_string))                    

                                
    def read_css_to_json(self):
        download_css = self.download_to_save()
        read_css = self.opencss("css")

    def all_divs(self,tag):
        file_pathb = self.dir_name + "/" + "src" +"/" + "components"
        if not os.path.exists(file_pathb):
                os.makedirs(file_pathb)
        divs =  self.getRequest().find_all(tag)
        nh = 0
        for d in divs:
            if d is not None:
                file_path2 = self.dir_name + "/" + "src" +"/" + "components" + "/" + f"{nh}"
                if not os.path.exists(file_path2):
                    os.makedirs(file_path2)
                completeName = os.path.join(file_path2,f"Div{nh}.js")
                file1 = open(completeName, "w")
                string = str(bs(str(d),"html.parser").prettify())
                ssp = bs(str(d),"html.parser").prettify()
                # file1.write(svt.format(f"Div{nh}",string,f"Div{nh}"))
                file1.write(

                    """
                function Div%s() {
                        return (
                            %s
                        );
                        }

                export default Div%s;

        """ % (nh,string,nh)
                )
                file1.close()
                cs = self.get_all_class(ssp)
                if not os.path.exists(file_path2):
                    os.makedirs(file_path2)
                file_path = os.path.join(file_path2, f"{nh}class.json")
                with open(file_path, "w") as f:
                    json.dump(cs, f,indent=4) 
                    print(cs)
                self.create_new_css("css",file_path2,f"{nh}")
                
                nh +=1

    def create_react_app(self):
        kk = os.system(f"npx create-react-app {self.dir_name}")
        print(kk)
        download_cdd = self.read_css_to_json()
        self.download_images()
        self.all_divs("body")
        
        cm =  os.chdir(f"{self.dir_name}")
        run =  os.system("yarn start")
        return "Done"

    

app = CreateReact("whatsapp","https://web.whatsapp.com/")
kk = app.create_react_app()
print(kk)
