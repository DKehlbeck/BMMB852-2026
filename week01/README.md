# Week 1

## git setup
Make a github account at [github.com][url0]
[url0]: https://github.com/

Generate an ssh key with the following algorithm 
> $ ssh-keygen -t ed25519

Link to github repository
> $ git config --global user.name 

> $ git config --global user.email

> $ git clone git@github.com:DKehlbeck/BMMB852-2026.git

Setup this README
> mkdir week01

> $ cd week01

> $ echo "Hello World" > README.md


### Testing git push
Hello World
> $ git commit -am "Added week01/README.md"
> $ git push

Editing .md file using vim, save with ZZ
> $ vim README.md

Here is additional text I wrote at 18:29 20260830
> $ git commit -am "updated some more text"
> $ git push

## Markdown test
Bold test with two astericks **this should be in bold**

For things like HTML and writing inline code use an apostophre. The following 'should be in line code'

To indent for a blockquote use a greater-than symbol

>This should be indented
>> This should be twice indented

Use an astericks and a space to delineate list items
* Item 1
* Item 2
* Item 3

[A link to Google][url]

[url]: https://www.google.com


I've been editing this file using
>$ vim README.md

I've been double checking markdown format using
>visual studio code

## Getting Started
[Follow setup on course home page for pixi on local machine][url2]
[url2]: https://www.biostarhandbook.com/courses/2026/appbio/setup/pixi-intro/
 

[Follow setup on course home page for setting up bioinfo on local machine][url3]
[url3]: https://www.biostarhandbook.com/courses/2026/appbio/setup/bioinfo-env/
Bioinfo exists here: /home/declan/declan/BMMB852/bioinfo

A symlink was setup to easily call it from home directory using the following:

> $ ln -s /home/declan/declan/BMMB852/bioinfo bioinfo

From any directory bio info can be activated with
> $ pixi shell -m ~/bioinfo/

Checking versions
> $ samtools --version

> samtools 1.24
> Using htslib 1.24

> $ bwa

> Program: bwa (alignment via Burrows-Wheeler transformation)
> Version: 0.7.19-r1273

## Assignment 1 
Practice directory generation
> $ mkdir week01sub

Make a sub directory
> $ mkdir week01sub/week01sub_subdirectory

Make a file in that subdirectory
> $ echo "These are my notes." > week01sub/week01sub_subdirectory/notes.txt

Write file with path information
> $ echo "Absolute path:" > week01sub/week01sub_subdirectory/notes.txt
pwd >> week01sub/week01sub_subdirectory/notes.txt
echo "Relative path:" >> week01sub/week01sub_subdirectory/notes.txt
echo "week01sub/week01sub_subdirectory/notes.txt" >> week01sub/week01sub_subdirectory/notes.txt
