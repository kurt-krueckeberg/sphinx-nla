# todo

## Work on the remaining build errors.

There  is a theme setting for  navigation menu levels expanded.

## Work on Appearance

[ChatGPT link++](https://chatgpt.com/share/69d41db3-02b4-832d-9145-4a80dae325ad)

## Test cross ferences to other Projects

Some Antora `xref:`'s reference AsciiDoc files in different Antora components, like the
**genealogy** or **immanuel** components, not merely different modules within the
current component; for example,

`xref:genealogy:petzen:PET-B-1728a.adoc[]`
 
references the **PET-B-1728a.adoc** file located in the **petzen** module
of the **genealogy** component. 
 
We are using the built-in Sphinx extension `sphinx.ext.intersphinx` (which
is enabled in **conf.py**) to support cross-Sphinx proejct corss refences.
Using it, the equivalent MyST cross reference of
`xref:genealogy:petzen:PET-B-1728a.adoc[]` is
**{external+genealogy:doc}`petzen/PET-B-1728a`**.
 
**adoc2myst** and **convert.py** support Antora/AsciiDoc `xref:`'s that 
 
 1. refer to files in other modules with the same component, whose
    syntax is: `xref:146:other-docs.adoc[]`
 2. refer to files in other components, whose syntax is:
    `xref:genealogy:petzen:PET-M-1822a.adoc[]` or
    `xref:genealogy:petzen:PET-B-1744a.adoc[Johann Heinrich's baptism]`
In the cross reference `xref:genealogy:petzen:PET-M1822a.adoc[]`, the MyST
link text in the converted MyST cross reference should be the page header
of the **PET-M1822a.adoc** file.
