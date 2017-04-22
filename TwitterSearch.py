import tkinter as tk
import tweepy

CONSUMER_KEY = 'CgttBoHkNZxIfrckK2GVRadLU'
CONSUMER_SECRET = 'VBKObpCgxxyZF8P2yd4vwy8UQajRX6XyA0O586tf6qIwL6dJO4'
ACCESS_TOKEN = '3437097531-QYRVTjkDhryDG0GU6qi5A3a2KKioKBihXcSvK7S'
ACCESS_TOKEN_SECRET = 'mJnCLV6uRKHkOesfjD2IoZEyTetJZq8cYaQqvX04nKERk'

class Politician:
    def __init__(self, name, username, aff_scale):
        self.name = name
        self.username = username
        self.aff_scale = aff_scale


    def get_tweets(self):
        return api.user_timeline(screen_name=self.username)

    def get_tweets_with(self, issue_list):
        tweets = self.get_tweets()
        hits = []
        for t in tweets:
            for issue in issue_list:
                if issue.upper() in t.text.upper():
                    hits.append(t)
        return hits

    def get_box_color(self):
        if self.aff_scale < 0:
            return (int(255*(1+self.aff_scale)), int(255*(1+self.aff_scale)), 255)
        elif self.aff_scale > 0:
            return (255, int(255*(1-self.aff_scale)), int(255*(1-self.aff_scale)))
        else:
            return (255, 255, 255)

class Issue:
    def __init__(self, text):
        self.text = text



policians = [
    Politician("Donald Trump", "realDonaldTrump", 1.5),
    Politician("Bernie Sanders", "BernieSanders", 9001),
    Politician("Hillary Clinton", "HillaryClinton", -45),
    Politician("Ted Cruz", "tedcruz", 999999999)
]



class MainWindow:
    def __init__(self, politicians, issues):
        self.root = tk.Tk()
        self.root.wm_title("Twitter Search")

        # tk.Label(self.root, text="Issues").grid(row=0, column=0)
        # self.search_box = tk.Entry(self.root)
        # self.search_box.grid(row=1, column=0)
        self.politicians = politicians
        self.politicians_frame = tk.LabelFrame(self.root, text="Politicians", padx=10, pady=10)
        self.render_politicians()
        self.politicians_frame.grid(row=1, column=0, sticky="N")

        self.issues = issues
        self.issues_frame = tk.LabelFrame(self.root, text="Issues", padx=10, pady=10)
        self.issues_frame.grid(row=1, column=1)
        self.render_issues()

    def render_politicians(self):
        for y in range(len(self.politicians)):
            p = self.politicians[y]
            tk.Label(self.politicians_frame, text=p.name).grid(row=y, column=0)
            p.selected = tk.BooleanVar(False)
            tk.Checkbutton(self.politicians_frame, variable=p.selected).grid(row=y, column=1)

    def render_issues(self):
        for y in range(len(self.issues)):
            i = self.issues[y]
            tk.Label(self.issues_frame, text="\"" + i.text + "\"").grid(row=y, column=0)
            i.selected = tk.BooleanVar(False)
            tk.Checkbutton(self.issues_frame, variable=i.selected).grid(row=y, column=1)

    def get_issues(self):
        return self.search_box.get()

    def mainloop(self):
        self.root.mainloop()


def get_tweets(screen_name):
    return




if __name__ == "__main__":
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    keys = ["health", "care", "bill", "mexico", "senate", "fox"]
    issues = [Issue(key) for key in keys]
    # for p in policians:
    #     tweets = p.get_tweets_with(issues)
    #     print("\n" + p.name + ":")
    #     for t in tweets:
    #         print(t.text + "\n")

    win = MainWindow(policians, issues)
    win.mainloop()