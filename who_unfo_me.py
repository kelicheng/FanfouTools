# from fanpy import *
import fanfou
import json

def get_followers(client):
	followers = []

	resp = client.followers.ids()
	# data = resp.json()
	data = json.loads(resp.read().decode('utf8'))


	for d in data:
		followers.append(d.encode('utf-8'))

	# print "[" + str(len(followers)) + " current followers.]"
	return followers


def read_past_followers(filename):
	try:
		with open(filename) as f:
			content = f.readlines()
		content = [x.strip() for x in content]
		return content
	except IOError:
		print "[No file found.]"
		return []


def check_and_block(past_followers, followers, client):
	num = 0
	for f in past_followers:
		if f not in followers:

			client.blocks.create({'id': f})
			num += 1
	# if num > 0: print "[" + str(num) + " user(s) blocked.]"
	print "[" + str(num) + "/" + str(len(past_followers)) + " user(s) blocked.]"

if __name__ == "__main__":
	accounts = {'账号ID-1': '账号密码-1', '账号ID-2': '账号密码-2'}
	consumer_key = 'b7d7411a97bce56df29043c7de521395'
	consumer_secret = '576f9b944ac787983be03c54831adbeb'
	consumer = {'key': consumer_key, 'secret': consumer_secret}

	for userID in accounts:
		# print "[Processing for " + userID + "...]"
		print userID + " "
		filename = userID + "_followers"
		client = fanfou.XAuth(consumer, userID, accounts[userID])
		fanfou.bound(client)


		past_followers = read_past_followers(filename)
		followers = get_followers(client)
		check_and_block(past_followers, followers, client)

		file = open(filename, 'w')
		for f in followers:
			file.write(f + "\n")
		file.close()

