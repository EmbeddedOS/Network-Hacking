# Code injector

- Modifying data in HTTP layer
  - Edit requests/responses.
  - Replace download requests.
  - Inject code (html, javascript).

## Analysing the HTTP response

## Client Side Attacks - BeEF Framework & Basic hook method

- Browser Exploitation Framework allowing us to launching a number of attacks on a hooked target.
- Targets are hooked once they load a hook url.
  - DNS spoof requests to a page containing the hook.
  - Inject the hook in browsed pages (need to be MITM)
  - Use XSS exploit.
  - Social engineer the target to open a hook page.

- Install BeEF:

```bash
sudo apt-get install software-properties-common
sudo apt-add-repository -y ppa:brightbox/ruby-ng
sudo apt-add-repository -y ppa:rael-gc/rvm
sudo apt-get install rvm
rvm install "ruby-2.5.3"
echo 'source "/etc/profile.d/rvm.sh"' >> ~/.bashrc
sudo add-apt-repository ppa:jonathonf/gcc-9.0
sudo apt-get install gcc-9

git clone https://github.com/beefproject/beef
cd beef
./install 
./beef 

```
