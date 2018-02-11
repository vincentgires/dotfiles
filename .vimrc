" Show file stats
set ruler

" Encoding
set encoding=utf-8

" General
syntax on
set number
set nowrap
set colorcolumn=80
set cursorline

set scrolloff=3

set expandtab " tab to space
set tabstop=4
set shiftwidth=4
set softtabstop=4

" Status bar
set laststatus=2

" Last line
set showmode
set showcmd

" Searching
nnoremap / /\v
vnoremap / /\v
set hlsearch
set incsearch
set ignorecase
set smartcase
set showmatch
map <leader><space> :let @/=''<cr> " clear search

