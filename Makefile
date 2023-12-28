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
	git add -A . ; git commit -m 'updating blog'; git push origin main
	cd public && rsync -avz . darveinnet-static:/var/www/darvein.net/html/
