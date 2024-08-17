# Messenger-Numbers

For people wondering how many messages they've exchanged with this fascinating stranger they've met a week ago at a pub. Or for those who just like knowing numbers.
Made beacause other versions didn't work.

---
### Data
Note: to use this script you'll need to manually download you data from Facebook / Messenger. Instructions below:

> To download messages from Facebook-Messenger (those are the ones from before E2E encryption): \
> https://accountscenter.facebook.com/info_and_permissions -> Your info... -> Download your info... -> choose .JSON format

> To download messages from Messenger App (post-e2e-encryption): \
> Account -> fully encrypted chats -> safe storage -> download data...

Unpack the  files  to convenient location - only the `inbox` folder is needed. \
If you want to merge data from Facebook-Messenger and Messenger App you'll have to manually copy the .JSON files into proper subfolder. It's pain because the conversation names are random numbers. I know.

---
### Usage

- `counter.py` - counts and displays stats for all chats (requires only Python3)
	1. open the file and edit the `inbox_path` so that it points to your shiny, new inbox folder
	2. (change how the data will be displayed)
	3. run the script
- `overtime.py` - plot specific chat over time (requires Python3 and matplotlib)
	1. open the file and edit the `folder_path` so that it points to the chat folder
	2. (change how the data will be displayed)
	3. run the script


