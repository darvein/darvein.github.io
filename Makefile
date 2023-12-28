run:
	@echo "Running hugo server"
	bash recents.sh
	./hugo serve --watch  -c content -v -s .
	#./hugo serve --watch  --ignoreCache  --noHTTPCache --disableFastRender -c content -D -E -F -v -s .

build:
	@echo "Generating build into public dir"
	rm -rvf public
	bash recents.sh
	./hugo --minify --config config.toml,prod.toml --noTimes -s .

publish: build
	@echo "Uploading files to server"
	cd content/devops/k8s2; git add -A . ; git commit -m 'Updating notes'; git push origin main; cd -
	exit 0
	git submodule init
	git submodule update
	git add -A . ; git commit -m 'Updating blog'; git push origin main
	cd public && rsync -avz . darveinnet-static:/var/www/darvein.net/html/
