import tkinter as tk
import tweepy
import webbrowser

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
        try:
            return api.user_timeline(screen_name=self.username)
        except:
            return None

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




class EntryWindow:
    def __init__(self, politicians, issues):
        self.root = tk.Tk()
        self.root.wm_title("Twitter Search")

        # tk.Label(self.root, text="Issues").grid(row=0, column=0)
        # self.search_box = tk.Entry(self.root)
        # self.search_box.grid(row=1, column=0)
        self.politicians = politicians
        self.politicians_canvas = tk.Canvas(self.root, width=180)
        tk.Label(text="Politicians", font=("Helvetica", 20)).grid(row=0, column=0)
        self.politicians_frame = tk.LabelFrame(self.politicians_canvas, padx=10, pady=10)
        self.vsb = tk.Scrollbar(self.root, orient="vertical", command=self.politicians_canvas.yview)
        self.politicians_canvas.configure(yscrollcommand=self.vsb.set)
        self.politicians_canvas.grid(row=1, column=0)
        self.politicians_canvas.create_window((4, 4), window=self.politicians_frame, anchor="nw", tags="self.frame")
        self.vsb.grid(row=1, column=1, sticky="ns")
        self.politicians_frame.bind("<Configure>", self.onFrameConfigure)
        self.render_politicians()
        # self.politicians_frame.grid(row=1, column=0, sticky="N")

        self.issues = issues
        tk.Label(text="Issues", font=("Helvetica", 20)).grid(row=0, column=2)
        self.issues_frame = tk.LabelFrame(self.root, padx=10, pady=10)
        self.issues_frame.grid(row=1, column=2, sticky="N")
        self.render_issues()

        tk.Button(self.root, text="Search", font=("Helvetica", 10), command=self.search).grid(row=2, column=0, columnspan=3)

    def onFrameConfigure(self, event):
        self.politicians_canvas.configure(scrollregion=self.politicians_canvas.bbox("all"))

    def render_politicians(self):

        for y in range(len(self.politicians)):
            p = self.politicians[y]
            tk.Label(self.politicians_frame, text=p.name, font=("Helvetica", 10)).grid(row=y, column=0, sticky="E")
            p.selected = tk.BooleanVar(False)
            tk.Checkbutton(self.politicians_frame, variable=p.selected).grid(row=y, column=1)
        self.other_politician = tk.Entry(self.politicians_frame)
        self.other_politician.grid(row=len(self.politicians), column=0)
        self.other_politician_selected = tk.BooleanVar(False)
        tk.Checkbutton(self.politicians_frame, variable=self.other_politician_selected).grid(row=len(self.politicians), column=1)

    def render_issues(self):
        for y in range(len(self.issues)):
            i = self.issues[y]
            tk.Label(self.issues_frame, text="\"" + i.text.title() + "\"", font=("Helvetica", 10)).grid(row=y, column=0, sticky="E")
            i.selected = tk.BooleanVar(False)
            tk.Checkbutton(self.issues_frame, variable=i.selected).grid(row=y, column=1)
        self.other_issue = tk.Entry(self.issues_frame, width=15)
        self.other_issue.grid(row=len(issues), column=0)
        self.other_issue_selected = tk.BooleanVar(False)
        tk.Checkbutton(self.issues_frame, variable=self.other_issue_selected).grid(row=len(self.issues), column=1)

    def search(self):
        pols = [p for p in self.politicians if p.selected.get()]
        if self.other_politician_selected.get():
            pols.append(Politician(self.other_politician, self.other_politician, 0))
        issues = [i for i in self.issues if i.selected.get()]
        if self.other_issue_selected.get():
            issues.append(Issue(self.other_issue.get()))
        hits = search(pols, issues)
        ResultsWindow(hits, pols, issues).mainloop()

    def mainloop(self):
        self.root.mainloop()

class ResultsWindow:
    def __init__(self, hits, pols, issues):
        self.hits = hits
        self.hits.sort(key=lambda hit: hit[1].favorite_count, reverse=True)

        self.root = tk.Toplevel()
        self.root.wm_title("Search Results")

        tk.Label(self.root, text="Results", font=("Helvetica", 20)).grid(row=0, column=0)

        tk.Label(self.root, text="[" + ", ".join(["'" + i.text.title() + "'" for i in issues]) + "] found " + str(len(hits)) + " result" + ("","s")[len(hits) > 1]).grid(row=1, column=0, sticky="W")

        self.results_canvas = tk.Canvas(self.root, width=590, height=500)
        self.results_frame = tk.LabelFrame(self.results_canvas)

        self.vsb = tk.Scrollbar(self.root, orient="vertical", command=self.results_canvas.yview)
        self.results_canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.grid(row=2, column=1, sticky="ns")
        self.results_canvas.grid(row=2, column=0)
        self.results_canvas.create_window((4, 4), window=self.results_frame, anchor="nw", tags="self.frame")
        self.results_frame.bind("<Configure>", lambda event, canvas=self.results_canvas: self.onFrameConfigure(canvas))

        for y in range(len(hits)):
            hit = hits[y][1]
            text = hit.text
            name = hit.author.name
            print(name)
            pol = hits[y][0]
            box_color = pol.get_box_color()
            text_color = "black"
            if box_color[1] < 128:
                text_color = "white"
            box_color = "#" + hex(box_color[0])[2:] + hex(box_color[1])[2:] + hex(box_color[2])[2:]
            date = hit.created_at.strftime("%B %d, %Y")
            retweets = hit.retweet_count
            likes = hit.favorite_count
            hit_frame = tk.Frame(self.results_frame)
            text_frame = tk.LabelFrame(hit_frame, width=410, height=72, bg=box_color)
            tk.Label(text_frame, text=name, bg=box_color, fg=text_color).grid(row=0, column=0, sticky="W")
            tk.Label(text_frame, text=date, bg=box_color, fg=text_color).grid(row=0, column=1, sticky="E")
            try:
                tk.Label(text_frame, text=hit.text[:min(70, len(text))], bg=box_color, fg=text_color).grid(row=1, column=0, columnspan=2)
                if len(text) > 70:
                    tk.Label(text_frame, text=hit.text[70:], bg=box_color, fg=text_color).grid(row=2, column=0, columnspan=2)
            except:
                tk.Label(text_frame, text="An unsupported character was encountered.", bg=box_color, fg=text_color).grid(row=1, column=0, columnspan=2)
            stats_frame = tk.LabelFrame(hit_frame, bg=box_color, width=100, height=72)
            tk.Label(stats_frame, text="Retweets: " + str(retweets), bg=box_color, fg=text_color).grid(row=0)
            tk.Label(stats_frame, text="", bg=box_color, fg=text_color).grid(row=1)
            tk.Label(stats_frame, text="Likes: " + str(likes), bg=box_color, fg=text_color).grid(row=2)
            text_frame.grid_propagate(False)
            stats_frame.grid_propagate(False)
            text_frame.grid(row=0, column=0, sticky="E")
            stats_frame.grid(row=0, column=1, sticky="E")
            tk.Button(hit_frame, text="View Tweet", command=(lambda: self.open(hit)), height=4, bg=box_color, fg=text_color).grid(row=0, column=2, sticky="E")
            hit_frame.grid(row=y)

    def onFrameConfigure(self, canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def open(self, tweet):
        name = tweet.author.screen_name
        id = str(tweet.author.id_str)
        webbrowser.open_new("www.twitter.com/" + name)


    def mainloop(self):
        self.root.mainloop()



def search(pols, issues):
    hits = []
    for p in pols:
        tweets = p.get_tweets()
        if tweets is not None:
            for t in tweets:
                for i in issues:
                    if i.text.upper() in t.text.upper():
                        print("hit found")
                        hits.append((p, t))

    bad = []
    for i in range(len(hits) - 1):
        if hits[i][1].text == hits[i+1][1].text:
            bad.append(i + 1)
    for b in bad[::-1]:
        hits.pop(b)

    return hits



if __name__ == "__main__":
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    
    politicians = [
        Politician("Bernie Sanders", "BernieSanders", -.83),
        Politician("Elizabeth Warren", "SenWarren", -.82),
        Politician("Hillary Clinton", "HillaryClinton", -.64),
        Politician("Martin OMalley", "MartinOMalley", -.62),
        Politician("Andrew Cuomo", "NYGovCuomo", -.54),
        Politician("Jim Webb", "JimWebbUSA", -.53),
        Politician("Joe Biden", "JoeBiden", -.44),
        Politician("Barack Obama", "BarackObama", -.65),
        Politician("Chris Christie", "GovChristie", .25),
        Politician("Jon Huntsman", "JonHuntsman", .3),
        Politician("Jeb Bush", "JebBush", .42),
        Politician("Rick Snyder", "onetoughnerd", .43),
        Politician("John Kasich", "JohnKasich", .45),
        Politician("Rick Santorum", "RickSantorum", .47),
        Politician("Mitt Romney", "MittRomney", .5),
        Politician("Bobby Jindal", "BobbyJindal", .51),
        Politician("Donald Trump", "realDonaldTrump", .56),
        Politician("Carly Fiorina", "CarlyFiorina", .6),
        Politician("Mike Huckabee", "GovMikeHuckabee", .62),
        Politician("Marco Rubio", "marcorubio", .67),
        Politician("Rick Perry", "GovernorPerry", .69),
        Politician("Ben Carson", "RealBenCarson", .74),
        Politician("Mike Pence", "mike_pence ", .76),
        Politician("Scott Walker", "ScottWalker", .78),
        Politician("Ted Cruz", "tedcruz", .97),
        Politician("Rand Paul", "RandPaul", 1)
    ]
    politicians.sort(key=lambda pol: pol.name)

    keys = ["health", "care", "bill", "mexico", "senate", "fox"]
    issues = [Issue(key) for key in keys]

    win = EntryWindow(politicians, issues)
    win.mainloop()