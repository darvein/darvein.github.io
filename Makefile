run:
	@echo "Running hugo server"
	#bash recents.sh
	hugo --cleanDestinationDir
	hugo server --watch --noHTTPCache --disableFastRender -c content -D -E -F -s . -p 1313

build:
	@echo "Generating build into public dir"
	rm -rvf public
	#bash recents.sh
	hugo --cleanDestinationDir
	hugo --minify --config config.toml,prod.toml --noTimes -s .
	cd static; bash compressimages.sh

github:
	@echo "Uploading files to server"
	#git submodule --init --update
	#git submodule update --remote --merge
	cd content/coding/python; git add -A . ; git commit -m 'Updating notes'; git push origin main; cd -
	cd content/devops/k8s2; git add -A . ; git commit -m 'Updating notes'; git push origin main; cd -
	cd content/devops/aws-notes; git add -A . ; git commit -m 'Updating notes'; git push origin main; cd -
	cd content/infosec/htb-notes; git add -A . ; git commit -m 'Updating notes'; git push origin main; cd -
	cd content/infosec/ctf-notes; git add -A . ; git commit -m 'Updating notes'; git push origin main; cd -
	git add -A . ; git commit -m 'Updating blog'; git push origin main

publish: build
	rsync -avz --delete \
		--exclude='.DS_Store' \
		--exclude='*.swp' \
		public/ halley:~/src/darvein.net/
	scp -rv Makefile halley:~/src/darvein.net/

web:
	sudo rm -rfv /var/www/blog/*
	sudo cp -rf ~/src/darvein.net/* /var/www/blog/
	sudo chown -R http:http /var/www/blog/
	#sudo rsync -avz --delete \
		#--exclude='.DS_Store' \
		#--exclude='*.swp' \
		#public/ /var/www/blog/

getimages:
	scp -rv prompts.txt opt3.py halley:~/tmp/test-st/
	ssh halley "rm -rfv ~/tmp/test-st/*.png"
	ssh halley "source /opt/miniconda3/etc/profile.d/conda.sh ; conda activate sd3_env ; cd ~/tmp/test-st ; python opt3.py"
	scp halley:~/tmp/test-st/*.png static/i/
	scp halley:~/tmp/test-st/*.png static/s/
