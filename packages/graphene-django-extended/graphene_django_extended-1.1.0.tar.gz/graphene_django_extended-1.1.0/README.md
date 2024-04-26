
## CAVEATS 
- No tests for now 
- Stubs are missing for graphene and graphene-django
- Unstable API - needs more usage
- Version 1.0.2 is the most stable
- Version 1.1 includes filtering capabilities (from DjangoFilterConnectionField), which is NOT an opt-in. It requires all Nodes to have filter_fields defined. It might also break the DjangoInterface, untested yet.

## TODO
- Make sure Sphinx generates docs from all files
- generate html instead of md ???
- add general introduction and usage guide on the docs

## Build
`hatch build` or `python -m hatch build`
`hatch publish` or `python -m hatch publish` with username `__token__`. Make sure the [keyrings backend](https://github.com/jaraco/keyrings.alt) is installed. 
On arch `pacman -S python-hatch python-keyrings-alt`, publish with `username:__token__`
The default keyring is located at `~/.local/share/python_keyring/` and uses the name "main". Again this is not a recommended implementation, just a quick and dirty keyring usage
