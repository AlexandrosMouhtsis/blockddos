import urllib.request
import re
import os
import time
import random
import ipaddress
from bs4 import BeautifulSoup

# δήλωση της λίστας useragents για να εμποδίσεi στον ιστότοπο τα πολλά αιτήματα
useragents=["Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",
			"Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25",
			"Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
			"Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0",
			"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
			"Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
			"Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16",
			"Opera/12.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.02",
			"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
			"Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.1 (KHTML, like Gecko) Maxthon/3.0.8.2 Safari/533.1",
			"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/601.1.56 (KHTML, like Gecko) Version/9.0 Safari/601.1.56",
			"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/601.2.7 (KHTML, like Gecko) Version/9.0.1 Safari/601.2.7",
			"Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",]

# τοποθεσίες που δημιουργήθηκαν με blogspot που έχουν την ίδια δομή
burls = ["http://sslproxies24.blogspot.it/", "http://proxyserverlist-24.blogspot.it/", "http://newfreshproxies24.blogspot.it/",
		"http://irc-proxies24.blogspot.it/", "http://getdailyfreshproxy.blogspot.it/", "http://www.proxyocean.com/",
		"http://www.socks24.org/",]

# urls vari
nurls = ["http://www.aliveproxy.com/socks5-list/", "http://www.aliveproxy.com/high-anonymity-proxy-list/", "http://www.aliveproxy.com/anonymous-proxy-list/",
		"http://www.aliveproxy.com/fastest-proxies/", "http://www.aliveproxy.com/us-proxy-list/", "http://www.aliveproxy.com/gb-proxy-list/",
		"http://www.aliveproxy.com/fr-proxy-list/", "http://www.aliveproxy.com/de-proxy-list/", "http://www.aliveproxy.com/jp-proxy-list/",
		"http://www.aliveproxy.com/ca-proxy-list/", "http://www.aliveproxy.com/ru-proxy-list/", "http://www.aliveproxy.com/proxy-list-port-80/",
		"http://www.aliveproxy.com/proxy-list-port-81/", "http://www.aliveproxy.com/proxy-list-port-3128/", "http://www.aliveproxy.com/proxy-list-port-8000/",
		"http://www.aliveproxy.com/proxy-list-port-8080/", "http://webanetlabs.net/publ/24", "http://www.proxz.com/proxy_list_high_anonymous_0.html",
		"http://free-proxy-list.net/", "https://www.socks-proxy.net/", "https://incloak.com/proxy-list/", "https://incloak.com/proxy-list/?start=64#list",
		"https://incloak.com/proxy-list/?start=128#list", "https://incloak.com/proxy-list/?start=192#list", "https://incloak.com/proxy-list/?start=256#list",
		"https://incloak.com/proxy-list/?start=320#list", "https://incloak.com/proxy-list/?start=384#list", "https://incloak.com/proxy-list/?start=448#list",
		"https://incloak.com/proxy-list/?start=512#list", "https://incloak.com/proxy-list/?start=576#list", "https://incloak.com/proxy-list/?start=640#list",
		"https://incloak.com/proxy-list/?start=704#list", "http://www.gatherproxy.com/", "http://sockslist.net/proxy/server-socks-hide-ip-address#proxylist",
		"http://sockslist.net/proxy/server-socks-hide-ip-address/2#proxylist", "http://sockslist.net/proxy/server-socks-hide-ip-address/3#proxylist", "http://sockslist.net/proxy/server-socks-hide-ip-address/4#proxylist",
		"http://skypegrab.net/proxy/http.txt", "http://skypegrab.net/proxy/socks.txt", "http://xseo.in/proxylist",
		"http://spys.ru/proxies/", "http://proxyb.net/",]

def initcheck():
	if os.getuid() != 0: # ελεγχος εκτέλεσης ως root
		print("You need to run this program as root.\n\n") # εκτύπωση ερωτήματος
		exit(0) # ως κανονικός χρήστης, βγαίνει από το πρόγραμμα
	else: # ως root συνεχίζει και συνεχίζεται
		pass

	if os.path.isfile("/sbin/ipset"): # έλεγχος αν το ipset είναι εγκατεστημένο στο σύστημα
		varchoice() # 
	else: # διαφορετικά πρέπει να το εγκαταστήσετε 
		try:
			os.system("apt-get install ipset") # debian based
			varchoice()
		except OSError:
			try:
				os.system("yum install ipset") # centos based
				varchoice()
			except OSError:
				try:
					os.system("pacman -S ipset") # arch based 
					varchoice()
				except OSError:
					try:
						os.system("dnf install ipset") # redhat based
						varchoice()
					except OSError: # αν δε μπορεί να το εγκαταστήσει μόνο του κάντε το χειροκίνητα 
						print ("You need to install ipset.\n")
						exit(0) # έξοδος απο το πρόγραμμα

def varchoice():
	global choice1
	global choice2
	global choice3
	global refreshsec

	choice1 = input ("\nDo you want to implement some basic iptables rules to prevent DoS? (Y/n): ")
	if choice1 == "y" or choice1 == "Y": # απαντάτε ναι, για εφαρμογή βασικών κανόνων
		os.system("iptables -F") # flash όλους του iptables κανόνες
		# Περιορίζει τη νέα κίνηση στη θύρα 80
		os.system("iptables -A INPUT -p tcp --dport 80 -m state --state NEW -m limit --limit 25/minute --limit-burst 100 -j ACCEPT")
		# Περιορίζει την καθιερωμένη κίνηση
		os.system("iptables -A INPUT -m state --state RELATED,ESTABLISHED -m limit --limit 25/second --limit-burst 25 -j ACCEPT")
		# Απορρίπτει παρωχημένα πακέτα
		os.system("iptables -A INPUT -s 10.0.0.0/8 -j DROP")
		os.system("iptables -A INPUT -s 169.254.0.0/16 -j DROP")
		os.system("iptables -A INPUT -s 224.0.0.0/4 -j DROP")
		os.system("iptables -A INPUT -d 224.0.0.0/4 -j DROP")
		os.system("iptables -A INPUT -s 240.0.0.0/5 -j DROP")
		os.system("iptables -A INPUT -d 240.0.0.0/5 -j DROP")
		os.system("iptables -A INPUT -s 0.0.0.0/8 -j DROP")
		os.system("iptables -A INPUT -d 0.0.0.0/8 -j DROP")
		os.system("iptables -A INPUT -d 239.255.255.0/24 -j DROP")
		os.system("iptables -A INPUT -d 255.255.255.255 -j DROP")
		# Σταματήστε τις επιθέσεις
		os.system("iptables -A INPUT -p icmp -m icmp --icmp-type address-mask-request -j DROP")
		os.system("iptables -A INPUT -p icmp -m icmp --icmp-type timestamp-request -j DROP")
		# Fuck όλα τα μη έγκυρα πακέτα
		os.system("iptables -A INPUT -m state --state INVALID -j DROP")
		os.system("iptables -A FORWARD -m state --state INVALID -j DROP")
		os.system("iptables -A OUTPUT -m state --state INVALID -j DROP")
		# Αποκλείει επιθέσεις RST
		os.system("iptables -A INPUT -p tcp -m tcp --tcp-flags RST RST -m limit --limit 2/second --limit-burst 2 -j ACCEPT")
	elif choice1 == "n" or choice1 == "N": # 
		os.system("iptables -F") # πληκτρολογήστε μόνο τους κανόνες iptables και μην προσθέσετε κανένα
	else: # εάν κάνετε ένα σφάλμα πληκτρολόγησης
		print ("")
		exit(0) # βγαίνει από το πρόγραμμα

	try: # λήξη χρόνου ανανέωσης του διακομιστή μεσολάβησης.
		refresh = int(input ("\nSet the time of proxies download refresh in minutes (5): "))
		refreshsec = refresh * 60 # μετατροπή σε δευτερόλεπτα
	except: # η προεπιλογή είναι 5 λεπτά αν κάνετε λάθη πληκτρολόγησης
		print ("5 minutes set!")
		refreshsec = 5 * 60

	choice2 = input ("\nDo you want to block also tor-exit-nodes? (y/N): ") # η επιλογή του μπλοκ κόμβων tor-exit-κόμβων
	if choice2 == "y" or choice2 == "Y":
		pass # για τώρα δεν κάνει τίποτα ... τότε θα ασχοληθούμε με αυτή την επιλογή2
	elif choice2 == "n" or choice2 == "N":
		pass # 
	else: # αν παρουσιαστεί σφάλμα πληκτρολόγησης
		print ("")
		exit(0) # έξοδος

	choice3 = input ("\nDo you want to start protection? (Y/n): ")
	if choice3 == "y" or choice3 == "Y" or choice3 == "":
		print ("")
		loop() # loop
	elif choice3 == "n" or choice3 == "N":
		print("")
		exit(0) # αλλιώς κλείνει
	else:
		print ("")
		exit(0) # 

def valid_ip(ip): # ip λειτουργία ελέγχου της εγκυρότητας επειδή κάποια ip που παίρνει grabban δεν είναι σε αυτο 
    try: # 
        ipaddress.IPv4Address(ip) # ipaddress επεξεργασία quell'ip
    except ipaddress.AddressValueError: # σφάλμα
        return False # τότε εξαλείφει
    else: # αλλιώς η ip είναι αληθές και αφήνει
        return True # με True Return

def inforgeget(): # λειτουργία αφιερωμένη μόνο στον ιστότοπο inforge.net που έχει διαφορετικό μηχανισμό
	try:
		req = urllib.request.Request("https://www.inforge.net/xi/forums/liste-proxy.1118/") # Σύνθεση req
		req.add_header("User-Agent", random.choice(useragents)) # τυχαία επιλογή χρήστη
		soup = BeautifulSoup(urllib.request.urlopen(req, timeout = 10)) # άνοιγμα url και μετατροπή σε πηγαίο κώδικα "soup"
		print ("\nDownloading from inforge.net in progress...")
		base = "https://www.inforge.net/xi/" # τη βάση του συνδέσμου, θα χρειαστούμε "πιο" παρακάτω
		for tag in soup.find_all("a", {"class":"PreviewTooltip"}):
			links = tag.get("href") # βρείτε συνδέσμους
			final = base + links # όλες οι συνδέσεις που βρέθηκαν
			result = urllib.request.urlopen(final) #
			for line in result :
				ip = re.findall("(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})", str(line)) # βρείτε ip proxy
				ipf = list(filter(lambda x: x if not x.startswith("1.5.") else None, ip)) # δεν αρπάζει το "falsoip" που ταιριάζει πάντα και ξεκινά με 1.5
				if ipf: # αν βρίσκει ip
					for x in ipf:
						if valid_ip(x): # και το ip είναι έγκυρο αφού έχει επεξεργαστεί στη λειτουργία valid_ip
							ipfinal = x # τότε ipfinal παίρνει το ip
							out_file = open("blacklist.txt","a")
							while True:
								out_file.write(x+"\n") # γράφει ip βρέθηκε
								out_file.close()
								break # όταν τελειώσει ο κύκλος
	except: # αν συμβεί κάτι κακό
		print("An error occurred, skipping to the next website.")

def blogspotget(url): # αυτή η δυνατότητα μεταφορτώνει επίσης διακομιστή μεσολάβησης από ιστοτόπους blogspot
	try:
		soup = BeautifulSoup(urllib.request.urlopen(url)) # 
		for tag in soup.find_all("h3", "post-title entry-title"): # βρίσκει στην πηγή οτι σχετικό με τους εξουσιοδοτημένους χρήστες
			links = tag.a.get("href")                             # παίρνει τους δεσμούς proxylist
			result = urllib.request.urlopen(links)                # ανοίγει τους συνδέσμους που βρέθηκαν
			for line in result :
				ip = re.findall("(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})", str(line)) # ψάξτε για ips: φέρτα σε σελίδες
				if ip: # αν βρεθεί η ip συνεχίζεται
					for x in ip:
						if valid_ip(x): # εάν η ip είναι έγκυρη
							ipfinal = x # είναι ενεργοποιημένη στο ipfinal
							out_file = open("blacklist.txt","a") #  γράψτε τις ip στο proxy.txt
							while True:
								out_file.write(x+"\n") # γράφει τις ip μια-μια στο αρχείο blacklist.txt
								out_file.close()
								break # ο κύκλος σταματάει μόλις ολοκληρωθεί
	except: # αν κάτι πάει στραβά
		print("An error occurred, skipping to the next website.") # 

def proxyget(url):
	try:
		req = urllib.request.Request(url) # url που αντιστοιχεί σε ένα σύνολο urls που καθορίζονται παρακάτω.
		req.add_header("User-Agent", random.choice(useragents)) # προσθέτει έναν τυχαίο παράγοντα-χρήστη από την παραπάνω λίστα
		sourcecode = urllib.request.urlopen(req, timeout = 10) # κατεβασε τη σελίδα προέλευσης κώδικα + χρονικό όριο που έχει οριστεί στο 10
		for line in sourcecode :
				ip = re.findall("(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})", str(line)) # ip proxy
				ipf = list(filter(lambda x: x if not x.startswith("0.") else None, ip)) # αποφεύγει ακόμη και ανεπιτυχή δανεισμό
				if ipf: # αν βρίσκει την ip συνεχίζεται
					for x in ipf:
						if valid_ip(x): # εάν η ip είναι έγκυρη
							ipfinal = x # είναι ενεργοποιημένη στο ipfinal
							out_file = open("blacklist.txt","a")
							while True:
								out_file.write(x+"\n") # γράφει τις ip μια-μια στο αρχείο blacklist.txt
								out_file.close()
								break # ο κύκλος σταματάει μόλις ολοκληρωθεί
	except:
		print("An error occurred, skipping to the next website.")

def proxylist(): # λειτουργία για τη δημιουργία proxylist
	global proxies
	print ("\nSetting up the blacklist...")
	entries = open("blacklist.txt").readlines() # η λίστα txt έχει διπλότυπα, έτσι ώστε:
	proxiesp = {tuple(x.strip().split(':')) for x in entries} # μετατρέπει πρώτα τη λίστα σε πλειάδα
	proxies = list(set(proxiesp)) # και στη συνέχεια να διπλασιαστεί ο διπλασιασμός
	print ("\nBlacklist Updated!\n")

def loop(): # αποτελεσματική λειτουργία του προγράμματος.
	global url
	while True: # τον άπειρο κύκλο
		try:

			out_file = open("blacklist.txt","w") # πρώτα από όλα
			out_file.write("") # διαγράφει τα προηγούμενα περιεχόμενα του blacklist.txt
			out_file.close()

			inforgeget() # αρχή της λήψης
			print("Current IPs in blacklist: %s" % (len(open("blacklist.txt").readlines()))) # αυτή η γραμμή εμφανίζει τον αριθμό των ips που βρέθηκαν

			if choice2 == "y": # εάν επιλέξατε να αποκλείσετε τους κόμβους tor-exit-exit, εκτελέστε τη διαδικασία
				print ("\nDownloading from torstatus.rueckgr.at in progress...")
				url = "https://torstatus.rueckgr.at/index.php?SR=Uptime&SO=Desc" # url exit κόμβους εξόδου
				try:
					proxyget(url) # και να το στείλετε στο proxyget
					print("Current IPs in blacklist: %s" % (len(open("blacklist.txt").readlines())))
				except: # μερικές φορές προκαλεί οργή
					try:
						proxyget(url) # και να το στείλετε στο proxyget
						print("Current IPs in blacklist: %s" % (len(open("blacklist.txt").readlines())))
					except:
						try:
							proxyget(url) # και να το στείλετε στο proxyget
							print("Current IPs in blacklist: %s" % (len(open("blacklist.txt").readlines())))
						except: # αν σε αυτές τις 3 προσπάθειες αποτύχει τότε εκτυπώσε ότι δεν κατάφερε και θα περάσει στην επόμενη λήψη
							print ("Tor exit nodes download failed.")
			else: # αλλιώς περνάει
				pass

			print ("\nDownloading from blogspot in progress...")
			for position, url in enumerate(burls): # που απαριθμείται χρησιμοποιείται για τον αριθμό του τρέχοντος αριθμού τοποθεσίας
				blogspotget(url) # 
				print("Completed downloads: (%s/%s)\nCurrent IPs in blacklist: %s" % (position+1, len(burls), len(open("blacklist.txt").readlines())))

			print ("\nDownloading from various mirrors in progress...")
			for position, url in enumerate(nurls):
				proxyget(url)
				print("Completed downloads: (%s/%s)\nCurrent IPs in blacklist: %s" % (position+1, len(nurls), len(open("blacklist.txt").readlines())))

			print ("\nDownloading from proxymore in progress...")
			proxymore = ['http://www.proxymore.com/proxy-list-%d.html' % n for n in range(1, 15)] # για να πάρει ip και των 15 σελίδων
			for position, url in enumerate(proxymore):
				proxyget(url)
			print("Current IPs in blacklist: %s" % (len(open("blacklist.txt").readlines())))

			print ("\nDownloading from foxtools in progress...")
			foxtools = ['http://api.foxtools.ru/v2/Proxy.txt?page=%d' % n for n in range(1, 6)] # για να πάρει το ip και των 6 σελίδων
			for position, url in enumerate(foxtools):
				proxyget(url)
			print("Current IPs in blacklist: %s" % (len(open("blacklist.txt").readlines())))

			print ("\nDownloading from nntime in progress...")
			numbers = ["01","02","03","04","05","06","07","08","09",] # τους αριθμούς του ονόματος της ιστοσελίδας
			for n in numbers:
				nntime = ("http://nntime.com/proxy-updated-%s.htm" % n)
				proxyget(nntime)
				print("Current IPs in blacklist: %s" % (len(open("blacklist.txt").readlines())))
			nntime = ("http://nntime.com/proxy-updated-%s.htm" % n for n in range(10, 31)) # και από το 10 και μετά είναι αριθμοί χωρίς 0 μπροστά και μετά συνεχίσε κανονικά
			proxyget(nntime)
			print("Current IPs in blacklist: %s" % (len(open("blacklist.txt").readlines())))

			print ("\nDownloading from proxylistplus in progress...")
			url = "http://list.proxylistplus.com/Fresh-HTTP-Proxy"
			proxyget(url)
			print("Current IPs in blacklist: %s" % (len(open("blacklist.txt").readlines())))
			proxylistplus = ['http://list.proxylistplus.com/Fresh-HTTP-Proxy-List-%s' % n for n in range(2, 6)] # για να πάρει όλες τις ip από τη σελίδα 2 έως 6
			for position, url in enumerate(proxylistplus):
				proxyget(url)
			print("Current IPs in blacklist: %s" % (len(open("blacklist.txt").readlines())))

			proxylist() # και στο τέλος εκτελεί αυτή τη λειτουργία που δημιουργεί τη λίστα

			print ("\nImporting Blacklisted IPs... (It can take a while)\n")
			os.system("ipset create evil_ips iphash -!") # εδώ δημιουργούμε τον πίνακα "evil_ips" και την εντολή -! χρησιμεύει στην αποφυγή σφαλμάτων
			os.system("ipset flush evil_ips -!") # εδώ flush όλα τα παλιά ips που σώζονται στο evil_ips
			for proxy in proxies:
				os.system("ipset add evil_ips %s -!" % (proxy)) # εδώ βάζει όλα τα πληρεξούσια που κατέβασαν στο evil_ips
			os.system("iptables -A INPUT -m set --match-set evil_ips src -j DROP") # εισάγοντας τις μαύρες λίστες στο INPUT
			os.system("iptables -A OUTPUT -m set --match-set evil_ips dst -j DROP")
			os.system("iptables -A FORWARD -m set --match-set evil_ips src -j DROP") # τόσο στο FORWARD
			os.system("iptables -A FORWARD -m set --match-set evil_ips dst -j DROP")
			print ("\nBlacklisted IPs Imported!")
			print ("\nSleeping for the time set.")
			time.sleep(refreshsec) # είναι μέχρι το χρόνο που έχει καθοριστεί πριν (refreshsec) και ξεκινά ξανά
			print ("\n\nRestarting cycle...")

		except KeyboardInterrupt: # αν κλείσετε το πρόγραμμα με το Ctrl + C
			choice3 = input ("\nDo you want to flush iptables rules? (y/n): ")
			if choice3 == "y" or choice3 == "Y": # αν αποφασίσετε να αλλάξετε
				print ("\nFlushing iptables before exit...\n")
				os.system("iptables -F") # flush όλους τους κανόνες iptables
				os.system("ipset flush evil_ips") # και τους πίνακες του ipset
				exit(0) # και κλείνει.
			elif choice3 == "n" or choice3 == "N": # αν δεν θέλετε να φλασαρετε
				print ("")
				exit(0) # εξοδος
			else: # αν πληκτρολογείτε λάθος
				print ("")
				exit(0) # εξοδος


print ("\n\nWARNING: This program will erase ALL current iptables rules.")
print ("TIP: Press Ctrl+C during sleeping time to exit and flush iptables rules.\n")
initcheck() # για να ξεκινήσει η λειτουργία βρόχου () και στη συνέχεια το πρόγραμμα
