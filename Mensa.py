import urllib2
import telegram
import re

bot = telegram.Bot(token='278206043:AAH13RqZiG1AdqcUpTDNbtAB-N_bL9EGeR4')


response = urllib2.urlopen("http://www.werkswelt.de/?id=ingo").read()

foodReg = re.compile(r'Speiseplan.*', re.IGNORECASE)
pattern = re.compile(r'<\/br>(.*?)<\/br>(.*?)<\/br>.*?<\/br>\s+<\/br>', re.IGNORECASE)

food = foodReg.findall(response)[1]
#print response
# print food
food = pattern.findall(food)
result = []
for elem in food:
 
    firstelem = re.sub(r"<sup>.*?<\/sup>", "", elem[0])
    secondelem = re.sub(r"&nbsp;","",elem[1])
    secondelem = re.sub(r"\s{2,}","",secondelem)
    result.append(firstelem + " | " + secondelem)


result = "\n".join(result)
print result

updates = bot.getUpdates()

print(updates)

# print bot.getMe()