" Show file stats
set ruler

" Encoding
set encoding=utf-8

" General
set background=dark
syntax on
set number
set nowrap
set cursorline
set colorcolumn=80
highlight ColorColumn ctermbg=gray

set scrolloff=3

" Indentation

set expandtab " tab to space
set tabstop=4
set shiftwidth=4
set softtabstop=4
set smartindent

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

noremap t h
noremap s j
noremap r k
noremap n l
