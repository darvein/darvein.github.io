run:
	@echo "Running hugo server"
	bash recents.sh
	./hugo --cleanDestinationDir
	./hugo serve --watch --noHTTPCache --disableFastRender -c content -D -E -F -v -s .
	#./hugo serve --watch  --ignoreCache  --noHTTPCache --disableFastRender -c content -D -E -F -v -s .

build:
	@echo "Generating build into public dir"
	rm -rvf public
	bash recents.sh
	./hugo --cleanDestinationDir
	./hugo --minify --config config.toml,prod.toml --noTimes -s .

publish: build
	@echo "Uploading files to server"
	#git submodule init
	#git submodule update
	cd content/coding/exercism; git add -A . ; git commit -m 'Updating notes'; git push origin main; cd -
	cd content/coding/codewars; git add -A . ; git commit -m 'Updating notes'; git push origin main; cd -
	cd content/coding/codeforces; git add -A . ; git commit -m 'Updating notes'; git push origin main; cd -
	cd content/coding/pytorch; git add -A . ; git commit -m 'Updating notes'; git push origin main; cd -
	cd content/coding/python; git add -A . ; git commit -m 'Updating notes'; git push origin main; cd -
	cd content/devops/k8s2; git add -A . ; git commit -m 'Updating notes'; git push origin main; cd -
	cd content/devops/aws-notes; git add -A . ; git commit -m 'Updating notes'; git push origin main; cd -
	cd content/infosec/htb-notes; git add -A . ; git commit -m 'Updating notes'; git push origin main; cd -
	cd content/infosec/ctf-notes; git add -A . ; git commit -m 'Updating notes'; git push origin main; cd -
	git add -A . ; git commit -m 'Updating blog'; git push origin main
	cd public && rsync -avz . darveinnet-static:/var/www/darvein.net/html/
