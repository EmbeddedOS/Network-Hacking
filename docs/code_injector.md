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

- For example, when we want to update the package in our system, we run `apt update`
- Install BeEF: `apt-get install beef-xss`
