## Project configuration ##

Steps 1 & 2 : only the first time
Attention : Step 3 after each git clone !!

Use configure.sh to replace steps 3 and 4

1. Install cocoapods 

	sudo gem install cocoapods

2. Setup cocoapods

	pod setup --verbose

3. Download dependencies

	pod install

3. Open project in Xcode and build !

	open StoreIt.xcworkspace


## DB MEMO

mkdir /usr/local/var/postgres
initdb -D /usr/local/var/postgres