# git remote add listen https://github.com/deeuu/listen.git

# Update listen
git checkout master
git fetch listen
git checkout listen/master site/assets/js site/_layouts site/_includes
git commit -a -m "Merge listen"
