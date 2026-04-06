# todo

## Work on the remaining build errors.

## Get rid of side-by-sdie image entirely. 

Command used to find .adoc files with side by side images:

```regex
~/nla/m main ❯ rg -l -U '\[cols="[^"]*1a,[^"]*1a[^"]*"[^\]]*\][\s\S]*?\|===\n\|image::[^\n]*\n\|image::[^\n]*\n\|===' ~/antora-nla/modules/*/pages | sort                                         sphinx-nla
```

**Results:**

/home/kurt/antora-nla/modules/1237/pages/doc3.adoc
/home/kurt/antora-nla/modules/1237/pages/doc5.adoc
/home/kurt/antora-nla/modules/1237/pages/doc6.adoc
/home/kurt/antora-nla/modules/139/pages/actum-bueckeburg-amt-21-aug-1849.adoc
/home/kurt/antora-nla/modules/139/pages/doc1-1.adoc
/home/kurt/antora-nla/modules/139/pages/rentkammer-confirmation-and-instruction-regards-sale-of-krueckeberg-holding.adoc
/home/kurt/antora-nla/modules/139/pages/sales-contract-for-no-10.adoc
/home/kurt/antora-nla/modules/2741/pages/index.adoc
/home/kurt/antora-nla/modules/689/pages/doc10.adoc
/home/kurt/antora-nla/modules/689/pages/doc2-1.adoc
/home/kurt/antora-nla/modules/689/pages/doc5.adoc
/home/kurt/antora-nla/modules/689/pages/doc6-3.adoc
/home/kurt/antora-nla/modules/689/pages/doc8-2.adoc
/home/kurt/antora-nla/modules/689/pages/doc8-3.adoc


[ChatGPT link++](https://chatgpt.com/share/69d41db3-02b4-832d-9145-4a80dae325ad)
