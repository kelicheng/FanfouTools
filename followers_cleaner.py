# -*- coding: utf-8 -*-
import fanfou
import json
from pprint import pprint
from datetime import datetime
import urllib2

'''
Remove specific followers
'''

def get_followers(client):
	followers = []

	try:
		resp = client.followers.ids()
		# data = resp.json()
		data = json.loads(resp.read())

		for d in data:
			followers.append(d.encode('utf-8'))
		print followers
		return followers

	except urllib2.HTTPError:
		return get_followers(client)

def get_friends(client):
	friends = []

	try:
		resp = client.friends.ids()
	# data = resp.json()
		data = json.loads(resp.read())

		for d in data:
			friends.append(d.encode('utf-8'))
		return friends

	except urllib2.HTTPError:
		return get_friends(client)
	# print friends
	# print "[" + str(len(friends)) + " current friends.]"


def check(client, followers, days, whitelist):
	found_names = []
	found_ids = []
	unfound = []
	failed = []
	friends = get_friends(client)
	count = 0


	print "[Processing...]"
	for f in followers:
		count += 1

		# 排除互关或白名单用户
		if f in friends:
			continue
		if f in whitelist:
			continue

		try:
			print f
			# found_ids.append(f)

			resp = client.users.show({'id': f})
			data = json.loads(resp.read())


			# # 清除消息数小于100的用户
			if data['statuses_count'] < 100:
				found_ids.append(f)
				continue

			# # 清除X天内未更新用户
			if data['status']:
				time_string = data['status']['created_at'].encode('utf-8')
				created = datetime.strptime(time_string.replace('+0000 ', ''), '%a %b %d %H:%M:%S %Y')
				now = datetime.now()
				delta = (now - created).days
				if delta > days:
					found_names.append(data['name'].encode('utf-8'))
					found_ids.append(f)
					print "[" + str(len(found_names)) + " user(s) found. " + str(count) + "/" + str(len(friends)) + " processed.]"
			else:
				found_ids.append(f)
				continue


		except urllib2.HTTPError:
			unfound.append(f)
		except urllib2.URLError:
			print "[URL Error, please try later.]"
			failed.append(f)
		except KeyError:
			if f not in found_ids:
				print "[User " + f + " does not have any public status.]"


	if len(unfound) > 0:
		print "[User(s) not found: ]"
		for u in unfound: print u

	if len(failed) > 0:
		# print "[User(s) failed: ]"
		# for u in failed: print u
		try:
			check(client, failed, days, whitelist)
		except urllib2.HTTPError:
			check(client, failed, days, whitelist)


	print "[" + str(len(found_ids)) + " users found.]"
	for f in found_ids: print f

	confirm = raw_input("Are you sure to remove? (Y/N) ").upper()
	if confirm == "Y":
		remove(found_ids, client)


def remove(followers, client):
	count = 0
	# blocked = []
	for f in followers:
		try:
			client.blocks.create({'id': f})
			client.blocks.destroy({'id': f})
			# blocked.append(f)
			count += 1
		except urllib2.HTTPError:
			continue
		except urllib2.URLError:
			client.blocks.create({'id': f})
			client.blocks.destroy({'id': f})
		except KeyError:
			print "[ERROR]: user " + f + " not found."

	# for f in blocked:
	# 	try:
	# 		client.blocks.destroy({'id': f})
	# 	except urllib2.HTTPError:
	# 		continue
	# 	except urllib2.URLError:
	# 		client.blocks.destroy({'id': f})
	# 	except KeyError:
	# 		print "[ERROR]: user " + f + " not found."

	print "[" + str(count) + " users removed.]"



if __name__ == "__main__":
	accounts = {'账号ID-1': '账号密码-1', '账号ID-2': '账号密码-2'}
	oauth_token = ''
	oauth_token_secret = ''
	consumer_key = 'b7d7411a97bce56df29043c7de521395'
	consumer_secret = '576f9b944ac787983be03c54831adbeb'
	consumer = {'key': consumer_key, 'secret': consumer_secret}

	for userID in accounts:
		client = fanfou.XAuth(consumer, userID, accounts[userID])
		fanfou.bound(client)

		followers = get_followers(client)
		try:
			check(client, followers, 100, [])
		except urllib2.URLError:
			check(client, followers, 100, [])

		# update follower's document
		followers = get_followers(client)
		filename = userID + "_followers"
		file = open(filename, 'w')
		for f in followers:
			file.write(f + "\n")
		file.close()









