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

publish: build
	@echo "Uploading files to server"
	#git submodule --init --update
	#git submodule update --remote --merge
	cd content/coding/python; git add -A . ; git commit -m 'Updating notes'; git push origin main; cd -
	cd content/devops/k8s2; git add -A . ; git commit -m 'Updating notes'; git push origin main; cd -
	cd content/devops/aws-notes; git add -A . ; git commit -m 'Updating notes'; git push origin main; cd -
	cd content/infosec/htb-notes; git add -A . ; git commit -m 'Updating notes'; git push origin main; cd -
	cd content/infosec/ctf-notes; git add -A . ; git commit -m 'Updating notes'; git push origin main; cd -
	git add -A . ; git commit -m 'Updating blog'; git push origin main
	#scp -rv public/* halley:~/src/darvein.net/
