#!/bin/sh

echo "[`date`]: Updating Twitter and Instapaper."

git pull origin master &&
python /home/git/mirrored-repositories/mgc/_aggregators/aggregator.instapaper.py &&
python /home/git/mirrored-repositories/mgc/_aggregators/aggregator.twitter.py &&
git add . &&
git commit -m "Autoupdate Instapaper and Twitter for `date`." &&
git push origin master
