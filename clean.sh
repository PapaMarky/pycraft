rm -rf dist pycraft.egg-info
find . -name '*~' -exec rm {} \;
find . -name '#*' -exec rm {} \;
find . -name '*.pyc' -exec rm {} \;
find . -name '*.png' -exec rm {} \;
