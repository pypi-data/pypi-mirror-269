-- Slice It Off! v0.3b --


Description:

	Small game where goal is to beat hiscores. Score is gained by
	slicing parts of playing area off. Faster you do it more score you
	get. If you hit enemies while slicing you lose healt. There will be
	also bonuses to boost the scores.


Installing:
	
	Get version on PyPI:
	- pip install sliceitoff

	One can also use provided `./dev.sh` shell script to buid and install
	any version of game:
	- `git clone https://git.hix.fi/scliceitoff.git`
	- `cd sliceitoff`
	- `./dev.sh install`

	Distribution package can be installed normally:
	- `pip(x) install sliceitoff.*.tar.gz`


License:

	This project uses GPL-2 license. Used components uses their
	licenses. There is gnufonts package from FreeDOS included in the
	source tree and it's license can be found on it's directory.


Developement:
	
	Project makes heavy use of poetry build and dependencies control
	system. Many shortcuts can be run easily from `./dev.sh` script:
	- `./dev.sh`
	- `./dev.sh dev`
	- `./dev.sh pytest`
	- `./dev.sh covff`
	- `./dev.sh all`
	- etc
