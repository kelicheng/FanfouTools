# from fanpy import *
import fanfou
import json
from pprint import pprint
from datetime import datetime
import urllib2

def get_friends(client):
	friends = []

	resp = client.friends.ids()
	# data = resp.json()
	data = json.loads(resp.read())

	for d in data:
		friends.append(d.encode('utf-8'))
	# print friends
	print "[" + str(len(friends)) + " current friends.]"
	return friends


def check(client, friends, days):
	found_names = []
	found_ids = []
	unfound = []
	count = 0

	print "[Processing...]"
	for f in friends:
		count += 1
		try:
			resp = client.users.show({'id': f})
			data = json.loads(resp.read())
			# data = resp.json()
			# pprint(data['status'])

			if data['status']:
				time_string = data['status']['created_at'].encode('utf-8')
			else:
				continue

			created = datetime.strptime(time_string.replace('+0000 ', ''), '%a %b %d %H:%M:%S %Y')
			now = datetime.now()
			delta = (now - created).days
			# print delta
			if delta > days:
				found_names.append(data['name'].encode('utf-8'))
				found_ids.append(f)
				print "[" + str(len(found_names)) + " user(s) found. " + str(count) + "/" + str(len(friends)) + " processed.]"
		except urllib2.HTTPError:
			unfound.append(f)
		except urllib2.URLError:
			continue
		except KeyError:
			found_ids.append(f)
			print "[User " + f + " does not have any status.]"



	print "[User(s) not found: ]"
	for u in unfound: print u

	print "[Users not updated for " + str(days) + " days/ has no status: ]"
	for f in found_names: print f
	confirm = raw_input("Are you sure to remove? (Y/N) ").upper()
	if confirm == "Y":
		remove(found_ids, client)

def remove(friends, client):
	count = 0
	for f in friends:
		try:
			client.friendships.destroy({'id': f})
			count += 1
		except urllib2.HTTPError:
			continue
		except urllib2.URLError:
			continue
	print "[" + str(count) + " users removed.]"


if __name__ == "__main__":
	accounts = {'账号ID-1': '账号密码-1', '账号ID-2': '账号密码-2'}
	days = 100
	oauth_token = ''
	oauth_token_secret = ''
	consumer_key = 'b7d7411a97bce56df29043c7de521395'
	consumer_secret = '576f9b944ac787983be03c54831adbeb'
	consumer = {'key': consumer_key, 'secret': consumer_secret}

	for userID in accounts:
		client = fanfou.XAuth(consumer, userID, accounts[userID])

		fanfou.bound(client)

		friends = get_friends(client)
		check(client, friends, days)