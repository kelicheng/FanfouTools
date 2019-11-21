# -*- coding: utf-8 -*-
import fanfou
import json
import urllib2

def get_timeline(client):
	replies = []
	resp = client.statuses.user_timeline({'count': 60, 'page': 6})
	data = json.loads(resp.read())
	total = data[0]['user']['statuses_count']
	for d in data:
		# reply = d['in_reply_to_status_id'].encode('utf-8')
		print d
		if d['in_reply_to_status_id'] != "":
			replies.append(d['id'])
	return replies


def cleanup(client, replies):
	count = 0
	for r in replies:
		client.statuses.destroy({'id': r})
		count += 1
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

		replies = get_timeline(client)

		print "[" + str(len(replies)) + " statuses found. ]"
		if len(replies) > 0:
			confirm = raw_input("Are you sure to remove? (Y/N) ").upper()
			if confirm == "Y":
				cleanup(client, replies)