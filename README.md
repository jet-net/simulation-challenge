# jet-net.github.io/simulation-challenge

[![Codestyle](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/jet-net/simulation-challenge/main.svg)](https://results.pre-commit.ci/latest/github/jet-net/simulation-challenge/main)

## Development guide

1. Install Ruby and Jekyll via https://jekyllrb.com/docs/installation/
   1. Note that for Mac I had to use `ruby-install ruby 3.1.3 -- --with-openssl-dir=$(brew --prefix openssl@3)` to install Ruby, see https://github.com/rbenv/homebrew-tap/issues/9#issuecomment-1650014112
   2. Also then had to run `gem install jekyll bundler` and `bundle add webrick`
2. Run `bundle install`
3. To run web page locally: `bundle exec jekyll serve --livereload`
   1. Again for my Mac I had to first do `bundle add webrick`. See [here](https://stackoverflow.com/a/70916831/3759946).
