
# SPAM - A <u>S</u>oftware <u>PA</u>ckage <u>M</u>anager #

To be honest,
it's not really a package manager,
but merely a wrapper that presents a uniform command-line interface
across Linux distros.


## Usage & Features ##

👉  Easy to type and use every day.
For example, to operate on the *foo* package:

```sh
⏵ spam -h               # usage and additional/customized cmd list

⏵ spam up               # or update; upgrade
⏵ spam in foo           # or install
⏵ spam rm foo           # or uninstall
⏵ spam clean            # clean up downloads and autoremove

# Moar!
⏵ spam add foo://bar    # add repo
⏵ spam info foo         # or show
⏵ spam lsf foo          # or listfiles
⏵ spam pr /bin/foo      # or provides, what or who-owns file
⏵ spam pu foo           # or purge
⏵ spam se foo           # or search
```

👉  It knows when to invoke sudo,
so you rarely need to worry about it.

👉  It prints the command it runs,
so you can learn how to do it on a package manager you may not be as familiar
with.
Also, if it wasn't able to do what you want,
it is easy to recover.


## Support ##

Currently supports Debian `apt` and Fedora `dnf`,
with hopefully more to come as time allows.


<!---
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)
-->
