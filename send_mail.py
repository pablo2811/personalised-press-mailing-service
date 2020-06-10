
import smtplib
from email.mime.image import MIMEImage

import pymongo
from markdown2 import Markdown
from jinja2 import Environment, FileSystemLoader
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email
import datetime
import imaplib,os
import importlib,re,itertools


class MailSender:

    def __init__(self):
        self.me = "dailypressbriefing@gmail.com"
        self.password = "XXXXXXXXXX"
        self.template = "mail.html"
        self.pages = ["wyborcza","nytimes","theguardian","bussinesinsider","przegladsportowy","nature","theeconomist","onet","reuters","washingtonpost","tygodnikpowszechny","rzeczpospolita","dailymail","thetelegraph","financialtimes"]
        self.links = self.get_links()
        self.stupidpages = dict()
        self.users = self.read_users()
        self.cached_pages = dict()
        self.commands = []
        self.maindir = os.getcwd()
        self.papers = self.maindir + "\\journals"
        self.set()
        self.logs = ""

    def get_links(self):
        res = dict()
        with open("links.txt","r") as f:
            lines = f.readlines()
            for i in range(len(lines)):
                res[self.pages[i]] = lines[i].rstrip()
        return res

    def set(self):
        normal_comands = ["ADD", "JOIN", "DELETE", "UNSUBSCRIBE"]
        rescomm = []
        for e in normal_comands:
            rescomm += map(''.join, itertools.product(*((c.upper(), c.lower()) for c in e)))
        self.commands = rescomm
        res = []
        for el in self.pages:
            z = map(''.join, itertools.product(*((c.upper(), c.lower()) for c in el)))
            res += z
            for perm in res:
                self.stupidpages[perm] = perm.lower()


    def read_users(self):
        client = pymongo.MongoClient("mongodb+srv://prasaadmin123:prasaprasa123@press-zn9bb.mongodb.net/test?retryWrites=true&w=majority")
        project = client.PRESS
        users = project.users
        current_users = []
        x = users.find()
        for us in x:
            user = LocalUser(us["mail"],us["alias"],us["pages"])
            current_users.append(user)
        return current_users

    def user_exists(self,mail):
        client = pymongo.MongoClient(
            f"mongodb+srv://prasaadmin123:{self.password}@press-zn9bb.mongodb.net/test?retryWrites=true&w=majority")
        project = client.PRESS
        users = project.users
        for u in users.find():
            if u["mail"] == mail:
                return True
        return False

    def page_exist(self,page):
        return page in self.pages

    def add_user(self, mail, alias, pages):
        if "@" in mail and " " not in mail and not self.user_exists(mail):
            client = pymongo.MongoClient(
                f"mongodb+srv://prasaadmin123:{self.password}@press-zn9bb.mongodb.net/test?retryWrites=true&w=majority")
            project = client.PRESS
            users = project.users
            new = {
                "mail": mail,
                "alias": alias,
                "pages": pages
            }
            users.insert_one(new)
            self.logs += f"JOIN;{mail};{pages};{self.getLogDate()};103\n"
        else:
            self.logs += f"JOIN;{mail};{pages};{self.getLogDate()};203\n"


    def update_pages(self,mail,new_pages):
        if self.user_exists(mail):
            client = pymongo.MongoClient(
                f"mongodb+srv://prasaadmin123:{self.password}@press-zn9bb.mongodb.net/test?retryWrites=true&w=majority")
            project = client.PRESS
            users = project.users
            query = {"mail": mail}
            local = [page for page in new_pages if self.page_exist(page)]
            new = {"$set": {"pages": local}}
            self.getuser(mail).pages = local
            users.update_one(query, new)
        else:
            print("You are not a subscriber.")



    def add_page(self,mail,page):
        if self.user_exists(mail):
            client = pymongo.MongoClient(
                f"mongodb+srv://prasaadmin123:{self.password}@press-zn9bb.mongodb.net/test?retryWrites=true&w=majority")
            project = client.PRESS
            users = project.users
            current = users.find_one({"mail":mail})["pages"]
            if page in current:
                print(f"{page} already in place.")
            else:
                if self.page_exist(page):
                    current.append(page)
                    self.update_pages(mail,current)
                    self.logs += f"ADD;{mail};{page};{self.getLogDate()};100\n"
                else:
                    self.logs += f"ADD;{mail};{page};{self.getLogDate()};200\n"
        else:
            self.logs += f"ADD;{mail};{page};{self.getLogDate()};201\n"


    def delete_page(self,mail,page):
        if self.user_exists(mail):
            client = pymongo.MongoClient(
                f"mongodb+srv://prasaadmin123:{self.password}@press-zn9bb.mongodb.net/test?retryWrites=true&w=majority")
            project = client.PRESS
            users = project.users
            current = users.find_one({"mail": mail})["pages"]
            if page not in current:
                self.logs += f"DELETE;{mail};{page};{self.getLogDate()};200\n"
            else:
                current.remove(page)
                self.update_pages(mail,current)
                self.logs += f"DELETE;{mail};{page};{self.getLogDate()};100\n"
        else:
            self.logs += f"DELETE;{mail};{page};{self.getLogDate()};201\n"

    def getuser(self,mail):
        for u in self.users:
            if u.mail == mail:
                return u

    def deleteUser(self,mail):
        if self.user_exists(mail):
            client = pymongo.MongoClient(
                f"mongodb+srv://prasaadmin123:{self.password}@press-zn9bb.mongodb.net/test?retryWrites=true&w=majority")
            project = client.PRESS
            users = project.users
            users.delete_one({"mail": mail})
            self.users.remove(self.getuser(mail))
            self.logs += f"UNSUBSCRIBE;{mail};x;{self.getLogDate()};102\n"
        else:
            self.logs += f"UNSUBSCRIBE;{mail};x;{self.getLogDate()};204\n"

    def parse(self,text,sender):
        text = ''.join(x for x in text if (x.isalpha() or x == "," or " "))
        text = re.findall(r"[\w']+", text)
        filtered = []
        cons_bad = 0
        for i in range(len(text)):
            if cons_bad > 10:
                break
            if text[i] in self.commands or text[i] in self.stupidpages.keys() or (i>0 and text[i-1] in self.commands):
                filtered.append(text[i])
                cons_bad = 0
            else:
                cons_bad += 1

        i = 0
        while i < len(filtered):
            if filtered[i] in self.commands:
                g = filtered[i].upper()
                if g == "JOIN" and i + 1 < len(filtered):
                    if filtered[i+1] in self.stupidpages.keys(): # we assume that user don't have username equal to page
                        alias = ""
                        i = i + 1
                    else:
                        alias = filtered[i+1]
                        i = i + 2
                    pag = []
                    while i < len(filtered) and filtered[i] not in self.commands:
                        if filtered[i] in self.stupidpages.keys():
                            pag.append(self.stupidpages[filtered[i]])
                        i += 1
                    self.add_user(sender,alias,pag)
                elif g == "ADD" or g == "DELETE":
                    i += 1
                    pag = []
                    while i < len(filtered) and filtered[i] not in self.commands:
                        if filtered[i] in self.stupidpages.keys():
                            pag.append(self.stupidpages[filtered[i]])
                        i += 1
                    if g == "ADD":
                        for p in pag:
                            self.add_page(sender,p)
                    else:
                        for p in pag:
                            self.delete_page(sender,p)
                elif g == "UNSUBSCRIBE":
                    self.deleteUser(sender)
                    break


    def read(self):
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(self.me, self.password)
        mail.list()
        mail.select("inbox")
        result, data = mail.search(None, "UNSEEN")
        ids = data[0]  # data is a list.
        id_list = ids.split()  # ids is a space separated string
        for id in id_list:
            result, data = mail.fetch(id, "(RFC822)")
            email_message = email.message_from_bytes(data[0][1])
            if email_message.is_multipart():
                for part in email_message.walk():
                    ctype = part.get_content_type()
                    cdispo = str(part.get('Content-Disposition'))
                    if ctype == 'text/plain' and 'attachment' not in cdispo:
                        body = part.get_payload(decode=True).decode("utf-8")  # decode
                        break
            else:
                body = email_message.get_payload(decode=True).decode("utf-8")
            try:
                res = re.sub(r'^>.*\n?', '', body, flags=re.MULTILINE)
                client = email_message.get("From")
                if "<" in client:
                    start = client.index("<")
                    end = client.index(">")
                    client = client[start+1:end]
                self.parse(res,client)
            except:
                pass
        self.updatelogs()

    def send_invitation(self):

        with open("invitation.txt") as inv:
            l = inv.readlines()
            body = " ".join(l)
            with open("mailsinvitation.txt","r") as f:
                l = f.readlines()
                l = [x.strip("\n") for x in l]
                for mail in l:
                    z = self.markdown_render(body,type="INVITATION")
                    self.send(z, mail)


    def md_personalised(self,user):
        body = f"# <center>ENJOY YOUR COFFEE, {user.alias}!</center>\n"
        body += "## <center>Essential. Compact. Yours.</center>\n"
        for page in user.pages:
            # performance boost
            body += f"<a href=\"{self.links[page]}\"><img src=\"cid:{page}\"></a>\n\n"
            try:
                if page not in self.cached_pages.keys():
                    module = importlib.import_module("journals."+page)
                    rendered = module.data()
                    self.cached_pages[page] = rendered
                    body += rendered
                else:
                    body += self.cached_pages[page]
            except:
                pass
        return body

    def sites_update_all(self):
        for u in self.users:
            self.sites_update_one(u)

    def sites_update_one(self,user):
        res = f"# We have some good news {user.alias}!\n"
        with open("new_pages.txt") as f:
            x = f.readlines()
            for el in x:
                res += el
        html = self.markdown_render(res,type="UPDATE")
        self.send(html,user.mail)


    def markdown_render(self,body,user=None,type="BRIEF"):
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template(self.template)
        markdowner = Markdown()
        markdown_content = markdowner.convert(body)
        title = ""
        if type == "BRIEF":
            title = f"{user.alias}'s press for {str(datetime.datetime.now()).split()[0]}."
        elif type == "INVITATION":
            title = "INVITATION"
        elif type == "UPDATE":
            title = "DAILYPRESS UPDATE"
        set_up = {'email_content': markdown_content, 'title': title}
        raw = template.render(set_up)
        return raw

    def updatelogs(self):
        os.chdir(self.maindir)
        with open("LOGS.txt","a") as logs:
            logs.write(self.logs)


    def sendallbriefs(self):
        for u in self.users:
            try:
                body = self.md_personalised(u)
                r = self.markdown_render(body,u)
                self.send(r, u.mail,photos=True)
            except:
                pass
        self.updatelogs()

    def sendone(self,mail):
        if self.user_exists(mail):
            us = self.getuser(mail)
            body = self.md_personalised(us)
            r = self.markdown_render(body,us)
            self.send(r,us.mail,photos=True)
        self.updatelogs()

    def getLogDate(self):
        x = str(datetime.datetime.now()).split()
        log_date = f"{x[0]}*{x[1][:5]}"
        return log_date

    def send(self,document,mail,photos=False):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"Press for {str(datetime.datetime.now()).split()[0]}."
        msg['From'] = self.me
        msg['To'] = mail
        try:
            final_mesg = MIMEText(document, 'html')
            if photos:
                os.chdir("loga")
                for p in self.getuser(mail).pages:
                    fp = open(f'{p}.png', 'rb')
                    msgImage = MIMEImage(fp.read())
                    msgImage.add_header('Content-ID', f'<{p}>')
                    msg.attach(msgImage)
                    fp.close()
                os.chdir("..")
            msg.attach(final_mesg)
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(self.me, self.password)
            server.sendmail(self.me,mail,msg.as_string().encode('utf-8'))
            self.logs += f"SEND;{mail};x;{self.getLogDate()};199\n"
            server.close()
        except:
            self.logs += f"SEND;{mail};x;{self.getLogDate()};299\n"



class LocalUser:
    def __init__(self,mail,alias,pages):
        self.mail = mail
        self.pages = pages
        self.alias = alias


