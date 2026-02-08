# pyvestaboard
Python library for sending and displaying messages from a Vestaboard

# FIXME
- Link to instructions for activating your local Vestaboard API and getting the token
- Add instructions or code to find the Vestaboard on the local network

# Running CLI client locally
- Create a virtualenv and activate it
- In the root directory of the git repo:
-- Run `python3 -m pip install --upgrade build`
-- Run `python3 install -e .`

You should now be able to run the `vb` command. On first run it will ask you about connection information for your Vestaboard. You'll need to have the IP on hand. The port will be 7000 by default. The connection info will be stored in `~/.pyvestaboard`. and will be reused after being set.