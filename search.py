# -*- coding: utf-8 -*-
import fanfou
import json
import urllib2

whitelist = ['不想被删掉的关键词1', '不想被删掉的关键词2']

def search(client, keyword):
	statuses = []
	resp = client.search.user_timeline({'q': keyword, 'count': 60, 'mode': 'lite'})
	data = json.loads(resp.read())

	for d in data:
		text = d['text'].encode('utf-8')
		print(text)
		statuses.append(d['id'])

	return statuses


def cleanup(client, statuses):
	count = 0
	for r in statuses:
		try:
			client.statuses.destroy({'id': r})
			count += 1
		except urllib2.HTTPError:
			print r + " not found."

	print "[" + str(count) + " statuses deleted.]"

if __name__ == "__main__":
	accounts = {'账号ID-1': '账号密码-1', '账号ID-2': '账号密码-2'}
	consumer_key = 'b7d7411a97bce56df29043c7de521395'
	consumer_secret = '576f9b944ac787983be03c54831adbeb'
	consumer = {'key': consumer_key, 'secret': consumer_secret}

	for userID in accounts:
		# print "[Processing for " + userID + "...]"
		client = fanfou.XAuth(consumer, userID, accounts[userID])
		fanfou.bound(client)

		statuses = search(client, '关键词')

		print "[" + str(len(statuses)) + " statuses found. ]"
		if len(statuses) > 0:
			confirm = raw_input("Are you sure to remove? (Y/N) ").upper()
			if confirm == "Y":
				cleanup(client, statuses)

