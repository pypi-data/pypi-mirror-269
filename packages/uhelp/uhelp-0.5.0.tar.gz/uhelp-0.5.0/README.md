<p>
<img alt="Version" src="https://img.shields.io/badge/version-1.0-blue.svg?cacheSeconds=2592000" />
  <img alt="Python" src="https://img.shields.io/badge/-Python-F2C63C.svg?logo=python&style=for-the-badge">
</p>

<h1 align=center>uhelp</h1>  

![uhelp banner](images/uhelp_banner.png)


<img src="images/welcome9.svg" alt="wellcome to your own help. it show dictionaly your own wrote command usage" width="100%" />  

> *You can also search for an excellent community base cheat sheet [tldr](https://tldr.sh)*  
> *and you can also set it to be displayed at the same time as your own.*  

  

#### NOTE : *Now Making*  
> **I don't have an x86_64 computer at hand, so I can't check the operation of the package,**  
> **so I would appreciate it if you could report that it doesn't work..**  

&nbsp;
## Install  

<h5>Ways 1</h5> using pip (PYPI / from this repository) 
  

```sh
pip install uhelp
```  


Package and install directly from this repository with pip  
```sh
pip install git+https://github.com/Suletta-Majo/uhelp.git
```  


<h5>Ways 2</h5> deb package 

*Download the latest release at the bottom that matches your computer's CPU architecture*  
*Cannot be installed on Termux!Proot-Distro environment is possible*  

It is a deb package that uses the compiled Python source.  


Please Make the X.X.X_\*\*\*\*\* part the same as the downloaded filename  
or specify it with a wildcard like uhelp*.deb  

```sh
apt install ./uhelp_X.X.X_*****.deb
```

  

<details>

<summary>*Do not install the PIP version and the DEB version together.*</summary>

##### conflict

Both are a method of starting the program by creating a symbolic link with the same name(uh) in usr/bin.  

So it is possible that one will not start.

</details>
  

## Usage

If you install with pip, you can call it with `uh`,  
and if you install deb with apt, you can call it with `uh` or `uhelp`.

show your command reference example below in case `ls`  

```sh
uh ls
```  
```sh
uhelp ls
```

*priority is User Dictionary > Built-in Dictionary*

&nbsp;


### Edit your own help item
```
uh -e [command name]
```
The text editor opens and you can edit it with reference to the description.  
  

<details>  

<summary>*About Tags Available for Editing*</summary>

it's possible to specify the basically [textual/rich](https://rich.readthedocs.io/en/stable/markup.html) console markup tag syntax,  
like \[blue][/blue] or \[#ffffff on blue][/]  


The tags that are likely to be used in uhelp are defined in the [rich\_theme\_manager](https://pypi.org/project/rich-theme-manager/) directory included with the program.  
\[codez], \[warning] .etc

</details> 


### Remove your own help item
```sh
uh -r [command name]
```


#### Change Theme
```sh
uh -v [theme name]
```
Now you can choose from 5 options: default, retro, retro2, simple, fruits

default
![default style](images/default_style.png)  

| retro                                | retro2                                |
| -------------------------------------| ------------------------------------- |
|![retro style](images/retro_style.png)| ![retro2 style](images/retro2_style.png)|  

| simple                               |fruits                                 |
| -------------------------------------| ------------------------------------- |
| ![simple style](images/simple_style.png)| ![fruits style](images/fruits_style.png)|  


&nbsp;  

### Tldr viwer Mode
```sh
uh -t [command name]
```
Command help mode using only [tldr pages](https://tldr.sh)


Check out the uhelp dictionary for other options such as backups and restores.`uh uhelp`


***

&nbsp;


As a bonus feature, there is a function to take a short note before falling asleep

```sh
uh -s i try fix suboutput function.but I think I'm going to sleep
```
```sh
uh -s "i try fix suboutput function.but I think I'm going to sleep"
```
Record up to 10 records

To view choose on  prompt 'no'


&nbsp;
## Author

👤 **Suletta-Majo**

* Github: [@Suletta-Majo](https://github.com/Suletta-Majo)

## Show your support

Give a ⭐️ if this project helped you!  


  

***

appendix: [A very useful tools used to create this page!!](appendix.md)  
 
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_
