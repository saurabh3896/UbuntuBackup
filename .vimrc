set nocompatible              " be iMproved, required
filetype off                  " required
set mouse=a
syntax enable
set number
set showmatch
set clipboard=unnamedplus
" autocmd VimEnter * NERDTree
" autocmd VimEnter * wincmd p

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
" alternatively, pass a path where Vundle should install plugins
"call vundle#begin('~/some/path/here')

" let Vundle manage Vundle, required
Plugin 'VundleVim/Vundle.vim'
Plugin 'scrooloose/nerdtree'
Plugin 'scrooloose/syntastic'
Plugin 'valloric/youcompleteme'
Plugin 'altercation/vim-colors-solarized'

call vundle#end()            " required
filetype plugin indent on    " required

" key mappings/aliases added by me
cnoreabbrev q qa
cnoreabbrev wq wqa
