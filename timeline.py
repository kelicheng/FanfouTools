# -*- coding: utf-8 -*-
import fanfou
import json
import urllib2

blacklist = ['希望被删掉的关键词1', '希望被删掉的关键词2']
whitelist = ['不想被删掉的关键词1', '不想被删掉的关键词2']

def get_timeline(client):
	statuses = []
	resp = client.statuses.user_timeline({'count': 1, 'mode': 'lite'})
	data = json.loads(resp.read())
	total = data[0]['user']['statuses_count']

	num_pages = int(total/60)+1
	for page in range(1, 20):
		print "********** PAGE " + str(page) + " ************"
		resp = client.statuses.user_timeline({'count': 60, 'page': page})
		data = json.loads(resp.read())

		for d in data:
			text = d['text'].encode('utf-8')


			# # 字数小于200且不含图片
			# if (len(text) < 200) and ('photo' not in d):
			# 	pass
			# 	# print(text)
			# 	# statuses.append(d['id'])
			# # 是回复他人的消息
			# elif d['in_reply_to_status_id'] != '':
			# 	# print(text)
			# 	statuses.append(d['id'])
			# # 包含关键词‘...‘
			# elif '...' in text:
			# 	print(text)
			# 	statuses.append(d['id'])
			# else:
			# 	# print d['text'].encode('utf-8')
			# 	pass

			f1 = [b in text for b in blacklist]
			f2 = [w not in text for w in whitelist]

			if any(f1) and all(f2):
				print(text)
				print(d['id'])
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

		statuses = get_timeline(client)

		print "[" + str(len(statuses)) + " statuses found. ]"
		if len(statuses) > 0:
			confirm = raw_input("Are you sure to remove? (Y/N) ").upper()
			if confirm == "Y":
				cleanup(client, statuses)

